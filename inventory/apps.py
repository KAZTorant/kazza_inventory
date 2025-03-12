from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.inventory'
    verbose_name = "Anbar"

    def ready(self) -> None:
        import apps.inventory.signals
        return super().ready()
