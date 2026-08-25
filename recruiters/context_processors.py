from .models import RecruiterProfile
from students.models import Company, JobAnnouncementForm

def recruiter_context(request):
    """Provides active recruiter profile, company details & blinking roadmap notifications across all recruiter templates."""
    active_recruiter = None
    active_company = None

    if request.user.is_authenticated:
        if hasattr(request.user, 'recruiter_profile'):
            active_recruiter = request.user.recruiter_profile
            active_company = active_recruiter.company

    if not active_company and request.session.get('recruiter_company_id'):
        active_company = Company.objects.filter(id=request.session['recruiter_company_id']).first()

    pending_workflow_jafs = []
    pending_workflow_count = 0
    first_pending_jaf = None

    if active_company:
        unconfig = JobAnnouncementForm.objects.filter(company=active_company, is_workflow_configured=False).order_by('-created_at')
        pending_workflow_jafs = list(unconfig)
        pending_workflow_count = len(pending_workflow_jafs)
        if pending_workflow_count > 0:
            first_pending_jaf = pending_workflow_jafs[0]

    return {
        'active_recruiter': active_recruiter,
        'active_company': active_company,
        'pending_workflow_jafs': pending_workflow_jafs,
        'pending_workflow_count': pending_workflow_count,
        'first_pending_jaf': first_pending_jaf,
    }
