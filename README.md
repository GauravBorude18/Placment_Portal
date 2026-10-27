# 🎓 Campus Placement & Training Management Portal (A2Z Placement Cell)

An end-to-end, enterprise-grade Campus Placement and Career Governance System built with **Python & Django**. This portal bridges graduating students, corporate recruiters, and the Training & Placement Office (TPO) through institutional governance, verified academic credentials, and automated recruitment pipelines.

---

## 🌟 Key Features & Portals

### 1. 🎓 Student Placement Portal (`students`)
- **Profile & Academic Verification:** Secure candidate onboarding with 10th, 12th/Diploma percentages, semester SGPA/CGPA, and departmental credentials audited by the TPO.
- **Master Resume Hub:** Upload and manage verified master resumes and skill portfolios.
- **Job Announcement Forms (JAF):** Browse verified corporate openings with real-time eligibility checks (branch, cutoff, backlog rules).
- **1-Click Application & Live Tracker:** Apply for roles and monitor stage-by-stage hiring progress (Shortlisted, Technical Interview, HR Round, Offer Letter).
- **1-Student-1-Job Policy:** Enforces institutional placement rules with Dream and Super-Dream offer upgrades.

### 2. 🏢 Corporate Recruiter Desk (`recruiters`)
- **Company & HR Onboarding:** Secure registration and verification for company talent acquisition teams.
- **JAF Creation Wizard:** Post structured job vacancies specifying role profiles, CTC breakdown (base, bonus, stock options), cutoff percentages, and eligible batches.
- **Applicant Pipeline & Funnel Tracker:** Filter eligible candidate pools, review audited academic records, download verified resumes, and advance candidates across rounds.
- **Offer Rollout & Status Updates:** Direct status notifications and offer rollouts to selected candidates.

### 3. 🛡️ TPO Administrative Control Room (`tpo_officer`)
- **Central Nodal Governance:** Complete oversight of campus placement drives, academic years, and recruitment sessions.
- **Student Verification Queue:** Audit and approve student registrations or place academic records on hold with customized feedback.
- **Company & Drive Approval:** Review recruiter profiles and approve Job Announcement Forms (JAFs) before publishing to students.
- **Day 1 / Day 2 Superday Slot Matrix:** Intelligent, conflict-free scheduling for high-volume campus interview slots (Slot 1: 08:00 AM, Slot 2: 02:00 PM).
- **Placement Analytics & Reports:** Real-time metrics including highest package, average domestic CTC, batch placement rates, and corporate participation.

### 4. 🎨 Modern & Responsive Frontend (Human UI/UX)
- **100% Mobile & Desktop Responsive:** Fully optimized with custom `@media` queries across smartphones (320px–480px), tablets (768px), and high-resolution displays.
- **Glassmorphic Navigation Bar:** Clean backdrop blur with interactive role-based `Login ▾` and `Register ▾` dropdowns and touch-scrollable tabs.
- **Visual Process Funnels:** Five-stage campus recruitment process visualizer (JAF Submission ➔ Academic Audit ➔ Online Assessment ➔ Technical & HR Superday ➔ Offer Rollout).

---

## 🛠️ Technology Stack

| Component | Technology | Description |
|---|---|---|
| **Backend Framework** | [Django](https://www.djangoproject.com/) (Python 3.10+) | High-level Python web framework with robust ORM and security |
| **Database** | SQLite3 / PostgreSQL compatible | Relational database schema with relational integrity |
| **Frontend Styling** | Custom CSS3 & Vanilla JavaScript (ES6+) | Lightweight, fast, dependency-free UI with responsive design |
| **Authentication** | Django Auth & Role-Based Access Control | Granular access separation (Student, Recruiter, TPO Admin) |
| **API Architecture** | Django REST Framework & JWT Ready | Modular REST endpoints for data exchange and verification |

---

## 📁 Project Directory Structure

```text
placement-portal/
├── manage.py                           # Django CLI controller
├── placement_core/                     # Project configuration & root routing
│   ├── settings.py                     # Installed apps, middleware, database config
│   ├── urls.py                         # Master URL routing table
│   └── wsgi.py                         # WSGI server entry point
├── students/                           # Student Portal App
│   ├── models.py                       # Student profile, resume, and application models
│   ├── views.py                        # Student dashboard, auth, and JAF application logic
│   └── templates/students/             # Base template, landing page, and dashboards
├── recruiters/                         # Corporate Recruiter App
│   ├── models.py                       # Company and JAF models
│   ├── views.py                        # HR dashboard, candidate reviewer, JAF creation
│   └── static/recruiters/              # Recruiter-specific CSS/JS assets
├── tpo_officer/                        # TPO Administration App
│   ├── models.py                       # Slot matrix, verification audit models
│   ├── views.py                        # Control room, approval queues, analytics
│   └── static/tpo_officer/             # TPO control room styling
├── static/                             # Shared global CSS, JavaScript, and branding logos
│   ├── css/style.css                   # Responsive styles and media queries
│   └── js/                             # Shared client interactions
└── media/                              # Uploaded profile photos, company crests, resumes
```

---

## 🚀 Getting Started & Installation

Follow these steps to set up and run the project locally on your machine:

### 1. Prerequisites
- **Python 3.10** or higher installed ([Download Python](https://www.python.org/downloads/))
- **Git** installed on your system ([Download Git](https://git-scm.com/))

### 2. Clone the Repository
```bash
git clone https://github.com/GauravBorude18/Placment_Portal.git
cd Placment_Portal
```

### 3. Create & Activate a Virtual Environment
- **On Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **On Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install django djangorestframework djangorestframework-simplejwt pillow
```

### 5. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (TPO Admin)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🔒 Security & Placement Governance Policies
- **Data Privacy:** Resumes and academic marks are strictly audited and accessible only to verified hiring partners and placement coordinators.
- **CSRF & XSS Protection:** Django standard middleware ensures CSRF token verification across all forms and AJAX endpoints.
- **Disciplinary Control:** TPO officers can place student accounts on academic or behavioral hold with real-time portal notifications.

---

## 👨‍💻 Author & Contributions
Developed with care for institutional campus placements and corporate talent acquisition.

- **GitHub Repository:** [https://github.com/GauravBorude18/Placment_Portal](https://github.com/GauravBorude18/Placment_Portal)
- **Author:** [Gaurav Borude](https://github.com/GauravBorude18)

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
