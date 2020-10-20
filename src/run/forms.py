from django import forms
from .models import Run
                                    


class DateInput(forms.DateInput):
    input_type = 'date'


class RunForm(forms.ModelForm):
    
    class Meta:
        model = Run
        fields = [
                    'vessel_name',
                    'max_seats',
                    'source',
                    'destination',
                    'departure_time',
                    'arrival_time',
                    'PASS',
                    'PARS',
                    'PCSS',
                    'PCRS',
                    'Mon',
                    'Tue',
                    'Wed',
                    'Thu',
                    'Fri',
                    'Sat',
                    'Sun',
        ]
        
      

        widgets = {
        'max_seats': forms.TextInput(attrs = {'value':0}),
        'departure_time': forms.TimeInput(attrs={'type': 'time'}),
        'arrival_time': forms.TimeInput(attrs={'type': 'time'}),
        'PCSS': forms.TextInput(attrs = {'value':0}),
        'PASS': forms.TextInput(attrs = {'value':0}),
        'PARS': forms.TextInput(attrs = {'value':0}),
        'PCRS': forms.TextInput(attrs = {'value':0}),
        
       
        }

