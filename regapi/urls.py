from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import CreateTokenView, APIVoterLogin, AddUserView, CorporateCreateView, APIVoterOTP, VerifyTokenView, ProfileView, CorporateLogin, AddEventView


urlpatterns = [
    path('verify-token/', VerifyTokenView, name='verify-token'),
    path('createtoken/', CreateTokenView, name='create-token'),
    path('login/<str:token>', APIVoterLogin, name='api-login-view'),
    path('otp/<str:user>/<str:token>', APIVoterOTP, name='otp-api-view'),
    path('profile/', ProfileView, name='api-profile-view'),
    path('corporate/login/', CorporateLogin, name='corporate-login-view'),
    path('corporate/create/', CorporateCreateView, name='corporate-create-view'),
    path('addevent/', AddEventView, name='add-event'),
    path('adduser/', AddUserView, name='add-user-view')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
