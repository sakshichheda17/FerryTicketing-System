from django import forms
from .models import Leg

days = [
        ('Monday',"Monday"),
        ('Tuesday',"Tuesday"),
        ('Wednesday',"Wednesday"),
        ('Thurday',"Thurday"),
        ('Friday',"Friday"),
        ('Saturday',"Saturday"),
        ('Sunday',"Sunday"),
]
class DateInput(forms.DateInput):
    input_type = 'date'


class LegForm(forms.ModelForm):
    class Meta:
        model = Leg
        
        fields = [
                    'date',
                    'day',
                    'run_id',
                    'source',
                    'destination',
                    'vessel_name',
                    'departure_time',
                    'arrival_time',
                    'PASS',
                    'PARS',
                    'PCSS',
                    'PCRS',
                    'max_seats',
                    'sold_seats',
                    'available_seats',
                    'cancelled_status',

                ]

        widgets = {
        'date': DateInput(),
        'departure_time': forms.TimeInput(attrs={'type': 'time','value':"12:00"}),
        'arrival_time': forms.TimeInput(attrs={'type': 'time','value':"14:00"}),
        'run_id': forms.TextInput(attrs = {'value':0}),
        #'available_seats': forms.TextInput(attrs = {'value':fields[12]}),
        'sold_seats': forms.TextInput(attrs = {'value':0}),
        'day': forms.Select(choices=days)
    	}

