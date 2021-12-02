from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "itez.authentication"
    label = "itez"

class HomeConfig(AppConfig):
    name = 'home'
 
    def ready(self):
        import home.signals