from django.urls import path
from . import views

app_name = 'recruiters'

urlpatterns = [
    path('dashboard/', views.recruiter_dashboard, name='dashboard'),
    path('roadmap/', views.hiring_roadmap_view, name='roadmap_default'),
    path('roadmap/<int:jaf_id>/', views.hiring_roadmap_view, name='roadmap'),
    path('process/configure/<int:jaf_id>/', views.configure_hiring_process_view, name='configure_process'),
    path('process/update-round/<int:round_id>/', views.update_round_status, name='update_round_status'),
    path('process/delete-round/<int:round_id>/', views.delete_round_view, name='delete_round'),
    path('pipeline/', views.recruitment_pipeline, name='pipeline'),
    path('companies/', views.company_list_view, name='company_list'),
    path('jaf/create/', views.create_jaf, name='create_jaf'),
    path('jaf/edit/<int:jaf_id>/', views.edit_jaf_view, name='edit_jaf'),
    path('jaf/delete/<int:jaf_id>/', views.delete_jaf_view, name='delete_jaf'),
    path('jaf/deleted/', views.deleted_jaf_list_view, name='deleted_jafs'),
    path('jaf/restore/<int:jaf_id>/', views.restore_jaf_view, name='restore_jaf'),
    path('jaf/permanent-delete/<int:jaf_id>/', views.permanent_delete_jaf_view, name='permanent_delete_jaf'),
    path('applicants/<int:jaf_id>/', views.view_applicants, name='applicants'),
    path('applicants/<int:jaf_id>/shortlist-eligible/', views.shortlist_eligible_candidates, name='shortlist_eligible'),
    path('register/', views.recruiter_register_view, name='register'),
    path('profile/', views.recruiter_profile_view, name='profile'),
    path('api/send-otp/', views.api_recruiter_send_otp, name='api_send_otp'),
    path('api/verify-otp/', views.api_recruiter_verify_otp, name='api_verify_otp'),
    path('applicant/update-status/<int:app_id>/', views.update_applicant_status, name='update_applicant_status'),
]
