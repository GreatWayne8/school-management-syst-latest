from django.contrib import admin
from .models import Route, Bus, StudentPickup, TransportRequest
from django.contrib import messages
from messaging.models import Message  # Import your Message model

# Customizing the Route Admin
@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('route_name', 'start_location', 'end_location')
    search_fields = ('route_name', 'start_location', 'end_location')
    list_filter = ('start_location', 'end_location')

# Customizing the Bus Admin
@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'route', 'driver', 'capacity')
    search_fields = ('bus_number', 'driver__username')
    list_filter = ('route', 'driver')
    filter_horizontal = ('teachers',)  # For ManyToManyField

# Customizing the StudentPickup Admin
@admin.register(StudentPickup)
class StudentPickupAdmin(admin.ModelAdmin):
    list_display = ('student', 'pickup_location', 'dropoff_location', 'route', 'bus')
    search_fields = ('student__user__username', 'route__route_name', 'bus__bus_number')
    list_filter = ('route', 'bus')

# Customizing the TransportRequest Admin
# In transportation/admin.py

from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from messaging.models import Message  # Import your Message model
from .models import Route, Bus, StudentPickup, TransportRequest

@admin.register(TransportRequest)
class TransportRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'transport_type', 'status', 'pickup_time', 'dropoff_time', 'approved')
    search_fields = ('student__user__username', 'pickup_location', 'dropoff_location')
    list_filter = ('status', 'transport_type', 'approved')  # Include 'approved' in filters
    actions = ['approve_requests']  # Add action for bulk approval

    def approve_requests(self, request, queryset):
        for transport_request in queryset:
            transport_request.approved = True
            transport_request.save()
            # Send a message to the student
            Message.objects.create(
                sender=request.user,
                recipient=transport_request.student.user,
                content=f"Your transport request for {transport_request.transport_type} has been approved!",
                timestamp=timezone.now()  # Ensure you have a timestamp field in your Message model
            )
        self.message_user(request, "Selected requests have been approved and notifications sent to students.")
    approve_requests.short_description = "Approve selected transport requests"
