from django_project import settings
from django_project import celeryconfig
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
app = Celery('django_projetc')
app.config_from_object(celeryconfig)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
