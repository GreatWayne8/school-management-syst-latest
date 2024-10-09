from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos import Point

class School(models.Model):
    name = models.CharField(max_length=100)
    location = geomodels.PointField(null=True, blank=True)  # Latitude/longitude, can be blank initially
    radius = models.FloatField(default=100)  # Radius in meters for geofencing

    def __str__(self):
        return self.name

    def is_within_geofence(self, user_location):
        """Check if the user's location is within the school's geofence radius."""
        if self.location:
            return self.location.distance(user_location) <= self.radius
        return False  # No geofence if location is not set

class Shift(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='shifts', null=True)  # Allow null for now

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    geom = geomodels.PointField()  # Stores latitude/longitude as geospatial data

    def __str__(self):
        return self.name

class ClockInOut(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_checkins', null=True, blank=True)  
    clock_in_time = models.DateTimeField(null=True, blank=True)
    clock_out_time = models.DateTimeField(null=True, blank=True)
    date = models.DateField(default=timezone.now)
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'date')  
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.user} - {self.date} {'by ' + str(self.teacher) if self.teacher else ''}"

    @property
    def is_clocked_in(self):
        return self.clock_in_time is not None and self.clock_out_time is None

    @property
    def is_clocked_out(self):
        return self.clock_out_time is not None

    @property
    def duration(self):
        if self.clock_in_time and self.clock_out_time:
            return self.clock_out_time - self.clock_in_time
        return None

    def clean(self):
        # Ensure clock-out is not before clock-in
        if self.clock_in_time and self.clock_out_time and self.clock_out_time < self.clock_in_time:
            raise ValidationError("Clock-out time cannot be earlier than clock-in time")

        # Get the teacher's current location (this should come from the front-end, e.g., GPS)
        user_location = Point(1.2345, 6.7890)  # Replace this with real GPS data from the user
        
        # Check if the user is attempting to clock in
        if self.clock_in_time:
            # Ensure that a school is associated with the ClockInOut instance
            if self.school:
                if not self.school.is_within_geofence(user_location):
                    raise ValidationError("You are outside the allowed geofence and cannot clock in.")

        super().clean()
