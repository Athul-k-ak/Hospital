from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from datetime import date
import uuid

from .forms import PatientForm, StaffForm, CasualtyReportForm
from .models import CasualtyReport, Consultation, Patient, Staff


# Dashboard View
def dashboard(request):
    return render(request, 'core/dashboard.html')

# Helper function to generate unique registration IDs
def generate_unique_reg_id():
    reg_id = str(uuid.uuid4())[:8]  # First 8 characters of UUID
    while Patient.objects.filter(reg_id=reg_id).exists():
        reg_id = str(uuid.uuid4())[:8]
    return reg_id

# ------------------- Registration Views ------------------- #

# Patient Registration View
def register_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.reg_id = generate_unique_reg_id()  # Unique registration ID

            # Check if patient is new or returning
            if Patient.objects.filter(name=patient.name).exists():
                existing_patient = Patient.objects.get(name=patient.name)
                existing_patient.paid_amount = 270  # Returning patient
                last_consultation = Consultation.objects.filter(patient=existing_patient).order_by('-date').first()
                existing_patient.last_visit = last_consultation.date if last_consultation else timezone.now().date()
                existing_patient.save()
            else:
                patient.paid_amount = 300  # New patient
                patient.save()

            # Create consultation for the registered patient
            Consultation.objects.create(
                patient=patient,
                paid_amount=patient.paid_amount,
                date=patient.registered_at
            )
            return redirect('patient_details', patient.reg_id)
    else:
        form = PatientForm()

    return render(request, 'core/register_patient.html', {'form': form})

# Register Staff View
def register_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StaffForm()

    return render(request, 'core/register_staff.html', {'form': form})

# Register Casualty View
def register_casualty(request):
    if request.method == 'POST':
        form = CasualtyReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('casualty_records')
    else:
        form = CasualtyReportForm()

    return render(request, 'core/register_casualty.html', {'form': form})

# ------------------- Dashboard and Consultation Views ------------------- #


# Consultation View
def consult_patient(request):
    if request.method == 'POST':
        reg_id = request.POST.get('reg_id')
        try:
            patient = Patient.objects.get(reg_id=reg_id)
            last_consultation = Consultation.objects.filter(patient=patient).order_by('-date').first()

            # Check if the last consultation was within 6 days
            if last_consultation and (timezone.now().date() - last_consultation.date).days <= 6:
                amount_paid = 0  # No payment if within 6 days
            else:
                amount_paid = 270  # Returning patient

            Consultation.objects.create(
                patient=patient,
                date=timezone.now().date(),
                time=timezone.now().time(),
                paid_amount=amount_paid
            )
            return redirect('consultation_records')
        except Patient.DoesNotExist:
            return HttpResponse("Patient with this Registration ID does not exist.", status=404)

    return render(request, 'core/consult_patient.html')

# Consultation Records View
def consultation_records(request):
    today = timezone.now().date()
    filter_date = request.GET.get('filter_date', today)

    consultations = Consultation.objects.filter(date=filter_date)
    total_cash_received = consultations.aggregate(Sum('paid_amount'))['paid_amount__sum']

    return render(request, 'core/consultation_records.html', {
        'paid_300_consultations': consultations.filter(paid_amount=300),
        'paid_270_consultations': consultations.filter(paid_amount=270),
        'visited_within_6_days_consultations': consultations.filter(paid_amount=0),
        'total_cash_received': total_cash_received,
        'filter_date': filter_date
    })

# ------------------- Records Views ------------------- #

# Patient Records View
def patient_records(request):
    patients = Patient.objects.all()
    return render(request, 'core/patient_records.html', {'patients': patients})

# Staff Records View
def staff_records(request):
    staff = Staff.objects.all()
    return render(request, 'core/staff_records.html', {'staff': staff})

# Casualty Records View
def casualty_records(request):
    today = timezone.now().date()
    filter_date = request.GET.get('filter_date', today)

    casualties = CasualtyReport.objects.filter(report_date=filter_date)
    
    return render(request, 'core/casualty_records.html', {
        'casualties': casualties,
        'filter_date': filter_date
    })

# ------------------- Detail Views ------------------- #

# Patient Details View
def patient_details(request, reg_id):
    patient = get_object_or_404(Patient, reg_id=reg_id)
    return render(request, 'core/patient_details.html', {'patient': patient})

# ------------------- Delete Views ------------------- #

# Delete Patient View
def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    return redirect('patient_records')

# Delete Consultation View
def delete_consultation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    consultation.delete()
    return redirect('consultation_records')

# Delete Casualty View
def delete_casualty(request, casualty_id):
    casualty = get_object_or_404(CasualtyReport, id=casualty_id)
    casualty.delete()
    return redirect('casualty_records')
