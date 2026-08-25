import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_core.settings')
django.setup()
from tpo_officer.models import TPOProfile

TPOProfile.objects.all().update(is_active_head=False)
prof_s = TPOProfile.objects.filter(full_name__icontains='Bhattacharya').first()
if prof_s:
    prof_s.is_active_head = True
    prof_s.save()
    print('Prof. S. Bhattacharya set as active head!')
