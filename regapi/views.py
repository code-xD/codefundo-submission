from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from evoterform.functions import genrandomstring, genrandomint
from .models import API, Event, Login_Token, Allowed_user, Event_token, Name_list
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
import json
import requests
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from evoterform.models import AccountDetail
from userauth.encryption import genspkey, decrypt, gen2key
from userauth.models import OTP
from .forms import CorporateForm, UserCreateForm, AuserForm, EventForm
from django.conf import settings


@csrf_exempt
def CreateTokenView(request):
    try:
        if request.method == 'POST':
            request_dict = json.loads(request.body)
            api_key = request_dict['api_key']
            api_secret = request_dict['api_secret']
            event_id = request_dict['event_id']
            api = API.objects.get(api_key=api_key, api_secret=api_secret)
            print(api)
            event = Event.objects.get(api=api, event_id=event_id)
            token = genrandomstring(32)
            login_token = Login_Token(token=token, event=event)
            login_token.save()
            return JsonResponse({'login_token': login_token.token})
    except Exception:
        return HttpResponseNotFound()
    return HttpResponseNotFound()


def APIVoterLogin(request, token):
    logout(request)
    username = password = ''
    try:
        login_token = Login_Token.objects.get(token=token, expiry_date__gte=timezone.now())
        event = login_token.event
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            users = Allowed_user.objects.all().filter(event=event)
            user_list = []
            for usr in users:
                print(usr.user)
                user_list.append(usr.user)
            if user is not None:
                if user not in user_list:
                    return HttpResponse('You are not registered for this event.')
                if len(Event_token.objects.filter(event=login_token.event, user=user)) != 0:
                    return HttpResponse('You have already voted.')
                if user.is_active:
                    data = AccountDetail.objects.get(voterID=user.username)
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
                    return redirect(reverse('otp-api-view', args=(user.username, login_token.token,)))
        return render(request, 'voter-login.html', {"event": event})
    except Exception:
        return HttpResponseNotFound()


def APIVoterOTP(request, user, token):
    try:
        user = User.objects.get(username=user)
        otp = OTP.objects.get(account=user, expiry_date__gte=timezone.now())
        login_token = Login_Token.objects.get(token=token, expiry_date__gte=timezone.now())
        if request.POST:
            line1 = request.POST['Line 1']
            line2 = request.POST['Line 2']
            if decrypt(line1, line2, otp.message):
                otp.delete()
                key = login_token.event.private_key
                key_list = genspkey(key)
                event_token = Event_token(event=login_token.event,
                                          user=User.objects.get(username=user), token=key_list[0])
                event_token.save()
                user_data = {
                    'Event_ID': event_token.event.event_id,
                    'user_token': key_list[1]
                }
                requests.post(event_token.event.api.callback_url, json=user_data)
                login_tokens = Login_Token.objects.filter(expiry_date__lte=timezone.now())
                for login_token in login_tokens:
                    login_token.delete()
                return redirect(event_token.event.api.redirect_url)
            else:
                messages.error(request, 'The OTP did not match.')
        return render(request, 'voter-otp.html')
    except Exception:
        otps = OTP.objects.all().filter(account=user)
        for opt in otps:
            opt.delete()
        return HttpResponseNotFound()


@csrf_exempt
def VerifyTokenView(request):
    try:
        if request.method == 'GET':
            request_dict = json.loads(request.body)
            api_key = request_dict['api_key']
            api_secret = request_dict['api_secret']
            event_id = request_dict['event_id']
            usertoken = request_dict['user_token']
            api = API.objects.get(api_key=api_key, api_secret=api_secret)
            event = Event.objects.get(api=api, event_id=event_id)
            events = Event_token.objects.all().filter(event=event).values_list('token', flat=True)
            for i in range(len(events)):
                if decrypt(event.private_key, usertoken, events[i]):
                    return JsonResponse({'verified': True})
            return JsonResponse({'verified': False})
    except Exception:
        return HttpResponseNotFound()


@csrf_exempt
def CorporateLogin(request):
    logout(request)
    if request.method == 'POST':
        print("POST")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('api-profile-view')
    return render(request, 'corp login.html')


def ProfileView(request):
    try:
        profile = API.objects.get(user=request.user)
        events = Event.objects.filter(api=profile)
        for event in events:
            total_votes = len(Allowed_user.objects.filter(event=event))
            voted = len(Event_token.objects.filter(event=event))
            event.total = total_votes
            event.voted = voted
        return render(request, 'corp-profile.html', {'user': request.user, 'events': events, 'profile': profile})
    except Exception:
        return redirect('corporate-login-view')


def CorporateCreateView(request):
    if request.method == 'POST':
        print('post')
        u_form = UserCreateForm(request.POST)
        a_form = CorporateForm(request.POST)
        if u_form.is_valid() and a_form.is_valid():
            print('valid')
            user = u_form.save()
            api = a_form.save(commit=False)
            api.api_key = genrandomint(10)
            api.api_id = genrandomint(15)
            api.api_secret = genrandomstring(32)
            api.user = user
            api.save()
        return redirect('corporate-login-view')
    return render(request, 'API registration.html')


def AddEventView(request):
    # try:
    api = API.objects.get(user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST)
        event = form.save(commit=False)
        event.event_id = genrandomint(15)
        event.private_key = genrandomstring(32)
        event.api = api
        event.save()
        return redirect('api-profile-view')
    form = EventForm()
    return render(request, 'regapi/eventform.html', {'form': form})
    # except Exception:
    #     return redirect('corporate-login-view')


def AddUserView(request):
    try:
        api = API.objects.get(user=request.user)
        if request.method == 'POST':
            form = AuserForm(api, request.POST, request.FILES)
            ff = form.save()
            event = ff.event
            with open(settings.MEDIA_ROOT+'/'+str(ff.name_list), 'r') as file:
                while file:
                    voter_id = file.readline()
                    voter_id = voter_id.strip('\n')
                    voter_id = voter_id.strip(' ')
                    voter_id = voter_id.strip('\t')
                    if voter_id == '':
                        break
                    print('voter_id', voter_id)
                    try:
                        ac = AccountDetail.objects.get(voterID=voter_id)
                        au = Allowed_user.objects.filter(
                            event=event, user=User.objects.get(username=voter_id))
                        for u in au:
                            print(u)
                        if len(au) == 0:
                            au = Allowed_user(
                                event=event, user=User.objects.get(username=voter_id))
                            au.save()
                    except Exception:
                        messages.error(request, 'File not properly configured.')
                        return render(request, 'regapi/eventform.html', {'form': form})
            return redirect('api-profile-view')
        file_field = AuserForm(api)
        return render(request, 'regapi/eventform.html', {'form': file_field})
    except Exception:
        return redirect('corporate-login-view')
