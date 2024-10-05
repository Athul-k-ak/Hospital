from django.http import HttpResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import uuid
from django.db.models import Sum

from .forms import PatientForm, StaffForm, CasualtyReportForm
from .models import CasualtyReport, Consultation, Patient, Staff

from datetime import date

def dashboard(request):
    context = {}
    return render(request, 'core/dashboard.html', context)

def patient_records(request):
    patients = Patient.objects.all()
    return render(request, 'core/patient_records.html', {'patients': patients})

def generate_unique_reg_id():
    reg_id = str(uuid.uuid4())[:8]  # Using only the first 8 characters for brevity
    while Patient.objects.filter(reg_id=reg_id).exists():
        reg_id = str(uuid.uuid4())[:8]
    return reg_id



def register_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.reg_id = generate_unique_reg_id()

            # Set the paid amount based on patient status
            if Patient.objects.filter(name=patient.name).exists():
                patient.paid_amount = 270  # Returning patient
            else:
                patient.paid_amount = 300  # New patient

            # Set the registration date and time
            patient.registered_at = timezone.datetime.combine(
                form.cleaned_data['date'],  # Use the date from the form
                timezone.now().time()  # Use the current time
            )

            patient.save()

            # Create a consultation record for this patient
            Consultation.objects.create(
                patient=patient,
                date=form.cleaned_data['date'],  # Use the date from the form
                time=timezone.now().time(),      # Use the current time
                paid_amount=patient.paid_amount
            )

            return redirect('patient_details', patient.reg_id)
    else:
        form = PatientForm()

    return render(request, 'core/register_patient.html', {'form': form})

def patient_details(request, reg_id):
    patient = get_object_or_404(Patient, reg_id=reg_id)
    return render(request, 'core/patient_details.html', {'patient': patient})

def register_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StaffForm()
    return render(request, 'core/register_staff.html', {'form': form})

def register_casualty(request):
    if request.method == 'POST':
        form = CasualtyReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CasualtyReportForm()
    return render(request, 'core/register_casualty.html', {'form': form})

def consultation_records(request):
    today = date.today()
    filter_date = request.GET.get('filter_date')
    
    if filter_date:
        consultations = Consultation.objects.filter(date=filter_date)
    else:
        consultations = Consultation.objects.filter(date=today)

    paid_300_consultations = consultations.filter(paid_amount=300)
    paid_270_consultations = consultations.filter(paid_amount=270)
    visited_within_6_days_consultations = consultations.filter(paid_amount=0)

    total_cash_received = (
        (paid_300_consultations.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0) +
        (paid_270_consultations.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0) +
        (visited_within_6_days_consultations.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0)
    )

    context = {
        'paid_300_consultations': paid_300_consultations,
        'paid_270_consultations': paid_270_consultations,
        'visited_within_6_days_consultations': visited_within_6_days_consultations,
        'total_cash_received': total_cash_received,
        'filter_date': filter_date,
        'today': today
    }

    return render(request, 'core/consultation_records.html', context)

def delete_consultation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    consultation.delete()
    return redirect('consultation_records')

# views.py


paid_270_count = 0
visited_within_6_days_count = 0

def consult_patient(request):
    # Declare global counters if needed
    global paid_270_count, visited_within_6_days_count

    if request.method == 'POST':
        reg_id = request.POST.get('reg_id')
        try:
            patient = Patient.objects.get(reg_id=reg_id)
            # For returning patients
            last_consultation = Consultation.objects.filter(patient=patient).order_by('-date').first()

            if last_consultation:
                # Combine last consultation date and time to create a timezone-aware datetime
                last_consultation_datetime = timezone.make_aware(
                    timezone.datetime.combine(last_consultation.date, last_consultation.time)
                )
                
                if (timezone.now() - last_consultation_datetime).days <= 6:
                    amount_paid = 0
                    visited_within_6_days_count += 1  # Increment the visit within 6 days counter
                else:
                    amount_paid = 270
                    paid_270_count += 1  # Increment the ₹270 counter
            else:
                # First consultation, consider it a new patient
                amount_paid = 300

            # Create a new consultation record
            Consultation.objects.create(patient=patient, paid_amount=amount_paid)

            return redirect('consultation_records')
        except Patient.DoesNotExist:
            return HttpResponse("Patient with this Registration ID does not exist.", status=404)
    
    return render(request, 'core/consult_patient.html')

def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    return redirect('patient_records')


def staff_records(request):
    staff = Staff.objects.all()
    return render(request, 'core/staff_records.html', {'staff': staff})

def casualty_records(request):
    casualties = CasualtyReport.objects.all()
    return render(request, 'core/casualty_records.html', {'casualties': casualties})