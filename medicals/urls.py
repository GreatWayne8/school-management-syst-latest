# urls.py
from django.urls import path
from .views import add_medical_record, medical_record_list,update_medical_record,delete_medical_record

app_name = 'medicals'

urlpatterns = [
    path('add/', add_medical_record, name='add_medical_record'),
    path('', medical_record_list, name='medical_record_list'),
    path('update/<int:id>/', update_medical_record, name='update_medical_record'),
    path('delete/<int:id>/', delete_medical_record, name='delete_medical_record'),


]
