from django.utils import timezone
from .models import ClockInOut

def is_user_clocked_in(user):
    """Check if the user is currently clocked in."""
    today = timezone.now().date()
    return ClockInOut.objects.filter(user=user, date=today, clock_out_time__isnull=True).exists()
