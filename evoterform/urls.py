from django.urls import path
from .views import EVoterFormView, VerificationView

urlpatterns = [
    path('', EVoterFormView, name='mainform-view'),
    path('<slug:connectionhash>/verify', VerificationView, name='verify-view')
]
