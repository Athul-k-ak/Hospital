from django import forms
from .models import Patient, Staff, CasualtyReport

class PatientForm(forms.ModelForm):
    # Date field to capture the registration date
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)

    class Meta:
        model = Patient
        fields = ['name', 'place', 'age', 'phone', 'gender', 'date']

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'role', 'phone']

class CasualtyReportForm(forms.ModelForm):
    class Meta:
        model = CasualtyReport
        fields = ['report']
