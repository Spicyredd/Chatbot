from django.apps import AppConfig
from django.apps import AppConfig
from django.core.management import call_command

class ApisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apis'
    
    def ready(self):
        print("🔄 Resetting Database on Start...")
        call_command('flush', '--noinput')
        call_command('migrate')
