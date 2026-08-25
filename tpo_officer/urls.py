from django.urls import path
from . import views

app_name = 'tpo_officer'

urlpatterns = [
    path('dashboard/', views.tpo_dashboard, name='dashboard'),
    path('students/verify/', views.verify_students, name='verify_students'),
    path('students/approve/<int:student_id>/', views.approve_single_student, name='approve_single_student'),
    path('students/decline/<int:student_id>/', views.decline_single_student, name='decline_single_student'),
    path('students/hold/<int:student_id>/', views.hold_single_student, name='hold_single_student'),
    path('students/unhold/<int:student_id>/', views.unhold_single_student, name='unhold_single_student'),
    path('jafs/', views.all_jafs_view, name='all_jafs'),
    path('jafs/<int:jaf_id>/applicants/', views.jaf_applicants_view, name='jaf_applicants'),
    path('jafs/approve/<int:jaf_id>/', views.approve_jaf, name='approve_jaf'),
    path('jafs/reject/<int:jaf_id>/', views.reject_jaf, name='reject_jaf'),
    path('companies/', views.companies_view, name='companies'),
    path('analytics/', views.placement_analytics, name='analytics'),
    path('profile/', views.tpo_profile_view, name='profile'),
    path('registration-setup/', views.tpo_registration_setup_view, name='registration_setup'),
    path('api/leadership/save/', views.api_save_leadership_member, name='api_save_leadership_member'),
    path('api/leadership/delete/', views.api_delete_leadership_member, name='api_delete_leadership_member'),
    path('api/toggle-phase/', views.api_toggle_placement_phase, name='api_toggle_phase'),
]
