from django.contrib import admin
from .models import Allowed_user, Name_list, API, Event, Event_token, Login_Token
# Register your models here.
admin.site.register(API)
admin.site.register(Allowed_user)
admin.site.register(Event)
admin.site.register(Event_token)
admin.site.register(Login_Token)
admin.site.register(Name_list)
