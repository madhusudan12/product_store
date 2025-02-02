from django.apps import AppConfig


class MetadataStoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'metadata_store'

    def ready(self):
        import metadata_store.signals
