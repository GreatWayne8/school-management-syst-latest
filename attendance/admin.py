from django import forms
from django.contrib import admin
from django.contrib.gis.geos import Point
from .models import School, Shift, ClockInOut


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'

    latitude = forms.FloatField(required=False, label="Latitude")
    longitude = forms.FloatField(required=False, label="Longitude")

    def save(self, commit=True):
        instance = super().save(commit=False)
        lat = self.cleaned_data.get('latitude')
        lng = self.cleaned_data.get('longitude')
        if lat is not None and lng is not None:
            instance.location = Point(lng, lat)  # lng first, then lat
        if commit:
            instance.save()
        return instance

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    form = SchoolForm
    change_form_template = "admin/attendance/change_form.html"  # Points to your custom template
    list_display = ('name', 'location', 'radius')

    class Media:
        css = {
            'all': ('https://unpkg.com/leaflet/dist/leaflet.css',)
        }
        js = (
            'https://unpkg.com/leaflet/dist/leaflet.js',
            '/static/js/school_admin.js',  # Path to your custom JS for the map
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Pre-populate latitude and longitude if editing
        if obj and obj.location:
            form.base_fields['latitude'].initial = obj.location.y  # Latitude
            form.base_fields['longitude'].initial = obj.location.x  # Longitude
        return form
        
@admin.register(ClockInOut)
class ClockInOutAdmin(admin.ModelAdmin):
    list_display = ('user', 'clock_in_time', 'clock_out_time', 'date')
    list_filter = ('date',)
    search_fields = ('user__username',)
