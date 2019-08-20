from django import forms
from .models import AccountDetail

genderlist = (
    (1, 'Male'),
    (2, 'Female'),
    (3, 'Others')
)


class EVoterForm(forms.Form):
    voter_name = forms.CharField(max_length=200, label='',
                                 widget=forms.TextInput(attrs={'placeholder': 'Name(As Per Aadhar Card)'}))
    age = forms.IntegerField(label='', widget=forms.TextInput(attrs={'placeholder': 'Age'}))
    gender = forms.ChoiceField(label='', choices=genderlist)
    aadhar_no = forms.IntegerField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Aadhar Number'}))
    aLine1 = forms.CharField(max_length=500, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Address(Line 1)'}))
    aLine2 = forms.CharField(max_length=500, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Address(Line 1)'}))
    s_code = forms.CharField(max_length=500, label='',
                             widget=forms.TextInput(attrs={'placeholder': 'State'}))
    c_code = forms.CharField(max_length=500, label='',
                             widget=forms.TextInput(attrs={'placeholder': 'City'}))
    d_code = forms.CharField(max_length=500, label='',
                             widget=forms.TextInput(attrs={'placeholder': 'District'}))
    pin = forms.IntegerField(label='', widget=forms.TextInput(attrs={'placeholder': 'Pincode'}))


class ContactForm(forms.ModelForm):
    class Meta:
        model = AccountDetail
        fields = ['email', 'voter_photo', 'govtID_card', 'address_proof']
