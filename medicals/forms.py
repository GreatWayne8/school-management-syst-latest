from django import forms
from .models import MedicalRecord
from accounts.models import Student

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = [
            'student',
            'record_date',
            'condition',
            'treatment',
            'notes',
            'doctor',
            'doctors_phone_number',
            'hospital',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Get the current user
        super().__init__(*args, **kwargs)

        # Filter students based on the user's role
        if user.is_superuser:  # Admin role
            self.fields['student'].queryset = Student.objects.all()  # Admin sees all students
        elif user.is_teacher:  # Teacher role
            self.fields['student'].queryset = Student.objects.filter(teacher__user=user)  # Teacher sees only their students
        elif user.is_parent:  # Parent role
            # Assuming there's a reverse relation from Student to Parent
            self.fields['student'].queryset = Student.objects.filter(parents__user=user)  # Parent sees their own children
        else:
            # Optionally, you can raise an error or set queryset to an empty list for unauthorized roles
            self.fields['student'].queryset = Student.objects.none()  # No access for other roles
