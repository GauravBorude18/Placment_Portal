from .models import StudentProfile, StudentEmailNotification

def student_notification_context(request):
    """Provides real-time official emails & notifications across the entire portal with strict role isolation."""
    # STRICT ROLE SANITY CHECK: If user is logged in as Recruiter or TPO, NEVER load student notifications
    if request.session.get('active_role') in ['recruiter', 'tpo'] or request.session.get('tpo_logged_in') or request.session.get('recruiter_company_id'):
        return {
            'student_notifications': [],
            'unread_notifications_count': 0,
            'unread_count': 0,
        }

    student = None
    if request.user.is_authenticated and hasattr(request.user, 'student_profile') and request.session.get('active_role') == 'student':
        student = request.user.student_profile
    elif request.session.get('active_student_id') and request.session.get('active_role') == 'student':
        student = StudentProfile.objects.filter(id=request.session.get('active_student_id')).first()

    if student:
        notifications = StudentEmailNotification.objects.filter(student=student).select_related('company', 'jaf')[:15]
        unread_count = StudentEmailNotification.objects.filter(student=student, is_read=False).count()
    else:
        notifications = []
        unread_count = 0

    return {
        'student_notifications': notifications,
        'unread_notifications_count': unread_count,
        'unread_count': unread_count,
    }
