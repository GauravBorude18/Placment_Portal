from django.contrib import admin
from .models import StudentProfile, Company, JobAnnouncementForm, Application, InterviewSlot, PlacementAnnouncement

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'full_name', 'department', 'cgpa', 'verification_status', 'is_dpc_verified', 'approved_by')
    search_fields = ('roll_number', 'full_name', 'department', 'user__email')
    list_filter = ('verification_status', 'is_dpc_verified', 'department', 'degree')
    actions = ['approve_students_for_season', 'reject_students_credentials']

    @admin.action(description="✓ Approve Selected Students for Placement Season (Placement Head Sign-Off)")
    def approve_students_for_season(self, request, queryset):
        queryset.update(
            is_dpc_verified=True,
            verification_status='APPROVED',
            approved_by='Prof. S. Bhattacharya (Head & DPC In-Charge)'
        )
        self.message_user(request, f"{queryset.count()} student credentials approved successfully!")

    @admin.action(description="⚠️ Mark Selected as Requires Correction / Re-submission")
    def reject_students_credentials(self, request, queryset):
        queryset.update(
            is_dpc_verified=False,
            verification_status='REJECTED'
        )
        self.message_user(request, f"{queryset.count()} student profiles flagged for correction.")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'sector', 'location', 'website')
    search_fields = ('name', 'sector', 'location')
    list_filter = ('sector',)


@admin.register(JobAnnouncementForm)
class JobAnnouncementFormAdmin(admin.ModelAdmin):
    list_display = ('role_title', 'company', 'sector', 'ctc_display', 'cgpa_cutoff', 'hiring_slot', 'is_active')
    list_filter = ('sector', 'hiring_slot', 'is_active')
    search_fields = ('role_title', 'company__name', 'description')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'jaf', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('student__roll_number', 'student__full_name', 'jaf__company__name', 'jaf__role_title')


@admin.register(InterviewSlot)
class InterviewSlotAdmin(admin.ModelAdmin):
    list_display = ('student', 'jaf', 'round_name', 'interview_date', 'interview_time', 'slot_display', 'status')
    list_filter = ('slot_display', 'status')


@admin.register(PlacementAnnouncement)
class PlacementAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'tag_type', 'author', 'created_at')
    list_filter = ('tag_type', 'tag')
    search_fields = ('title', 'content')
