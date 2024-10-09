from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError
from .models import Patient, Staff, CasualtyReport

class PatientForm(forms.ModelForm):
    registered_at = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Patient
        fields = ['name', 'place', 'age', 'phone', 'gender', 'registered_at']

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['place'].widget.attrs.update({'class': 'form-control'})
        self.fields['age'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})

    # Validate registered_at field to ensure no future dates
    def clean_registered_at(self):
        registered_at = self.cleaned_data.get('registered_at')
        if registered_at > timezone.now().date():  # Use Django's timezone.now()
            raise ValidationError("Registration date cannot be in the future.")
        return registered_at
    
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'role', 'phone']

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['role'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})


class CasualtyReportForm(forms.ModelForm):
    class Meta:
        model = CasualtyReport
        fields = ['name', 'report', 'amount']
    
    def __init__(self, *args, **kwargs):
        super(CasualtyReportForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['report'].widget.attrs.update({'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
