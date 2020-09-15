from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'no_of_adults',
            'no_of_children',
            'journey_type'
        ]

        widgets = {
            'no_of_adults': forms.TextInput(attrs={'class': 'form-control'}),
            'no_of_children': forms.TextInput(attrs={'class': 'form-control'}),
            'journey_type': forms.RadioSelect(attrs={'class': 'list-unstyled'}),
        }