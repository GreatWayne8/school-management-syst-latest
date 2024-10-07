# medicals/views.py

from django.shortcuts import render, redirect,get_object_or_404
from .forms import MedicalRecordForm 
from .models import MedicalRecord
from django.contrib import messages

def add_medical_record(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('medicals:medical_record_list')  # Redirect to the list of medical records
    else:
        form = MedicalRecordForm(user=request.user)

    return render(request, 'medicals/add_medical_record.html', {'form': form})

def medical_record_list(request):
    if request.user.is_superuser:
        medical_records = MedicalRecord.objects.all()
    elif request.user.is_teacher:
        medical_records = MedicalRecord.objects.filter(student__teacher__user=request.user)
    elif request.user.is_parent:
        medical_records = MedicalRecord.objects.filter(student__parents__user=request.user)
    else:
        medical_records = MedicalRecord.objects.none()  # No access for other roles

    return render(request, 'medicals/medical_record_list.html', {'medical_records': medical_records})

def update_medical_record(request, id):
    record = get_object_or_404(MedicalRecord, id=id)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=record, user=request.user)  # Pass the user
        if form.is_valid():
            form.save()
            return redirect('medicals:medical_record_list')  # Redirect to the list after updating
    else:
        form = MedicalRecordForm(instance=record, user=request.user)  # Pass the user

    return render(request, 'medicals/update_medical_record.html', {'form': form, 'record': record})

def delete_medical_record(request, id):
    record = get_object_or_404(MedicalRecord, id=id)
    if request.method == 'POST':
        record.delete()
        return redirect('medicals:medical_record_list')  # Redirect to the list after deletion
    return render(request, 'medicals/confirm_delete.html', {'record': record})