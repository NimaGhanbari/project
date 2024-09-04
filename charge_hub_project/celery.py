from charge_hub_project import settings
from charge_hub_project import celeryconfig
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'charge_hub_project.settings')
app = Celery('django_projetc')
app.config_from_object(celeryconfig)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
