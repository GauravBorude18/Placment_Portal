from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('student_dashboard/', views.dashboard, name='student_dashboard'),
    path('student/dashboard/', views.dashboard, name='student_dashboard_slash'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('jobs/', views.dashboard, name='jobs'),
    path('policy/', views.policy_view, name='policy'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.view_student_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('applications/', views.applications_view, name='applications'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('api/notifications/mark-read/<int:notif_id>/', views.api_mark_notification_read, name='api_mark_notification_read'),
    path('api/notifications/mark-all-read/', views.api_mark_all_notifications_read, name='api_mark_all_notifications_read'),
    path('api/jaf/<int:jaf_id>/', views.api_jaf_detail, name='api_jaf_detail'),
    path('api/apply/<int:jaf_id>/', views.api_apply_jaf, name='api_apply_jaf'),
    path('api/send-otp/', views.api_send_otp, name='api_send_otp'),
    path('api/verify-otp/', views.api_verify_otp, name='api_verify_otp'),
    path('api/check-email/', views.api_check_email, name='api_check_email'),
    path('api/check-credentials/', views.api_check_credentials, name='api_check_credentials'),
    path('api/pincode-lookup/<str:pincode>/', views.api_pincode_lookup, name='api_pincode_lookup'),
    path('api/student/toggle-approval/', views.api_toggle_student_approval, name='api_toggle_student_approval'),
    path('api/captcha/refresh/', views.api_refresh_captcha, name='api_refresh_captcha'),
    
    # Master Resume PDF Download Endpoint
    path('resume/<int:student_id>/download/', views.download_resume_pdf, name='download_resume'),

    # JWT Registration & ₹99 Placement Fee Services
    path('api/payment/create-order/', views.api_create_registration_jwt_order, name='api_create_registration_jwt_order'),
    path('api/payment/verify/', views.api_verify_registration_payment, name='api_verify_registration_payment'),
    path('api/razorpay/webhook/', views.razorpay_webhook_view, name='razorpay_webhook'),
    path('fee-receipt/', views.download_fee_receipt_view, name='fee_receipt'),
    path('fee-receipt/<int:receipt_id>/', views.download_fee_receipt_view, name='fee_receipt_detail'),
    path('api/tpo/export-paid-students/', views.api_tpo_export_paid_students_csv, name='api_tpo_export_paid_students_csv'),

    # Forgot Password API Endpoints
    path('api/forgot-password/request-otp/', views.api_forgot_password_request_otp, name='api_forgot_password_request_otp'),
    path('api/forgot-password/verify-otp/', views.api_forgot_password_verify_otp, name='api_forgot_password_verify_otp'),
    path('api/forgot-password/reset/', views.api_forgot_password_reset, name='api_forgot_password_reset'),

    # JWT Authentication Endpoints
    path('api/auth/token/', views.api_jwt_login, name='jwt_login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('api/auth/me/', views.api_jwt_me, name='jwt_me'),
]

