from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from students.models import StudentProfile, Company, JobAnnouncementForm, Application, InterviewSlot, PlacementAnnouncement

class Command(BaseCommand):
    help = 'Seeds initial realistic placement data for IIT Bombay Student Portal'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting database seeding for IIT Bombay Placement Portal..."))

        # 1. Create or get Admin user
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'tpo@iitb.ac.in', 'is_staff': True, 'is_superuser': True}
        )
        admin_user.set_password('iitb2026')
        admin_user.save()

        # 2. Create or get Student user & Profile
        student_user, _ = User.objects.get_or_create(
            username='aarav',
            defaults={'email': 'aarav.sharma@iitb.ac.in', 'first_name': 'Aarav', 'last_name': 'Sharma'}
        )
        student_user.set_password('iitb2026')
        student_user.save()

        student, _ = StudentProfile.objects.get_or_create(
            user=student_user,
            defaults={
                'roll_number': '220050042',
                'full_name': 'Aarav Sharma',
                'degree': 'B.Tech in Computer Science & Engineering',
                'department': 'Computer Science & Engineering',
                'specialization': 'Honours in Artificial Intelligence • Minor in Finance',
                'cgpa': Decimal('9.48'),
                'batch': 'Class of 2026',
                'department_rank': 4,
                'is_dpc_verified': True,
                'resume_sde_name': 'Aarav_Sharma_SDE_Master.pdf',
                'resume_quant_name': 'Aarav_Sharma_Quant_Finance.pdf',
                'dpc_verifier': 'Prof. S. Bhattacharya (DPC)'
            }
        )

        # 3. Companies & JAFs
        companies_data = [
            {
                'name': 'Google',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg',
                'logo_fallback': 'G',
                'sector': 'Software & AI',
                'location': 'Bengaluru / Hyderabad (Domestic) • Mountain View (Intl)',
                'website': 'https://careers.google.com',
                'jaf': {
                    'role_title': 'Software Development Engineer - Systems & AI',
                    'sector': 'Software & AI',
                    'location': 'Bengaluru / Mountain View',
                    'ctc_display': '₹48.5 LPA',
                    'ctc_breakdown': 'Base: ₹24 LPA + Stocks: $35,000 (4 yrs) + Joining Bonus: ₹5 LPA + Relocation',
                    'cgpa_cutoff': Decimal('8.50'),
                    'eligible_branches': ['Computer Science (CS)', 'Electrical Engg (EE)', 'Maths & Computing (MnC)'],
                    'eligible_degrees': ['B.Tech', 'Dual Degree'],
                    'deadline': timezone.now() + timedelta(hours=14),
                    'deadline_display': 'Today, 11:59 PM IST',
                    'hiring_slot': 'Day 1 • Slot 1 (Dec 1)',
                    'description': 'As an SDE at Google, you will tackle massive scale engineering problems across distributed systems, machine learning infrastructure, and cloud networking. You will collaborate with global teams on products touching billions of users worldwide.',
                    'requirements': [
                        'Strong fundamentals in Data Structures, Distributed Algorithms, and OS',
                        'Proficiency in C++, Go, Java, or Python',
                        'Prior experience in systems programming, high-performance computing, or AI is a plus'
                    ],
                    'selection_process': [
                        {'step': 'Online Coding Test', 'date': 'Nov 20, 2026', 'details': '3 Algorithmic Challenges (90 mins)'},
                        {'step': 'Shortlist Announcement', 'date': 'Nov 25, 2026', 'details': 'Top 40 candidates shortlisted'},
                        {'step': 'Technical Round 1 & 2', 'date': 'Dec 1, 2026', 'details': 'System Design & Algorithms'},
                        {'step': 'Googlyness & Leadership', 'date': 'Dec 1, 2026', 'details': 'Behavioral & Culture Fit'}
                    ],
                    'initial_status': 'SHORTLISTED'
                }
            },
            {
                'name': 'Jane Street',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Jane_Street_Capital_Logo.svg/1200px-Jane_Street_Capital_Logo.svg.png',
                'logo_fallback': 'JS',
                'sector': 'Quant & Finance',
                'location': 'Hong Kong / London / New York',
                'website': 'https://janestreet.com',
                'jaf': {
                    'role_title': 'Quantitative Trader / Researcher',
                    'sector': 'Quant & Finance',
                    'location': 'Hong Kong / New York',
                    'ctc_display': '₹1.42 Cr ($275,000 USD)',
                    'ctc_breakdown': 'Base: $150,000 + Performance Bonus: $100,000 + Relocation: $25,000',
                    'cgpa_cutoff': Decimal('9.00'),
                    'eligible_branches': ['Open to All Branches (B.Tech / DD / BS)'],
                    'eligible_degrees': ['B.Tech', 'Dual Degree', 'BS'],
                    'deadline': timezone.now() + timedelta(hours=36),
                    'deadline_display': 'Tomorrow, 6:00 PM IST',
                    'hiring_slot': 'Day 1 • Slot 1 (Dec 1)',
                    'description': 'Jane Street is a quantitative trading firm with a unique focus on technology and collaborative problem solving. Traders and researchers build mathematical models and trade hundreds of thousands of financial products around the world.',
                    'requirements': [
                        'Exceptional mathematical intuition, probability theory, and combinatorics skills',
                        'Quick mental math and risk evaluation under uncertainty',
                        'Experience in OCaml, Python, C++, or functional programming is a bonus'
                    ],
                    'selection_process': [
                        {'step': 'Mental Math & Probability Test', 'date': 'Nov 18, 2026', 'details': '45 mins speed calculation'},
                        {'step': 'Quant Interview Round 1', 'date': 'Nov 26, 2026', 'details': 'Game theory and probability puzzles'},
                        {'step': 'Final Superday (Day 1)', 'date': 'Dec 1, 2026', 'details': '3 Intensive Trading Simulation Rounds'}
                    ],
                    'initial_status': 'INTERVIEW'
                }
            },
            {
                'name': 'Microsoft',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg',
                'logo_fallback': 'MS',
                'sector': 'Software & AI',
                'location': 'Hyderabad / Bengaluru / Noida',
                'website': 'https://careers.microsoft.com',
                'jaf': {
                    'role_title': 'Software Development Engineer II',
                    'sector': 'Software & AI',
                    'location': 'Hyderabad / Bengaluru',
                    'ctc_display': '₹51.0 LPA',
                    'ctc_breakdown': 'Base: ₹22.5 LPA + Performance Bonus: 20% + Stocks: $40,000 + Joining Bonus: ₹6 LPA',
                    'cgpa_cutoff': Decimal('7.50'),
                    'eligible_branches': ['CS', 'EE', 'MnC', 'Mechanical (ME)', 'Civil (CE)'],
                    'eligible_degrees': ['B.Tech', 'Dual Degree', 'M.Tech'],
                    'deadline': timezone.now() + timedelta(days=2),
                    'deadline_display': 'In 2 days',
                    'hiring_slot': 'Day 1 • Slot 2 (Dec 1)',
                    'description': 'Join the Azure Cloud and AI division at Microsoft. You will build cutting-edge generative AI copilot experiences and ultra-low latency hyper-scale infrastructure powering millions of enterprises worldwide.',
                    'requirements': [
                        'Solid foundations in object-oriented programming (C#, C++, Java)',
                        'Understanding of asynchronous architectures and microservices',
                        'Problem-solving acumen and collaborative team spirit'
                    ],
                    'selection_process': [
                        {'step': 'Online Assessment (OA)', 'date': 'Nov 15, 2026', 'details': 'Codility Test (2 questions)'},
                        {'step': 'Technical Interviews (Day 1)', 'date': 'Dec 1, 2026', 'details': '3 Technical Rounds + 1 AA Round'}
                    ],
                    'initial_status': 'INTERVIEW'
                }
            },
            {
                'name': 'Tower Research Capital',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Tower_Research_Capital_logo.svg/1200px-Tower_Research_Capital_logo.svg.png',
                'logo_fallback': 'TRC',
                'sector': 'Quant & Finance',
                'location': 'Gurugram / Singapore',
                'website': 'https://tower-research.com',
                'jaf': {
                    'role_title': 'Core Engineering Analyst - High Frequency Trading',
                    'sector': 'Quant & Finance',
                    'location': 'Gurugram / Singapore',
                    'ctc_display': '₹65.0 LPA',
                    'ctc_breakdown': 'Base: ₹32 LPA + Guaranteed Bonus: ₹18 LPA + Performance Incentive + Relocation',
                    'cgpa_cutoff': Decimal('8.80'),
                    'eligible_branches': ['Computer Science (CS)', 'Electrical Engg (EE)', 'Maths & Computing (MnC)'],
                    'eligible_degrees': ['B.Tech', 'Dual Degree'],
                    'deadline': timezone.now() + timedelta(days=3),
                    'deadline_display': 'In 3 days',
                    'hiring_slot': 'Day 1 • Slot 1 (Dec 1)',
                    'description': 'Develop sub-microsecond low-latency trading software, custom kernel bypass network stacks, and FPGA accelerated pipelines in C++20 for global financial exchanges.',
                    'requirements': [
                        'Mastery in Modern C++ (C++17/20), multi-threading, lock-free data structures',
                        'In-depth grasp of CPU cache hierarchies, memory models, and Linux internals'
                    ],
                    'selection_process': [
                        {'step': 'Hackerrank Systems Test', 'date': 'Nov 22, 2026', 'details': 'Low-latency C++ challenges'},
                        {'step': 'Interviews (Day 1)', 'date': 'Dec 1, 2026', 'details': 'Architecture, Concurrency & C++ Deep Dive'}
                    ],
                    'initial_status': None
                }
            },
            {
                'name': 'Texas Instruments',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Texas_Instruments_logo.svg/1200px-Texas_Instruments_logo.svg.png',
                'logo_fallback': 'TI',
                'sector': 'Core Engineering',
                'location': 'Bengaluru',
                'website': 'https://ti.com',
                'jaf': {
                    'role_title': 'Analog & Mixed-Signal IC Design Engineer',
                    'sector': 'Core Engineering',
                    'location': 'Bengaluru',
                    'ctc_display': '₹34.0 LPA',
                    'ctc_breakdown': 'Base: ₹20 LPA + RSU: $20,000 + Joining Bonus: ₹4 LPA',
                    'cgpa_cutoff': Decimal('7.80'),
                    'eligible_branches': ['Electrical (EE)', 'Energy Science (EN)', 'Engineering Physics (EP)'],
                    'eligible_degrees': ['B.Tech', 'Dual Degree', 'M.Tech'],
                    'deadline': timezone.now() + timedelta(days=3),
                    'deadline_display': 'In 3 days',
                    'hiring_slot': 'Day 2 • Slot 1 (Dec 2)',
                    'description': 'Design state-of-the-art power management ICs, RF transceivers, and precision data converters for next-generation automotive and aerospace electronics.',
                    'requirements': [
                        'Deep knowledge of CMOS Analog Circuit Design, Op-Amps, and Bandgap References',
                        'Familiarity with Cadence Virtuoso and SPICE simulation suites'
                    ],
                    'selection_process': [
                        {'step': 'Written Technical Assessment', 'date': 'Nov 23, 2026', 'details': 'Analog Circuits & Signals'},
                        {'step': 'Technical Interviews', 'date': 'Dec 2, 2026', 'details': 'Schematic design and layout questions'}
                    ],
                    'initial_status': None
                }
            },
            {
                'name': 'McKinsey & Company',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/McKinsey_%26_Company_Logo.svg/1200px-McKinsey_%26_Company_Logo.svg.png',
                'logo_fallback': 'McK',
                'sector': 'Management Consulting',
                'location': 'Mumbai / Delhi / Bengaluru',
                'website': 'https://mckinsey.com',
                'jaf': {
                    'role_title': 'Junior Associate - Strategy & Digital Transformation',
                    'sector': 'Management Consulting',
                    'location': 'Mumbai / Delhi',
                    'ctc_display': '₹32.0 LPA',
                    'ctc_breakdown': 'Fixed: ₹24 LPA + Performance Bonus: ₹6 LPA + Retiral & Benefits',
                    'cgpa_cutoff': Decimal('8.00'),
                    'eligible_branches': ['Open to All Engineering & Science Branches'],
                    'eligible_degrees': ['B.Tech', 'Dual Degree', 'M.Tech', 'MBA'],
                    'deadline': timezone.now() + timedelta(days=4),
                    'deadline_display': 'In 4 days',
                    'hiring_slot': 'Day 1 • Slot 2 (Dec 1)',
                    'description': 'Work with C-suite leadership across Fortune 500 companies to solve complex strategic dilemmas, execute digital transformations, and drive sustainable growth.',
                    'requirements': [
                        'Strong structured problem solving and quantitative reasoning',
                        'Exemplary communication, stakeholder management, and executive presence'
                    ],
                    'selection_process': [
                        {'step': 'Problem Solving Game (PSG)', 'date': 'Nov 16, 2026', 'details': 'Imbellus Simulation Assessment'},
                        {'step': 'Case Interviews (Day 1)', 'date': 'Dec 1, 2026', 'details': '3 Rounds of Business Case & PEI'}
                    ],
                    'initial_status': 'APPLIED'
                }
            },
            {
                'name': 'Apple',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg',
                'logo_fallback': 'AAPL',
                'sector': 'Core Engineering',
                'location': 'Hyderabad / Bengaluru',
                'website': 'https://apple.com/careers',
                'jaf': {
                    'role_title': 'Silicon Validation & Architecture Engineer',
                    'sector': 'Core Engineering',
                    'location': 'Hyderabad / Bengaluru',
                    'ctc_display': '₹42.0 LPA',
                    'ctc_breakdown': 'Base: ₹24 LPA + Apple RSU: $28,000 + Joining Bonus: ₹5 LPA',
                    'cgpa_cutoff': Decimal('8.00'),
                    'eligible_branches': ['Electrical (EE)', 'Computer Science (CS)', 'Mechanical (ME)'],
                    'eligible_degrees': ['B.Tech', 'Dual Degree', 'M.Tech'],
                    'deadline': timezone.now() + timedelta(days=5),
                    'deadline_display': 'In 5 days',
                    'hiring_slot': 'Day 2 • Slot 1 (Dec 2)',
                    'description': 'Join the Silicon Engineering Group to test, debug, and validate next-gen M-series Apple Silicon powering Mac, iPad, and Vision Pro devices.',
                    'requirements': [
                        'Knowledge of Computer Architecture, RISC-V/ARM, and Verilog/SystemVerilog',
                        'Proficiency with Python/C++ automation test harnesses'
                    ],
                    'selection_process': [
                        {'step': 'Silicon Architecture Test', 'date': 'Nov 24, 2026', 'details': 'Microarchitecture & Digital Logic'},
                        {'step': 'Technical Interviews', 'date': 'Dec 2, 2026', 'details': '3 Technical Architecture Rounds'}
                    ],
                    'initial_status': None
                }
            }
        ]

        for item in companies_data:
            company, _ = Company.objects.get_or_create(
                name=item['name'],
                defaults={
                    'logo_url': item['logo_url'],
                    'logo_fallback': item['logo_fallback'],
                    'sector': item['sector'],
                    'location': item['location'],
                    'website': item['website']
                }
            )

            jdata = item['jaf']
            jaf, _ = JobAnnouncementForm.objects.get_or_create(
                company=company,
                role_title=jdata['role_title'],
                defaults={
                    'sector': jdata['sector'],
                    'location': jdata['location'],
                    'ctc_display': jdata['ctc_display'],
                    'ctc_breakdown': jdata['ctc_breakdown'],
                    'cgpa_cutoff': jdata['cgpa_cutoff'],
                    'eligible_branches': jdata['eligible_branches'],
                    'eligible_degrees': jdata['eligible_degrees'],
                    'deadline': jdata['deadline'],
                    'deadline_display': jdata['deadline_display'],
                    'hiring_slot': jdata['hiring_slot'],
                    'description': jdata['description'],
                    'requirements': jdata['requirements'],
                    'selection_process': jdata['selection_process'],
                }
            )

            # Create initial application status if configured
            if jdata.get('initial_status'):
                Application.objects.get_or_create(
                    student=student,
                    jaf=jaf,
                    defaults={
                        'status': jdata['initial_status'],
                        'resume_used': student.resume_sde_name
                    }
                )

        # 4. Create Interview Slots
        msft_jaf = JobAnnouncementForm.objects.filter(company__name='Microsoft').first()
        if msft_jaf:
            InterviewSlot.objects.get_or_create(
                student=student,
                jaf=msft_jaf,
                round_name='Round 1: Systems & Concurrency',
                defaults={
                    'interview_date': 'Dec 1, 2026',
                    'interview_time': '08:30 AM - 09:30 AM IST',
                    'slot_display': 'Day 1 • Slot 1',
                    'location': 'Room MB-204 (Gulmohar Building) / Microsoft Teams',
                    'meeting_link': 'https://teams.microsoft.com/l/meetup-join/iitb-slot1-msft',
                    'interview_type': 'Technical',
                    'status': 'Confirmed'
                }
            )

        js_jaf = JobAnnouncementForm.objects.filter(company__name='Jane Street').first()
        if js_jaf:
            InterviewSlot.objects.get_or_create(
                student=student,
                jaf=js_jaf,
                round_name='Round 2: Probability & Market Making Games',
                defaults={
                    'interview_date': 'Dec 1, 2026',
                    'interview_time': '11:00 AM - 12:15 PM IST',
                    'slot_display': 'Day 1 • Slot 1',
                    'location': 'Computer Center Lab 1 (CC-102)',
                    'meeting_link': 'https://janestreet.zoom.us/j/iitb-day1-superday',
                    'interview_type': 'Superday Quant',
                    'status': 'Confirmed'
                }
            )

        goog_jaf = JobAnnouncementForm.objects.filter(company__name='Google').first()
        if goog_jaf:
            InterviewSlot.objects.get_or_create(
                student=student,
                jaf=goog_jaf,
                round_name='Round 1: Distributed Algorithms & Systems',
                defaults={
                    'interview_date': 'Dec 1, 2026',
                    'interview_time': '03:00 PM - 04:00 PM IST',
                    'slot_display': 'Day 1 • Slot 2',
                    'location': 'Room MB-301 (Gulmohar Building) / Google Meet',
                    'meeting_link': 'https://meet.google.com/iitb-goog-day1',
                    'interview_type': 'Technical',
                    'status': 'Confirmed'
                }
            )

        # 5. Create Announcements
        announcements_data = [
            {
                'tag': 'URGENT',
                'tag_type': 'danger',
                'title': 'Day 1 Slot 1 Interview Schedules Released',
                'author': 'Placement Office (TPO)',
                'time_display': '15 mins ago',
                'content': 'All shortlisted students for Google, Jane Street, Microsoft, and Tower Research must report to the Gulmohar Building by 07:30 AM IST on Dec 1st. Formal dress code and physical ID cards mandatory.'
            },
            {
                'tag': 'SHORTLIST',
                'tag_type': 'success',
                'title': 'Google SDE Shortlist (40 Candidates) Published',
                'author': 'DPC Computer Science',
                'time_display': '2 hours ago',
                'content': 'The shortlist for Google Software Engineering (Systems & AI) has been published on the portal. Shortlisted candidates have received direct calendar invites.'
            },
            {
                'tag': 'NOTICE',
                'tag_type': 'warning',
                'title': 'Resume Freezing Window Closes Tonight at 23:59 IST',
                'author': 'Prof. In-Charge, Placements',
                'time_display': '5 hours ago',
                'content': 'No further modifications will be permitted for Master Resumes for Phase 1 Day 1 & Day 2 companies after midnight.'
            },
            {
                'tag': 'PPT INFO',
                'tag_type': 'info',
                'title': 'Tower Research Capital Pre-Placement Talk Recording',
                'author': 'Student Placement Team',
                'time_display': 'Yesterday',
                'content': 'The video recording of the TRC PPT held in Auditorium 1 has been uploaded to the placement portal drive.'
            }
        ]

        for ann in announcements_data:
            PlacementAnnouncement.objects.get_or_create(
                title=ann['title'],
                defaults={
                    'content': ann['content'],
                    'tag': ann['tag'],
                    'tag_type': ann['tag_type'],
                    'author': ann['author'],
                    'time_display': ann['time_display']
                }
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded all IIT Bombay Placement data!"))
        self.stdout.write(self.style.SUCCESS("Default credentials: admin/iitb2026 and aarav/iitb2026"))
