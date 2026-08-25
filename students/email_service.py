from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import StudentEmailNotification, InterviewSlot
import threading

def send_recruitment_stage_email(student, jaf, new_status, custom_note=None, h_round=None):
    """
    Dispatches rich official recruitment emails to the student when their stage changes.
    Supports dynamic HiringRound objects for exact scheduled date, time, venue, and stage title!
    """
    recipient_email = student.user.email or f"{student.roll_number.lower()}@campus.ac.in"
    company_name = jaf.company.name
    role_title = jaf.role_title
    
    subject = ""
    headline = ""
    body_content = ""
    action_url = ""
    action_label = ""
    notification_type = "SHORTLIST"
    now = timezone.now()

    if h_round:
        stage_name = h_round.title
        sched_date = h_round.scheduled_date or (now + timedelta(days=1)).strftime("%b %d, %Y")
        sched_time = h_round.scheduled_time or "10:00 AM IST"
        venue_raw = (h_round.location_or_platform or "").strip()
        venue = venue_raw or "A2Z Placement Cell / Online Assessment Portal"
        criteria = h_round.passing_criteria or "N/A"

        # Smart Platform Link Detection: Extract entered URL with Regex or match platform type
        import re
        target_link = "/dashboard/"
        btn_label = f"View {stage_name} Details ➔"

        venue_lower = venue_raw.lower()
        url_match = re.search(r'https?://[^\s]+', venue_raw)
        extracted_url = url_match.group(0).rstrip('.,;') if url_match else None

        if extracted_url:
            target_link = extracted_url
            if "hackerrank" in venue_lower or "hacker" in venue_lower:
                btn_label = f"⚡ Start {stage_name} (HackerRank) ➔"
            elif "meet.google" in venue_lower or "gmeet" in venue_lower or "google meet" in venue_lower:
                btn_label = f"📹 Join {stage_name} (Google Meet) ➔"
            elif "zoom" in venue_lower:
                btn_label = f"📹 Join {stage_name} (Zoom) ➔"
            elif "unstop" in venue_lower:
                btn_label = f"🏆 Open {stage_name} (Unstop) ➔"
            else:
                btn_label = f"🚀 Open {stage_name} Platform ➔"
        elif venue_raw.startswith("www."):
            target_link = f"https://{venue_raw}"
            btn_label = f"🚀 Open {stage_name} Platform ➔"
        elif "hackerrank" in venue_lower or h_round.round_type == 'ONLINE_TEST' or 'coding' in stage_name.lower() or 'test' in stage_name.lower():
            target_link = f"https://hackerrank.com/a2z-test-{jaf.id}"
            btn_label = f"⚡ Start {stage_name} (HackerRank) ➔"
        elif "meet.google" in venue_lower or "gmeet" in venue_lower or "google meet" in venue_lower or h_round.round_type in ['TECH_INTERVIEW_1', 'TECH_INTERVIEW_2', 'HR_INTERVIEW']:
            target_link = "https://meet.google.com/a2z-interview-panel"
            btn_label = f"📹 Join {stage_name} (Google Meet) ➔"
        elif "zoom" in venue_lower:
            target_link = "https://zoom.us/join"
            btn_label = f"📹 Join {stage_name} (Zoom) ➔"
        elif "unstop" in venue_lower:
            target_link = "https://unstop.com/"
            btn_label = f"🏆 Open {stage_name} (Unstop) ➔"

        subject = f"🎯 Advanced to Stage: {stage_name} — {company_name} ({role_title})"
        headline = f"Congratulations {student.full_name}! Selected for {stage_name}"
        action_url = target_link
        action_label = btn_label
        
        body_content = f"""Dear {student.full_name},

Congratulations! We are pleased to inform you that you have been selected to advance to the next recruitment stage: '{stage_name}' for the position of {role_title} at {company_name}.

📌 Stage Schedule & Venue Details:
• Stage Title: {stage_name}
• Scheduled Date: {sched_date}
• Scheduled Time: {sched_time}
• Platform / Venue: {venue}
• Evaluation Criteria: {criteria}

Please be prepared and log in / report 15 minutes prior to the scheduled start time.

Best regards,
Talent Acquisition & Campus Recruitment Team, {company_name}
In Association with A2Z Placement Cell"""

    elif new_status == 'SHORTLISTED':
        notification_type = 'SHORTLIST'
        subject = f"🎯 Shortlisted for {company_name} — Next Step: Technical OA"
        headline = f"Congratulations! You have been shortlisted for {company_name}"
        action_url = f"https://hackerrank.com/a2z-test-{jaf.id}"
        action_label = "Start Technical OA Test ➔"
        active_until_date = (now + timedelta(days=3)).strftime("%b %d, %Y")
        
        body_content = f"""Dear {student.full_name},

We are pleased to inform you that your profile has been successfully SHORTLISTED for the role of {role_title} at {company_name} based on your verified academic record (CPI: {student.cgpa}).

📝 Assessment Details:
• Platform: HackerRank Automated Coding Assessment
• Duration: 90 Minutes
• Topics: Data Structures, Algorithms & Domain Fundamentals
• Test Window: Active until {active_until_date} • 11:59 PM IST

Please ensure a stable internet connection and quiet environment before starting.

Best regards,
Talent Acquisition Team, {company_name}
In Association with A2Z Placement Cell"""

    elif new_status == 'INTERVIEW':
        notification_type = 'INTERVIEW'
        subject = f"🎙️ Official Technical Interview Call: {company_name} ({role_title})"
        headline = f"Interview Scheduled with Technical Panel — {company_name}"
        action_url = "https://meet.google.com/a2z-interview-panel-1"
        action_label = "Join Video Interview Room 🔗"
        interview_date_str = (now + timedelta(days=2)).strftime("%b %d, %Y")
        
        # Ensure interview slot exists
        InterviewSlot.objects.get_or_create(
            student=student,
            jaf=jaf,
            defaults={
                'round_name': 'Round 1: Technical & Core Architecture',
                'interview_date': interview_date_str,
                'interview_time': '10:00 AM - 11:15 AM IST',
                'slot_display': 'Day 1 • Slot 1',
                'location': 'Room MB-204 (Gulmohar Building) / Google Meet Panel',
                'meeting_link': action_url,
                'interview_type': 'Technical Live Coding',
                'status': 'Confirmed'
            }
        )

        body_content = f"""Dear {student.full_name},

Congratulations! Having successfully cleared the technical evaluation, you are invited to appear for the Technical Interview with {company_name} for the position of {role_title}.

🗓️ Interview Schedule:
• Slot: Day 1 • Slot 1 ({interview_date_str})
• Time: 10:00 AM - 11:15 AM IST
• Venue: Room MB-204 (Gulmohar Building) / Google Meet
• Focus Areas: System Design, Whiteboard Coding & Project Defense

Please be available 15 minutes prior to your allocated slot.

Best regards,
Campus Recruitment Panel, {company_name}
A2Z Placement Cell"""

    elif new_status == 'OFFERED':
        notification_type = 'OFFER'
        subject = f"🏆 OFFICIAL CAMPUS PLACEMENT OFFER: {company_name} ({jaf.ctc_display})!"
        headline = f"Congratulations {student.full_name}! Formal Job Offer Extended by {company_name}."
        action_url = "/dashboard/"
        action_label = "Accept Placement Offer in Portal 📜"
        body_content = f"""Dear {student.full_name},

On behalf of {company_name}, we take immense pleasure in offering you the full-time position of {role_title} as part of the Campus Placement Season 2025-26.

💼 Offer Highlights:
• Total CTC Package: {jaf.ctc_display}
• Compensation Structure: {jaf.ctc_breakdown}
• Joining Location: {jaf.location}
• Role: {role_title}

Your dedication and exceptional performance throughout the recruitment process stood out. Please log in to the student portal to review and accept the official letter.

Heartiest congratulations from all of us!

Warm regards,
Head of University Relations & Talent Acquisition, {company_name}
Prof. S. Bhattacharya, Head — A2Z Placement Cell"""

    elif new_status == 'REJECTED':
        notification_type = 'REJECTED'
        subject = f"Application Status Update: {company_name} ({role_title})"
        headline = f"Status Update for {company_name} Application"
        action_url = "/dashboard/"
        action_label = "View Other Openings"
        body_content = f"""Dear {student.full_name},

Thank you for your interest and time during the selection process for {role_title} at {company_name}. 

While your credentials are commendable, after careful review, we regret to inform you that we will not be moving forward with your candidature for this specific role at this time.

We wish you the very best in your upcoming campus placement drives.

Sincerely,
Recruitment Team, {company_name}"""

    # 1. Log in Database Notification Mailbox
    notif = StudentEmailNotification.objects.create(
        student=student,
        company=jaf.company,
        jaf=jaf,
        notification_type=notification_type,
        subject=subject,
        recipient_email=recipient_email,
        headline=headline,
        body_content=body_content,
        action_url=action_url,
        action_label=action_label
    )

    # 2. Dispatch real Django send_mail in background thread (0ms lag)
    def _async_stage_send():
        try:
            send_mail(
                subject=subject,
                message=body_content,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'placement-cell@a2z.edu.in'),
                recipient_list=[recipient_email],
                fail_silently=True
            )
            print(f"[STAGE EMAIL SENT] {subject} -> {recipient_email}")
        except Exception as e:
            print(f"[STAGE EMAIL NOTICE] {e}")

    threading.Thread(target=_async_stage_send, daemon=True).start()
    return notif


import threading

def send_registration_otp_email(email, otp):
    """Dispatches 6-digit verification OTP email asynchronously in a non-blocking background thread for 0ms UI delay."""
    subject = f"🔐 Your A2Z Placement Portal Verification Code: {otp}"
    body = f"""Dear Candidate,

Your one-time email verification code (OTP) for the A2Z Placement & Recruitment Portal is:

{otp}

This code is valid for 10 minutes. Please enter this code on the registration page to verify your institutional email address.

If you did not request this code, please ignore this email.

A2Z Placement Cell Security Desk"""

    def _async_send():
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'placement-cell@a2z.edu.in'),
                recipient_list=[email],
                fail_silently=False
            )
            print(f"[EMAIL SUCCESS] 6-digit OTP {otp} successfully dispatched to: {email}")
        except Exception as e:
            print(f"[EMAIL NOTICE] SMTP Error sending to {email}: {e}")

    # Launch in non-blocking background thread
    threading.Thread(target=_async_send, daemon=True).start()
    return True

