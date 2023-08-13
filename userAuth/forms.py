from django import forms
from django.contrib.auth.models import User
from .models import userInfo


class userform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

    def __init__(self, *args, **kwargs): 
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs = ({'class': 'form-control', 'placeholder': "First name"})
        self.fields['last_name'].widget.attrs = ({'class': 'form-control', 'placeholder': "Last Name"})
        self.fields['email'].widget.attrs = ({'class': 'form-control', 'placeholder': "Email Address"})
        self.fields['username'].widget.attrs = ({'class': 'form-control', 'placeholder': "Username"})
        self.fields['password'].widget.attrs = ({'class': 'form-control', 'placeholder': "Password"})



class userformMoreinfo(forms.ModelForm):
    
    class Meta():
        model = userInfo
        fields = ('phone', 'gender', 'proPic')

    def __init__(self, *args, **kwargs): 
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        self.fields['proPic'].label = 'Profile pic'

        self.fields['phone'].widget.attrs = ({'class': 'form-control', 'placeholder': "Phone Number"})
        self.fields['gender'].widget.attrs = ({'class': 'form-control', 'placeholder': "Gender"})
        self.fields['proPic'].widget.attrs = ({'class': 'form-control-file'})





