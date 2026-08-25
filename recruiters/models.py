from django.db import models
from django.contrib.auth.models import User
from students.models import Company

class RecruiterProfile(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending TPO Approval'),
        ('APPROVED', 'Approved by TPO'),
        ('REJECTED', 'Rejected / Declined'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile', null=True, blank=True)
    hr_name = models.CharField(max_length=120)
    official_email = models.EmailField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=20)
    designation = models.CharField(max_length=150, default="University Relations Manager / HR Lead")
    
    company_name = models.CharField(max_length=150)
    sector = models.CharField(max_length=100, default="Software & AI")
    location = models.CharField(max_length=200, default="Bangalore / Hybrid")
    website = models.URLField(max_length=300, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='recruiters')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    tpo_remarks = models.TextField(blank=True, default="")
    profile_picture = models.FileField(upload_to='profiles/recruiters/', blank=True, null=True, help_text="Official HR Representative / Company Logo Picture")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def profile_picture_url(self):
        if self.profile_picture:
            try:
                return self.profile_picture.url
            except Exception:
                pass
        if self.company and self.company.logo_file:
            try:
                return self.company.logo_file.url
            except Exception:
                pass
        return ""

    class Meta:
        verbose_name = "Corporate Recruiter Profile"
        verbose_name_plural = "Corporate Recruiter Profiles"

    def __str__(self):
        return f"{self.hr_name} ({self.company_name}) - {self.status}"
