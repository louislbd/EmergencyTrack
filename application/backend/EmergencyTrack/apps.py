from django.apps import AppConfig


class EmergencyTrackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EmergencyTrack'

    def ready(self):
        import EmergencyTrack.notifications  # Import the signals module
