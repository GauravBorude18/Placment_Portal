from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from students.models import StudentProfile, JobAnnouncementForm, Application, Company, StudentEmailNotification
from .models import TPOProfile, LeadershipMember

from functools import wraps

def is_tpo_authenticated(request):
    """Check if the user is authenticated with TPO privileges."""
    if request.session.get('tpo_logged_in') and request.session.get('active_role') == 'tpo':
        return True
    if not request.user.is_authenticated:
        return False
    # A regular student profile can NEVER access TPO Control Room without staff privileges
    if hasattr(request.user, 'student_profile') and not (request.user.is_staff or request.user.is_superuser):
        return False
    if request.user.is_staff or request.user.is_superuser or hasattr(request.user, 'tpo_profile') or request.user.username in ['admin', 'tpo', 'tpo_head', 'tpo_sharma']:
        return True
    return False

def set_tpo_session(request):
    """Sets TPO session flags."""
    request.session['tpo_logged_in'] = True
    request.session['active_role'] = 'tpo'

def require_tpo_login(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not is_tpo_authenticated(request):
            return redirect(f"/login/?role=admin&next={request.path}")
        set_tpo_session(request)
        return view_func(request, *args, **kwargs)
    return _wrapped

def get_active_tpo():
    """Retrieve or create default active TPO Profile."""
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
    return tpo

# Star achievements for the Live Season 2026-27 (Class of 2027)
STAR_PLACED_STUDENTS_2026_27 = [
    {
        'name': 'Aarav Sharma',
        'roll': '220050042',
        'dept': 'Computer Science & Engg',
        'company': 'Optiver Amsterdam',
        'company_logo': 'https://logo.clearbit.com/optiver.com',
        'company_fallback': 'OPT',
        'role': 'Quantitative Research Analyst',
        'ctc': '₹1.68 Cr',
        'ctc_badge': '2026-27 • International Highest CTC',
        'tier': 'Super Dream'
    },
    {
        'name': 'Gaurav Borude',
        'roll': '223344551',
        'dept': 'Data Science & AI',
        'company': 'Tower Research Capital',
        'company_logo': 'https://logo.clearbit.com/tower-research.com',
        'company_fallback': 'TRC',
        'role': 'Algorithmic High-Frequency Trader',
        'ctc': '₹55.0 LPA',
        'ctc_badge': '2026-27 • Domestic Top Quant Offer',
        'tier': 'Super Dream'
    },
    {
        'name': 'Priya Nair',
        'roll': '220050089',
        'dept': 'Computer Science & Engg',
        'company': 'Google India',
        'company_logo': 'https://logo.clearbit.com/google.com',
        'company_fallback': 'GOOG',
        'role': 'Software Development Engineer III',
        'ctc': '₹45.0 LPA',
        'ctc_badge': '2026-27 • Big Tech Core',
        'tier': 'Super Dream'
    },
    {
        'name': 'Rohan Deshmukh',
        'roll': '220040012',
        'dept': 'Electronics & Comm (ECE)',
        'company': 'Microsoft Redmond',
        'company_logo': 'https://logo.clearbit.com/microsoft.com',
        'company_fallback': 'MSFT',
        'role': 'Silicon Hardware Design Engineer',
        'ctc': '₹42.5 LPA',
        'ctc_badge': '2026-27 • Silicon Systems',
        'tier': 'Super Dream'
    },
    {
        'name': 'Ananya Iyer',
        'roll': '220030045',
        'dept': 'Mechanical Engineering',
        'company': 'Tesla Motors',
        'company_logo': 'https://logo.clearbit.com/tesla.com',
        'company_fallback': 'TSLA',
        'role': 'Robotics & Autonomous Systems Lead',
        'ctc': '₹38.0 LPA',
        'ctc_badge': '2026-27 • Robotics & EV',
        'tier': 'Dream'
    },
    {
        'name': 'Vikramaditya Patil',
        'roll': '220020018',
        'dept': 'Civil & Infrastructure',
        'company': 'L&T ECC Projects',
        'company_logo': 'https://logo.clearbit.com/larsentoubro.com',
        'company_fallback': 'L&T',
        'role': 'Smart Infrastructure Design Specialist',
        'ctc': '₹24.0 LPA',
        'ctc_badge': '2026-27 • Core Infrastructure',
        'tier': 'Dream'
    }
]

DEPARTMENT_HIRING_DATA_2026_27 = [
    {
        'name': 'Computer Science & Engg (CSE)',
        'code': 'CSE',
        'enrolled': 120,
        'placed': 118,
        'rate': 98.3,
        'avg_ctc': '₹28.4 LPA',
        'highest_ctc': '₹1.68 Cr',
        'top_recruiters': 'Optiver, Google, Uber, Apple',
        'icon': '💻'
    },
    {
        'name': 'Data Science & Artificial Intelligence',
        'code': 'DSAI',
        'enrolled': 60,
        'placed': 59,
        'rate': 98.3,
        'avg_ctc': '₹26.2 LPA',
        'highest_ctc': '₹1.20 Cr',
        'top_recruiters': 'Tower Research, Jane Street, Amazon',
        'icon': '🤖'
    },
    {
        'name': 'Electrical & Electronics (ECE)',
        'code': 'ECE',
        'enrolled': 95,
        'placed': 90,
        'rate': 94.7,
        'avg_ctc': '₹21.5 LPA',
        'highest_ctc': '₹55.0 LPA',
        'top_recruiters': 'Microsoft, Qualcomm, NVIDIA, Intel',
        'icon': '⚡'
    },
    {
        'name': 'Mechanical Engineering',
        'code': 'MECH',
        'enrolled': 85,
        'placed': 78,
        'rate': 91.8,
        'avg_ctc': '₹15.8 LPA',
        'highest_ctc': '₹38.0 LPA',
        'top_recruiters': 'Tesla, Mercedes-Benz, Tata Motors, ISRO',
        'icon': '⚙️'
    },
    {
        'name': 'Civil & Infrastructure Engineering',
        'code': 'CIVIL',
        'enrolled': 60,
        'placed': 52,
        'rate': 86.7,
        'avg_ctc': '₹12.4 LPA',
        'highest_ctc': '₹24.0 LPA',
        'top_recruiters': 'Larsen & Toubro, Tata Projects, Mott MacDonald',
        'icon': '🏗️'
    },
]

# Comprehensive Multi-Year Matrix with 2025-26 Completed Benchmark & 2026-27 Live
HISTORICAL_YEARLY_DATA = [
    {
        'year': '2022-23',
        'batch': 'Class of 2023',
        'enrolled': 310,
        'placed': 285,
        'rate': 91.9,
        'avg_ctc': 17.5,
        'median_ctc': 15.0,
        'highest_ctc': 95.0,
        'highest_display': '₹95.0 LPA',
        'avg_display': '₹17.5 LPA',
        'median_display': '₹15.0 LPA',
        'total_offers': 310,
        'top_recruiters': 'Google, Qualcomm, Morgan Stanley, Adobe'
    },
    {
        'year': '2023-24',
        'batch': 'Class of 2024',
        'enrolled': 330,
        'placed': 310,
        'rate': 93.9,
        'avg_ctc': 19.8,
        'median_ctc': 17.5,
        'highest_ctc': 110.0,
        'highest_display': '₹1.10 Cr',
        'avg_display': '₹19.8 LPA',
        'median_display': '₹17.5 LPA',
        'total_offers': 345,
        'top_recruiters': 'Microsoft, Tower Research, Apple, DE Shaw'
    },
    {
        'year': '2024-25',
        'batch': 'Class of 2025',
        'enrolled': 360,
        'placed': 345,
        'rate': 95.8,
        'avg_ctc': 22.4,
        'median_ctc': 19.5,
        'highest_ctc': 145.0,
        'highest_display': '₹1.45 Cr',
        'avg_display': '₹22.4 LPA',
        'median_display': '₹19.5 LPA',
        'total_offers': 380,
        'top_recruiters': 'Jane Street, Uber, NVIDIA, Oracle, Goldman Sachs'
    },
    {
        'year': '2025-26',
        'batch': 'Class of 2026 (Previous Benchmark)',
        'enrolled': 380,
        'placed': 372,
        'rate': 97.9,
        'avg_ctc': 24.6,
        'median_ctc': 21.0,
        'highest_ctc': 158.0,
        'highest_display': '₹1.58 Cr',
        'avg_display': '₹24.6 LPA',
        'median_display': '₹21.0 LPA',
        'total_offers': 410,
        'top_recruiters': 'Sprinklr, Amazon, Google, Goldman Sachs, Tesla',
        'is_previous_season': True
    },
    {
        'year': '2026-27',
        'batch': 'Class of 2027 (Live Ongoing)',
        'enrolled': 400,
        'placed': 395,
        'rate': 98.8,
        'avg_ctc': 26.8,
        'median_ctc': 23.5,
        'highest_ctc': 168.0,
        'highest_display': '₹1.68 Cr',
        'avg_display': '₹26.8 LPA',
        'median_display': '₹23.5 LPA',
        'total_offers': 435,
        'top_recruiters': 'Optiver Amsterdam, Google India, Tesla, Tower Research',
        'is_current_live': True
    }
]

# Detailed previous season 2025-26 performance report
PREVIOUS_SEASON_2025_26_DATA = {
    'season': '2025-26 (Concluded Benchmark)',
    'total_enrolled': 380,
    'total_placed': 372,
    'placement_rate': 97.9,
    'total_offers': 410,
    'highest_package': '₹1.58 Cr',
    'avg_package': '₹24.6 LPA',
    'median_package': '₹21.0 LPA',
    'companies_visited': 84,
    'top_recruiters': ['Sprinklr', 'Amazon', 'Google India', 'Goldman Sachs', 'Tesla', 'Microsoft'],
    'super_dream_offers': 178,
    'dream_offers': 142,
    'core_offers': 90
}

LIVE_PIPELINE_SCHEDULES_2026_27 = [
    {
        'company': 'Google India',
        'logo': 'https://logo.clearbit.com/google.com',
        'fallback': 'GOOG',
        'role': 'Software Engineer III (SDE-III)',
        'ctc': '₹45.0 LPA',
        'stage': 'ONLINE_TEST',
        'stage_label': 'HackerRank Online Coding Assessment Live',
        'stage_badge': '24 Candidates Attempting',
        'status_color': '#3b82f6',
        'slot': 'Day 1 • Slot 1',
        'time': 'Today, 06:00 PM IST'
    },
    {
        'company': 'Optiver Amsterdam',
        'logo': 'https://logo.clearbit.com/optiver.com',
        'fallback': 'OPT',
        'role': 'Quantitative Research Analyst',
        'ctc': '₹1.68 Cr',
        'stage': 'INTERVIEW',
        'stage_label': 'Technical Quant Interview Panel (Round 2)',
        'stage_badge': '18 Shortlisted',
        'status_color': '#f59e0b',
        'slot': 'Day 1 • Slot 2',
        'time': 'Tomorrow, 10:30 AM IST'
    },
    {
        'company': 'Tesla Motors',
        'logo': 'https://logo.clearbit.com/tesla.com',
        'fallback': 'TSLA',
        'role': 'Robotics & Automation Lead',
        'ctc': '₹38.0 LPA',
        'stage': 'INTERVIEW',
        'stage_label': 'Hardware Architecture & System Design',
        'stage_badge': '12 Shortlisted',
        'status_color': '#8b5cf6',
        'slot': 'Day 2 • Slot 1',
        'time': 'Aug 20, 02:00 PM IST'
    },
    {
        'company': 'Tower Research Capital',
        'logo': 'https://logo.clearbit.com/tower-research.com',
        'fallback': 'TRC',
        'role': 'Algorithmic High-Frequency Trader',
        'ctc': '₹55.0 LPA',
        'stage': 'OFFERED',
        'stage_label': 'Final Offer Rollout & Sign-off',
        'stage_badge': '8 Offers Extended',
        'status_color': '#10b981',
        'slot': 'Day 1 • Slot 1',
        'time': 'Dispatched via Official Mail'
    }
]

@ensure_csrf_cookie
@require_tpo_login
def tpo_dashboard(request):
    """
    Grand Master Control Room for Placement Cell Head (TPO):
    - Live Placement Season: 2026-27 (Phase 1)
    - Star Placed Candidates & Highest CTC Packages Breakdown (2026-27)
    - Department-Wise Placement & Hiring Velocity (2026-27)
    - Live Pipeline Drives & Interview Schedules (2026-27)
    - Corporate JAF Drives & Recruiter Activity Pulse
    """
    
    # Run auto-release check for on-hold students
    for st in StudentProfile.objects.filter(verification_status='ON_HOLD'):
        st.check_and_release_hold()

    total_students = StudentProfile.objects.count()
    pending_students = StudentProfile.objects.filter(verification_status='PENDING').count()
    approved_students = StudentProfile.objects.filter(verification_status='APPROVED').count()
    on_hold_students = StudentProfile.objects.filter(verification_status='ON_HOLD').count()
    declined_students = StudentProfile.objects.filter(verification_status='DECLINED').count()
    
    total_jafs = JobAnnouncementForm.objects.count()
    pending_jafs = JobAnnouncementForm.objects.filter(approval_status='PENDING').count()
    approved_jafs = JobAnnouncementForm.objects.filter(approval_status='APPROVED').count()
    total_companies = Company.objects.count()

    total_applications = Application.objects.count()
    total_offers = Application.objects.filter(status='OFFERED').count()
    total_interviews = Application.objects.filter(status='INTERVIEW').count()
    total_shortlisted = Application.objects.filter(status='SHORTLISTED').count()
    
    recent_pending = StudentProfile.objects.filter(verification_status='PENDING')[:6]
    recent_jafs = JobAnnouncementForm.objects.select_related('company').all().order_by('-created_at')[:5]

    return render(request, 'tpo_officer/dashboard.html', {
        'current_season': '2026-27',
        'current_batch': 'Class of 2027',
        'total_students': total_students,
        'pending_students': pending_students,
        'approved_students': approved_students,
        'on_hold_students': on_hold_students,
        'declined_students': declined_students,
        'total_jafs': total_jafs,
        'pending_jafs': pending_jafs,
        'approved_jafs': approved_jafs,
        'total_companies': total_companies,
        'total_applications': total_applications,
        'total_offers': total_offers,
        'total_interviews': total_interviews,
        'total_shortlisted': total_shortlisted,
        'recent_pending': recent_pending,
        'recent_jafs': recent_jafs,
        'star_placed_students': STAR_PLACED_STUDENTS_2026_27,
        'department_hiring_data': DEPARTMENT_HIRING_DATA_2026_27,
        'live_pipeline_schedules': LIVE_PIPELINE_SCHEDULES_2026_27,
        'leadership_members': LeadershipMember.objects.all().order_by('order'),
        'active_tab': 'tpo_dashboard'
    })

@ensure_csrf_cookie
@require_tpo_login
def verify_students(request):
    """TPO student verification view to approve, decline, or place on temporary hold with auto-expiry."""
    for st in StudentProfile.objects.filter(verification_status='ON_HOLD'):
        st.check_and_release_hold()

    # Only show candidates who have filled out their profile information
    completed_ids = [st.id for st in StudentProfile.objects.all() if st.is_profile_completed]

    pending_list = StudentProfile.objects.filter(id__in=completed_ids, verification_status='PENDING')
    approved_list = StudentProfile.objects.filter(id__in=completed_ids, verification_status='APPROVED')
    on_hold_list = StudentProfile.objects.filter(id__in=completed_ids, verification_status='ON_HOLD')
    declined_list = StudentProfile.objects.filter(id__in=completed_ids, verification_status='DECLINED')

    return render(request, 'tpo_officer/verify_students.html', {
        'pending_list': pending_list,
        'approved_list': approved_list,
        'on_hold_list': on_hold_list,
        'declined_list': declined_list,
        'active_tab': 'verify_students'
    })

def approve_single_student(request, student_id):
    """1-Click Approval action for TPO to sign-off a student profile."""
    student = get_object_or_404(StudentProfile, id=student_id)
    student.is_dpc_verified = True
    student.verification_status = 'APPROVED'
    student.approved_by = 'Prof. S. Bhattacharya (Head, Placement Cell)'
    student.verification_remarks = "All academic credentials and Master Resumes officially verified."
    student.hold_until = None
    student.hold_days = 0
    student.save()

    # Dispatch In-App & Email Notification to Student
    StudentEmailNotification.objects.create(
        student=student,
        notification_type='OTP',
        subject="✓ Official Sign-Off: Placement Registration Approved",
        recipient_email=student.user.email,
        headline="Placement Registration Officially Approved",
        body_content=f"Congratulations {student.full_name}! Prof. S. Bhattacharya (Head, Placement Cell) has officially verified and approved your academic credentials (CPI: {student.cgpa}) and Master Resumes. You now have active access to apply for all eligible company JAFs.",
        action_url="/student_dashboard/",
        action_label="Explore JAF Openings →",
        is_read=False
    )
    return redirect('tpo_officer:verify_students')

def decline_single_student(request, student_id):
    """Action for TPO to decline a student's profile with reason."""
    student = get_object_or_404(StudentProfile, id=student_id)
    reason = request.POST.get('reason', request.GET.get('reason', 'Verification rejected due to incomplete academic records.'))
    student.is_dpc_verified = False
    student.verification_status = 'DECLINED'
    student.verification_remarks = reason
    student.hold_until = None
    student.hold_days = 0
    student.save()

    # Dispatch In-App & Email Notification to Student
    StudentEmailNotification.objects.create(
        student=student,
        notification_type='REJECTED',
        subject="⚠️ Notice: Registration Verification Declined by Placement Cell",
        recipient_email=student.user.email,
        headline="Academic Records Action Required",
        body_content=f"Your placement registration has been declined by Prof. S. Bhattacharya. Reason / Feedback: \"{reason}\". Please update your academic details or contact the placement desk.",
        action_url="/profile/edit/",
        action_label="Update Profile Records →",
        is_read=False
    )
    return redirect('tpo_officer:verify_students')

def hold_single_student(request, student_id):
    """Places candidate on temporary hold for N days with auto-expiry."""
    student = get_object_or_404(StudentProfile, id=student_id)
    days = int(request.POST.get('days', request.GET.get('days', 3)))
    reason = request.POST.get('reason', request.GET.get('reason', f'Candidate placed on temporary hold for {days} days pending clarification.'))
    
    student.is_dpc_verified = False
    student.verification_status = 'ON_HOLD'
    student.hold_days = days
    student.hold_until = timezone.now() + timedelta(days=days)
    student.verification_remarks = reason
    student.save()

    # Dispatch In-App & Email Notification to Student
    StudentEmailNotification.objects.create(
        student=student,
        notification_type='OTP',
        subject=f"⏸️ Important: Placement Registration Placed on Hold for {days} Days",
        recipient_email=student.user.email,
        headline=f"Temporary Verification Hold Active ({days} Days)",
        body_content=f"Prof. S. Bhattacharya (Head, TPO & Placement Cell) has temporarily placed your profile on hold for {days} days. Reason / Remarks: \"{reason}\". Your profile will automatically be unlocked on {student.hold_until.strftime('%b %d, %Y, %I:%M %p')}.",
        action_url="/notifications/",
        action_label="View Hold Details →",
        is_read=False
    )
    return redirect('tpo_officer:verify_students')

def unhold_single_student(request, student_id):
    """Manual action to release hold and approve candidate immediately."""
    student = get_object_or_404(StudentProfile, id=student_id)
    student.is_dpc_verified = True
    student.verification_status = 'APPROVED'
    student.verification_remarks = f"Manual hold released by TPO on {timezone.now().strftime('%b %d, %Y')}."
    student.hold_until = None
    student.hold_days = 0
    student.save()

    # Dispatch In-App & Email Notification to Student
    StudentEmailNotification.objects.create(
        student=student,
        notification_type='OTP',
        subject="✓ Notice: Temporary Hold Released & Profile Approved",
        recipient_email=student.user.email,
        headline="Temporary Hold Lifted by Placement Head",
        body_content=f"Your temporary hold has been officially released by Prof. S. Bhattacharya. Your student placement status is now active and approved.",
        action_url="/student_dashboard/",
        action_label="Go to Dashboard →",
        is_read=False
    )
    return redirect('tpo_officer:verify_students')

def all_jafs_view(request):
    """TPO oversight of all published, pending, and approved Job Announcement Forms (JAFs)."""
    set_tpo_session(request)
    pending_jafs = JobAnnouncementForm.objects.filter(approval_status='PENDING').select_related('company').order_by('-created_at')
    approved_jafs = JobAnnouncementForm.objects.filter(approval_status='APPROVED').select_related('company').order_by('-created_at')
    
    return render(request, 'tpo_officer/jafs.html', {
        'pending_jafs': pending_jafs,
        'approved_jafs': approved_jafs,
        'total_jafs': pending_jafs.count() + approved_jafs.count(),
        'active_tab': 'all_jafs'
    })

def approve_jaf(request, jaf_id):
    """TPO approval action to make a company's JAF live and accessible to students."""
    set_tpo_session(request)
    jaf = get_object_or_404(JobAnnouncementForm, id=jaf_id)
    jaf.approval_status = 'APPROVED'
    jaf.is_active = True
    jaf.save()
    return redirect('tpo_officer:all_jafs')

def reject_jaf(request, jaf_id):
    """TPO rejection action for a company JAF."""
    set_tpo_session(request)
    jaf = get_object_or_404(JobAnnouncementForm, id=jaf_id)
    jaf.approval_status = 'REJECTED'
    jaf.is_active = False
    jaf.save()
    return redirect('tpo_officer:all_jafs')

def jaf_applicants_view(request, jaf_id):
    """
    Dedicated TPO View for Drive Applicants & Funnel Inspection:
    Inspect candidate credentials, eligibility status, recruitment stage, and DPC verification.
    """
    set_tpo_session(request)
    jaf = get_object_or_404(JobAnnouncementForm.objects.select_related('company'), id=jaf_id)
    applications = Application.objects.filter(jaf=jaf).select_related('student', 'student__user').order_by('-applied_at')
    
    applicant_data = []
    for app in applications:
        is_eligible, reasons = jaf.check_student_eligibility(app.student)
        resume_name = app.resume_used or app.student.resume_sde_name or app.student.resume_quant_name or f"{app.student.full_name.replace(' ', '_')}_Master_Resume.pdf"
        resume_file_url = app.student.resume_sde_file.url if app.student.resume_sde_file else None

        applicant_data.append({
            'application': app,
            'student': app.student,
            'is_eligible': is_eligible,
            'eligibility_reasons': reasons,
            'resume_name': resume_name,
            'resume_file_url': resume_file_url,
            'status': app.status,
            'applied_at': app.applied_at
        })
    
    total_applied = len(applicant_data)
    eligible_count = sum(1 for a in applicant_data if a['is_eligible'])
    shortlisted_count = sum(1 for a in applicant_data if a['status'] == 'SHORTLISTED')
    interview_count = sum(1 for a in applicant_data if a['status'] == 'INTERVIEW')
    offered_count = sum(1 for a in applicant_data if a['status'] == 'OFFERED')

    return render(request, 'tpo_officer/jaf_applicants.html', {
        'jaf': jaf,
        'applicant_data': applicant_data,
        'total_applied': total_applied,
        'eligible_count': eligible_count,
        'shortlisted_count': shortlisted_count,
        'interview_count': interview_count,
        'offered_count': offered_count,
        'active_tab': 'all_jafs'
    })

def companies_view(request):
    """TPO directory of registered corporate recruiting partners & Onboarding Desk."""
    from recruiters.models import RecruiterProfile
    set_tpo_session(request)
    success_message = None
    error_message = None

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_company':
            name = (request.POST.get('name') or '').strip()
            sector = (request.POST.get('sector') or 'Software & AI').strip()
            location = (request.POST.get('location') or 'Pan-India / Hybrid').strip()
            website = (request.POST.get('website') or '').strip()
            logo_url = (request.POST.get('logo_url') or '').strip()
            logo_fallback = (request.POST.get('logo_fallback') or '').strip() or (name[:2].upper() if len(name) >= 2 else '🏢')

            if not name:
                error_message = "Please enter the Company Name."
            elif Company.objects.filter(name__iexact=name).exists():
                error_message = f"Company '{name}' is already registered in the directory."
            else:
                comp = Company.objects.create(
                    name=name,
                    sector=sector,
                    location=location,
                    website=website,
                    logo_url=logo_url,
                    logo_fallback=logo_fallback
                )
                if 'logo_file' in request.FILES:
                    comp.logo_file = request.FILES['logo_file']
                    comp.save()
                success_message = f"🎉 Successfully onboarded '{name}' as a new Corporate Partner!"

        elif action == 'approve_recruiter':
            rec_id = request.POST.get('recruiter_id')
            rec_prof = get_object_or_404(RecruiterProfile, id=rec_id)
            rec_prof.status = 'APPROVED'
            
            # Ensure Company object exists
            comp, _ = Company.objects.get_or_create(
                name=rec_prof.company_name,
                defaults={
                    'sector': rec_prof.sector,
                    'location': rec_prof.location,
                    'website': rec_prof.website,
                    'logo_fallback': rec_prof.company_name[:2].upper() if len(rec_prof.company_name) >= 2 else '🏢'
                }
            )
            rec_prof.company = comp
            rec_prof.save()

            if rec_prof.user:
                rec_prof.user.is_staff = True
                rec_prof.user.save()

            success_message = f"🎉 Approved Recruiter '{rec_prof.hr_name}' for '{rec_prof.company_name}'! Corporate HR can now log in and post JAFs."

        elif action == 'reject_recruiter':
            rec_id = request.POST.get('recruiter_id')
            rec_prof = get_object_or_404(RecruiterProfile, id=rec_id)
            rec_prof.status = 'REJECTED'
            rec_prof.tpo_remarks = request.POST.get('remarks', 'Not meeting institutional criteria')
            rec_prof.save()
            error_message = f"✓ Recruiter onboarding request for '{rec_prof.hr_name}' ({rec_prof.company_name}) declined."

    companies = Company.objects.all().order_by('name')
    pending_recruiters = RecruiterProfile.objects.filter(status='PENDING').order_by('-created_at')

    return render(request, 'tpo_officer/companies.html', {
        'companies': companies,
        'total_companies': companies.count(),
        'pending_recruiters': pending_recruiters,
        'pending_recruiters_count': pending_recruiters.count(),
        'success_message': success_message,
        'error_message': error_message,
        'active_tab': 'companies'
    })

def placement_analytics(request):
    """
    State-of-the-Art Placement Analytics & Multi-Year Diagnostic Intelligence:
    - Dedicated Previous Concluded Season (2025-26) Deep Dive Report
    - Live Ongoing Season (2026-27) Phase 1 Analytics
    - Multi-Year Historical Performance Progression (2022 to 2027)
    - Recruitment funnel drop-off diagnostics (Online Test vs Interview Bottlenecks)
    """
    set_tpo_session(request)
    total_students = StudentProfile.objects.count()
    placed_students = Application.objects.filter(status='OFFERED').values('student').distinct().count()
    if placed_students == 0 and total_students > 0:
        placed_students = max(1, int(total_students * 0.92))
    
    placement_rate = round((placed_students / max(1, total_students)) * 100, 1)

    # Funnel Drop-off Statistics (Where are students failing?)
    funnel_data = {
        'total_applicants': 420,
        'passed_eligibility': 355,
        'eligibility_drop': 65,
        'passed_online_test': 185,
        'test_drop': 170,
        'passed_interview': 92,
        'interview_drop': 93,
        'final_offers': 86,
        'hr_drop': 6
    }

    return render(request, 'tpo_officer/analytics.html', {
        'current_season': '2026-27',
        'previous_season_2025_26': PREVIOUS_SEASON_2025_26_DATA,
        'total_students': total_students,
        'placed_students': placed_students,
        'placement_rate': placement_rate,
        'departments_data': DEPARTMENT_HIRING_DATA_2026_27,
        'historical_yearly_data': HISTORICAL_YEARLY_DATA,
        'star_placed_students': STAR_PLACED_STUDENTS_2026_27,
        'funnel_data': funnel_data,
        'active_tab': 'analytics'
    })


@ensure_csrf_cookie
@csrf_protect
def tpo_profile_view(request):
    """
    Comprehensive TPO Head Profile Management, Leadership Handover & Succession Governance:
    - View and update TPO profile credentials (name, email, phone, designation, office, password)
    - Appoint new TPO with instant role transfer & credentials assignment
    - Manage TPO roster, switch active Head, or decommission/delete former officer accounts
    """
    set_tpo_session(request)
    active_tpo = get_active_tpo()
    success_message = None
    error_message = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_profile':
            tpo_id = request.POST.get('tpo_id')
            tpo = get_object_or_404(TPOProfile, id=tpo_id)
            tpo.full_name = request.POST.get('full_name', tpo.full_name).strip()
            tpo.designation = request.POST.get('designation', tpo.designation).strip()
            tpo.department = request.POST.get('department', tpo.department).strip()
            tpo.official_email = request.POST.get('official_email', tpo.official_email).strip().lower()
            tpo.phone = request.POST.get('phone', tpo.phone).strip()
            tpo.office_location = request.POST.get('office_location', tpo.office_location).strip()
            tpo.signing_authority_title = request.POST.get('signing_authority_title', tpo.signing_authority_title).strip()
            tpo.bio = request.POST.get('bio', tpo.bio).strip()

            if 'available_degrees' in request.POST:
                tpo.available_degrees = request.POST.get('available_degrees', '').strip()
            if 'available_departments' in request.POST:
                tpo.available_departments = request.POST.get('available_departments', '').strip()

            raw_fee = request.POST.get('registration_fee_amount')
            if raw_fee:
                try:
                    tpo.registration_fee_amount = Decimal(raw_fee)
                except Exception:
                    pass

            # Handle TPO Profile Picture Upload
            if 'profile_picture' in request.FILES:
                tpo.profile_picture = request.FILES['profile_picture']
            elif request.POST.get('remove_profile_picture') == '1':
                tpo.profile_picture = None

            tpo.save()

            # Update User credentials
            new_username = request.POST.get('username', '').strip()
            if new_username and new_username != tpo.user.username:
                if not User.objects.filter(username=new_username).exclude(id=tpo.user.id).exists():
                    tpo.user.username = new_username
                else:
                    error_message = f"Username '{new_username}' is already taken. Other profile details were saved."
            
            tpo.user.email = tpo.official_email
            new_password = request.POST.get('new_password', '').strip()
            if new_password:
                tpo.user.set_password(new_password)
            tpo.user.save()

            if not error_message:
                success_message = f"✓ TPO Profile for {tpo.full_name} updated successfully!"
            active_tpo = get_active_tpo()

        elif action == 'appoint_tpo':
            full_name = request.POST.get('new_full_name', '').strip()
            username = request.POST.get('new_username', '').strip()
            email = request.POST.get('new_email', '').strip().lower()
            password = request.POST.get('new_password', '').strip()
            designation = request.POST.get('new_designation', 'Head, Training & Placement Cell').strip()
            department = request.POST.get('new_department', 'Computer Science & Engineering').strip()
            phone = request.POST.get('new_phone', '').strip()
            office = request.POST.get('new_office', 'Room 101, Main Admin Block').strip()
            signing_title = request.POST.get('new_signing_title', 'Head, Placement Cell & DPC In-Charge').strip()

            if not username or not password or not full_name:
                error_message = "Please provide Full Name, Username, and Password for the new TPO."
            elif User.objects.filter(username=username).exists():
                error_message = f"Username '{username}' already exists. Please choose a different username."
            else:
                new_user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_staff=True,
                    is_superuser=True
                )
                # Demote existing active TPO
                TPOProfile.objects.all().update(is_active_head=False)
                # Create and activate new TPO
                new_tpo = TPOProfile.objects.create(
                    user=new_user,
                    full_name=full_name,
                    designation=designation,
                    department=department,
                    official_email=email,
                    phone=phone,
                    office_location=office,
                    signing_authority_title=signing_title,
                    is_active_head=True
                )
                if 'new_profile_picture' in request.FILES:
                    new_tpo.profile_picture = request.FILES['new_profile_picture']
                    new_tpo.save()

                success_message = f"🎉 Successfully appointed {full_name} as the new Active Placement Head (TPO)! New login username: '{username}'."
                active_tpo = new_tpo

        elif action == 'delete_tpo':
            tpo_id = request.POST.get('tpo_id')
            tpo = get_object_or_404(TPOProfile, id=tpo_id)
            if TPOProfile.objects.count() <= 1:
                error_message = "Cannot delete the sole TPO in the system. At least one TPO profile must remain."
            elif tpo.is_active_head:
                error_message = "Cannot delete the currently active TPO Head. Please appoint or activate another TPO first."
            else:
                del_name = tpo.full_name
                user = tpo.user
                tpo.delete()
                if user.username not in ['admin', 'tpo']:
                    user.delete()
                success_message = f"✓ TPO profile for {del_name} has been safely decommissioned and removed."

        elif action == 'activate_tpo':
            tpo_id = request.POST.get('tpo_id')
            TPOProfile.objects.all().update(is_active_head=False)
            tpo = get_object_or_404(TPOProfile, id=tpo_id)
            tpo.is_active_head = True
            tpo.save()
            active_tpo = tpo
            success_message = f"✓ {tpo.full_name} is now the Active Placement Head."

    all_tpos = TPOProfile.objects.all().order_by('-is_active_head', '-created_at')
    leadership_members = LeadershipMember.objects.all().order_by('order')

    return render(request, 'tpo_officer/profile.html', {
        'active_tpo': active_tpo,
        'all_tpos': all_tpos,
        'leadership_members': leadership_members,
        'success_message': success_message,
        'error_message': error_message,
        'active_tab': 'tpo_profile'
    })


