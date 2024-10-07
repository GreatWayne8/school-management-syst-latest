from django.urls import path
from . import views

from .views import (
    bus_list, bus_detail, create_bus,
    route_list, route_detail, create_route,
    student_pickup_list, student_pickup_detail, create_student_pickup, approve_transport_request
)

app_name = 'transportation' 
urlpatterns = [
    # Bus URLs
    path('buses/', bus_list, name='bus_list'),
    path('buses/<int:pk>/', bus_detail, name='bus_detail'),
    path('buses/create/', create_bus, name='create_bus'),
    
    # Route URLs
    path('routes/', route_list, name='route_list'),
    path('routes/<int:pk>/', route_detail, name='route_detail'),
    path('routes/create/', create_route, name='create_route'),
    
    # Student Pickup URLs
    path('student-pickups/', student_pickup_list, name='student_pickup_list'),
    path('student-pickups/<int:pk>/', student_pickup_detail, name='student_pickup_detail'),
    path('student-pickups/create/', create_student_pickup, name='create_student_pickup'),

    # Transport Request URLs
    path('transport/create/', views.create_transport_request, name='create_transport_request'),
    path('transport/list/', views.transport_list, name='transport_list'),
    path('transport/approve/<int:pk>/', approve_transport_request, name='approve_transport_request'),
]
