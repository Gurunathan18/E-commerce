from django.apps import AppConfig


class FirstappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'firstapp'
class YourAppConfig(AppConfig):
    name = 'firstapp'
    verbose_name = 'firstapp'

    def ready(self):
        import firstapp.signals
