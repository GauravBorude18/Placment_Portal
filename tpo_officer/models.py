from django.db import models
from django.contrib.auth.models import User

class TPOProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tpo_profile')
    full_name = models.CharField(max_length=200, default="Prof. S. Bhattacharya")
    designation = models.CharField(max_length=200, default="Head, Training & Placement Cell")
    department = models.CharField(max_length=200, default="Computer Science & Engineering")
    official_email = models.EmailField(default="tpo@a2zplacement.edu")
    phone = models.CharField(max_length=50, default="+91 98220 12345")
    office_location = models.CharField(max_length=250, default="Room 101, Main Admin Block, A2Z Campus")
    signing_authority_title = models.CharField(max_length=250, default="Head, Placement Cell & DPC In-Charge")
    profile_picture = models.FileField(upload_to='profiles/tpo/', blank=True, null=True, help_text="Official TPO photo")
    bio = models.TextField(blank=True, default="Managing Tier-1 campus recruitments, corporate relations, and student career governance.")
    active_phase = models.CharField(max_length=20, default="PHASE_1", help_text="PHASE_1 or PHASE_2")
    registration_fee_amount = models.DecimalField(max_digits=8, decimal_places=2, default=99.00, help_text="Official Student Registration Fee in INR")
    available_degrees = models.TextField(
        default="B.E. (Bachelor of Engineering), B.Tech (Bachelor of Technology)",
        help_text="Comma-separated list of Degrees available during student registration"
    )
    available_departments = models.TextField(
        default="Computer Science & Engineering, Computer Engineering, Electrical Engineering, Mechanical Engineering, Civil Engineering, Information Technology, Mathematics & Computing, Data Science & AI Centre",
        help_text="Comma-separated list of Departments available during student registration"
    )
    is_active_head = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def degree_list(self):
        if self.available_degrees:
            items = [d.strip() for d in self.available_degrees.replace('\n', ',').split(',') if d.strip()]
            if items:
                return items
        return [
            "B.E. (Bachelor of Engineering)",
            "B.Tech (Bachelor of Technology)"
        ]

    @property
    def department_list(self):
        if self.available_departments:
            items = [d.strip() for d in self.available_departments.replace('\n', ',').split(',') if d.strip()]
            if items:
                return items
        return [
            "Computer Science & Engineering",
            "Computer Engineering",
            "Electrical Engineering",
            "Mechanical Engineering",
            "Civil Engineering",
            "Information Technology",
            "Mathematics & Computing",
            "Data Science & AI Centre"
        ]

    @property
    def profile_picture_url(self):
        if self.profile_picture:
            try:
                return self.profile_picture.url
            except Exception:
                pass
        return None

    class Meta:
        verbose_name = "TPO Profile"
        verbose_name_plural = "TPO Profiles"
        ordering = ['-is_active_head', '-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.designation} ({'Active Head' if self.is_active_head else 'Former'})"


class LeadershipMember(models.Model):
    THEME_CHOICES = [
        ('blue', 'Royal Blue'),
        ('green', 'Emerald Green'),
        ('purple', 'Violet Purple'),
        ('gold', 'Amber Gold'),
    ]

    initials = models.CharField(max_length=10, default="SB")
    name = models.CharField(max_length=200)
    role_title = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=200, help_text="Email or Phone Number (e.g. ✉️ dpc.incharge@a2z.edu.in)")
    theme_color = models.CharField(max_length=20, choices=THEME_CHOICES, default='blue')
    order = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.name} ({self.role_title})"
