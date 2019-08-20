from django.http import *
from .models import OTP
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from evoterform.functions import genrandomstring
from evoterform.models import AccountDetail, Task, WorkerProfile
from .encryption import gen2key, decrypt
from django.contrib.auth.models import User
from django.core.mail import send_mail
from regapi.models import Event_token
from django.utils import timezone


def loginView(request):
    logout(request)
    username = password = ''
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            data = AccountDetail.objects.filter(voterID=user.username)
            if user.is_active and len(data) == 1:
                data = data[0]
                keys = gen2key()
                otps = OTP.objects.all().filter(account=user)
                for otp in otps:
                    otp.delete()
                otp = OTP(message=keys[2], encrypt=keys[1], private_key=keys[0], account=user)
                mailbody = f"""
                Dear User,
                You are mailed a text enter it in appropriate field-
                Line 1 : '{keys[0]}'
                Line 1 : '{keys[1]}'
                Regards,
                MainAdmin
                (EVoterAuth)
                """
                send_mail('OTP has been mailed', mailbody, 'admin@evoter.com', [data.email])
                otp.save()
                return redirect(reverse('otp-login-view', args=(user,)))
    return render(request, 'voter-login.html')


def OTPview(request, user):
    logout(request)
    try:
        user = User.objects.get(username=user)
        otp = OTP.objects.get(account=user, expiry_date__gte=timezone.now())
        if request.POST:
            line1 = request.POST['Line 1']
            line2 = request.POST['Line 2']
            if decrypt(line1, line2, otp.message):
                login(request, user)
                otp.delete()
                return redirect('voter-profile-view')
            else:
                messages.error(request, 'The OTP did not match.')
        return render(request, 'voter-otp.html')
    except Exception:
        otps = OTP.objects.all().filter(account=user)
        for opt in otps:
            opt.delete()
        return HttpResponseNotFound()


def VoterProfileView(request):
    try:
        user = request.user
        details = AccountDetail.objects.get(voterID=user.username)
        events = Event_token.objects.filter(user=user)
        return render(request, "voter-profile.html", {"events": events})
    except Exception:
        return redirect('main-login-view')


def AdminLoginView(request):
    logout(request)
    username = password = ''
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active and len(WorkerProfile.objects.all().filter(user=user)) == 1:
                print(user)
                login(request, user)
                return redirect('admin-profile-view')
    return render(request, 'admin login.html')


def AdminProfileView(request):
    try:
        tasks = Task.objects.all().filter(worker__user=request.user)
        return render(request, 'admin-profile.html', {'user': request.user, 'tasks': tasks})
    except Exception:
        return redirect('admin-login-view')


def LogoutView(request):
    logout(request)
    return redirect('main-view')