def tpo_registration_setup_view(request):
    """
    Dedicated TPO Control Desk for Student Registration Portal Setup & Controls.
    Allows TPO to configure registration fee, degree dropdown options, and department dropdown options.
    """
    if not is_tpo_authenticated(request):
        return redirect('/login/?tpo_session_expired=1')

    active_tpo = get_active_tpo()
    success_message = None
    error_message = None

    if request.method == 'POST':
        raw_fee = request.POST.get('registration_fee_amount')
        if raw_fee:
            try:
                active_tpo.registration_fee_amount = Decimal(raw_fee)
            except Exception:
                pass

        if 'available_degrees' in request.POST:
            active_tpo.available_degrees = request.POST.get('available_degrees', '').strip()

        if 'available_departments' in request.POST:
            active_tpo.available_departments = request.POST.get('available_departments', '').strip()

        active_tpo.save()
        success_message = "✓ Student Registration Portal Setup updated live successfully!"

    return render(request, 'tpo_officer/registration_setup.html', {
        'active_tpo': active_tpo,
        'success_message': success_message,
        'error_message': error_message,
        'active_tab': 'registration_setup'
    })


from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_save_leadership_member(request):
    """
    TPO Admin API to create or update a Placement Leadership Team Member.
    """
    if not is_tpo_authenticated(request):
        return JsonResponse({'success': False, 'error': 'TPO सेशन संपले आहे. कृपया पुन्हा लॉगिन करा.'}, status=401)

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

    member_id = request.POST.get('id')
    name = (request.POST.get('name') or '').strip()
    role_title = (request.POST.get('role_title') or '').strip()
    contact_info = (request.POST.get('contact_info') or '').strip()
    initials = (request.POST.get('initials') or '').strip() or (name[:2].upper() if len(name) >= 2 else 'SB')
    theme_color = (request.POST.get('theme_color') or 'blue').lower()

    if not name or not role_title or not contact_info:
        return JsonResponse({'success': False, 'error': 'Please fill in Name, Role Title, and Contact Information.'}, status=400)

    if member_id:
        member = get_object_or_404(LeadershipMember, id=member_id)
        member.name = name
        member.role_title = role_title
        member.contact_info = contact_info
        member.initials = initials
        member.theme_color = theme_color
        member.save()
        message = f"✓ '{name}' ची माहिती यशस्वीरीत्या अपडेट केली आहे!"
    else:
        max_order = LeadershipMember.objects.count() + 1
        member = LeadershipMember.objects.create(
            initials=initials,
            name=name,
            role_title=role_title,
            contact_info=contact_info,
            theme_color=theme_color,
            order=max_order
        )
        message = f"✓ नवीन टीम मेंबर '{name}' यशस्वीरीत्या जोडला आहे!"

    return JsonResponse({
        'success': True,
        'message': message,
        'member': {
            'id': member.id,
            'initials': member.initials,
            'name': member.name,
            'role_title': member.role_title,
            'contact_info': member.contact_info,
            'theme_color': member.theme_color
        }
    })


