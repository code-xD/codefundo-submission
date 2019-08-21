from django.shortcuts import render, redirect
from .forms import EVoterForm, ContactForm
from .blockchain import runblockchain
import requests
import random
from .searchcodes import getcodes
from django.core.mail import send_mail
from .models import AccountDetail, CacheVoterData
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.models import User
from django.contrib import messages
from .functions import addressparser, taskmailbody, genrandomstring, getminworker
from .models import Task
# from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.


def home(request):
    logout(request)
    return render(request, "home.html")


def EVoterFormView(request):
    logout(request)
    if request.method == 'POST':
        v_form = EVoterForm(request.POST)
        c_form = ContactForm(request.POST, request.FILES)
        # print(v_form)
        if v_form.is_valid() and c_form.is_valid():
            voterdata = v_form.cleaned_data
            # print(voterdata)
            if len(AccountDetail.objects.all().filter(aadhar_no=voterdata['aadhar_no'])) == 0:
                contactdata = c_form.save(commit=False)
                contactdata.aadhar_no = voterdata['aadhar_no']
                if not voterdata['age'] < 18:
                    templatedata = requests.get(
                        f"http://codefundo-heroku.herokuapp.com/details/{voterdata['aadhar_no']}", auth=('testuser', 'codefundo'))
                    try:
                        templatedata = templatedata.json()
                        aLine1 = voterdata['aLine1']
                        aLine2 = voterdata['aLine2']
                        templatedata['aLine1'] = addressparser(templatedata['aLine1'])
                        templatedata['aLine2'] = addressparser(templatedata['aLine2'])
                        voterdata['aLine1'] = addressparser(voterdata['aLine1'])
                        voterdata['aLine2'] = addressparser(voterdata['aLine2'])
                        scd = getcodes(voterdata['s_code'],
                                       voterdata['c_code'], voterdata['d_code'])
                        voterdata['s_code'] = scd[0]
                        voterdata['c_code'] = scd[1]
                        voterdata['d_code'] = scd[2]
                        for key, value in voterdata.items():
                            if str(templatedata[key]) != str(value):
                                print(templatedata[key], value)
                                raise Exception
                        status = runblockchain(voterdata, templatedata)
                    except Exception:
                        messages.error(request, 'Your entered data did not match with the dataset')
                        return redirect('/form/')
                    else:
                        print("status", status)
                        if status == '1':
                            print("equal")
                            voterdata['aLine1'] = aLine1
                            voterdata['aLine2'] = aLine2
                            contactdata.connectionHash = genrandomstring(250)
                            minworker = getminworker()
                            url = taskmailbody(contactdata.connectionHash, minworker.user.email)
                            task = Task(connectionurl=url, worker=minworker,
                                        connectionHash=contactdata.connectionHash)
                            task.save()
                            minworker.task_count += 1
                            minworker.save()
                            contactdata.save()
                            del voterdata['contractProperties']
                            cvoterdata = CacheVoterData(**voterdata)
                            cvoterdata.save()
                            messages.success(
                                request, """Your details are sent to the Admin.
                                You will be notified in the mail""")
                            return redirect('/form/')
                        elif status != '1':
                            messages.error(
                                request, 'Your entered data did not match with the dataset')
                else:
                    messages.error(request, "You are underage to make a voter ID Card")
            else:
                messages.error(request, "Already filled the form")
            return redirect('/form/')
    v_form = EVoterForm()
    c_form = ContactForm()
    return render(request, 'voterform.html', {'v_form': v_form, 'c_form': c_form})


def VerificationView(request, connectionhash):
    # try:
    required_data = AccountDetail.objects.get(connectionHash=connectionhash)
    tasks = Task.objects.all().filter(connectionHash=connectionhash)
    if len(tasks) != 1:
        raise Exception
    task = tasks[0]
    if task.worker.user != request.user:
        return redirect('admin-login-view')
    aadhar_no = required_data.aadhar_no
    print(required_data.aadhar_no)
    evoterdata = CacheVoterData.objects.get(aadhar_no=aadhar_no)
    if request.method == 'POST':
        if "verified" in request.POST:
            required_data.voterID = int(''.join([str(random.randint(1, 9)) for i in range(12)]))
            password = genrandomstring(15)
            user = User(username=required_data.voterID)
            user.save()
            user.set_password(password)
            user.save()
            send_mail(
                "Verification Successful",
                f"""
                Your details have been successfully verfied.
                Below are your logincredentials-
                username-{user.username}
                password-{password}
                Regards,
                MainAdmin
                (EVoterAuth)
                """,
                'admin@evoter.com', [required_data.email]
            )
            # print("verified")
            required_data.connectionHash = ''
            required_data.save()
        elif "failed" in request.POST:
            send_mail(
                "Verification Failed",
                """
                Your Verification has been unsuccessful.
                The admin did not approve the documents.
                Regards,
                MainAdmin
                (EVoterAuth)
                """,
                'admin@evoter.com', [required_data.email]
            )
            required_data.delete()
        task.delete()
        evoterdata.delete()
        return redirect('admin-profile-view')
    return render(request, 'evoterform/verification.html', {'voterdata': evoterdata, 'imagedata': required_data})
    # except Exception:
    #     return HttpResponseNotFound()
