from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from recruiters import views as recruiter_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recruiter-register/', recruiter_views.recruiter_register_view, name='recruiter_register'),
    path('recruiter/', include('recruiters.urls')),
    path('tpo/', include('tpo_officer.urls')),
    path('', include('students.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
