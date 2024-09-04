from django.apps import AppConfig


class ChargeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.charge"
    
    
    def ready(self):
        import apps.charge.signals 