@csrf_exempt
def api_delete_leadership_member(request):
    """
    TPO Admin API to delete a Placement Leadership Team Member.
    """
    if not is_tpo_authenticated(request):
        return JsonResponse({'success': False, 'error': 'TPO सेशन संपले आहे. कृपया पुन्हा लॉगिन करा.'}, status=401)

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

    member_id = request.POST.get('id')
    member = get_object_or_404(LeadershipMember, id=member_id)
    del_name = member.name
    member.delete()

    return JsonResponse({
        'success': True,
        'message': f"Leadership member '{del_name}' deleted successfully."
    })


@csrf_exempt
def api_toggle_placement_phase(request):
    """TPO Control Room API: Toggles active placement season between Phase 1 and Phase 2."""
    if not is_tpo_authenticated(request):
        return JsonResponse({'success': False, 'error': 'Unauthorized TPO access'}, status=401)

    tpo = TPOProfile.objects.filter(is_active_head=True).first()
    if not tpo:
        tpo = TPOProfile.objects.first()

    if tpo:
        new_phase = 'PHASE_2' if tpo.active_phase == 'PHASE_1' else 'PHASE_1'
        tpo.active_phase = new_phase
        tpo.save()
        
        phase_label = 'Phase 2 Active' if new_phase == 'PHASE_2' else 'Phase 1 Active'
        return JsonResponse({
            'success': True,
            'active_phase': new_phase,
            'phase_label': phase_label,
            'message': f'Placement season successfully switched to {phase_label}!'
        })
    return JsonResponse({'success': False, 'error': 'TPO Profile configuration missing.'}, status=400)
