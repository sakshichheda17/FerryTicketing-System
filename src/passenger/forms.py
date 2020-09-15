from django import forms
from .models import Passenger


class PassengerCreationForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = [
        			'username',
        			'password',
        			'email',
        			'phone_no'
        	]
        widgets = {
        'password': forms.PasswordInput(),
    	}


class PassengerLoginForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = [
                    'username',
                    'password',
                ]
        widgets = {
            'password': forms.PasswordInput(),
            }