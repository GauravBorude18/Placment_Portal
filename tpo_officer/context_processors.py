from .models import TPOProfile
from django.contrib.auth.models import User
from recruiters.models import RecruiterProfile
from students.models import StudentProfile

def tpo_context(request):
    """Provides active TPO profile data & real-time governance notification counts across all TPO pages."""
    tpo = TPOProfile.objects.filter(is_active_head=True).first()
    if not tpo:
        user = User.objects.filter(username__in=['tpo', 'admin']).first()
        if not user:
            user = User.objects.create_superuser('tpo', 'tpo@a2zplacement.edu', 'tpo123')
        tpo = TPOProfile.objects.create(
            user=user,
            full_name="Prof. S. Bhattacharya",
            designation="Head, Training & Placement Cell",
            department="Computer Science & Engineering",
            official_email="tpo@a2zplacement.edu",
            phone="+91 98220 12345",
            office_location="Room 101, Main Admin Block, A2Z Campus",
            signing_authority_title="Head, Placement Cell & DPC In-Charge",
            is_active_head=True
        )

    try:
        pending_recruiters = list(RecruiterProfile.objects.filter(status='PENDING').order_by('-created_at')[:10])
        pending_recruiters_count = RecruiterProfile.objects.filter(status='PENDING').count()
    except Exception:
        pending_recruiters = []
        pending_recruiters_count = 0

    try:
        unverified_students_count = StudentProfile.objects.filter(verification_status='PENDING').count()
    except Exception:
        unverified_students_count = 0

    tpo_notif_count = pending_recruiters_count + unverified_students_count

    return {
        'active_tpo': tpo,
        'tpo_pending_recruiters': pending_recruiters,
        'tpo_pending_recruiters_count': pending_recruiters_count,
        'tpo_unverified_students_count': unverified_students_count,
        'tpo_notif_count': tpo_notif_count,
    }
