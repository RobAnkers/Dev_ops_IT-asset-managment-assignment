#apps.py

from django.apps import AppConfig

# Define an application configuration class for the 'inventory' app


class InventoryConfig(AppConfig):
    # Set the default primary key type for models in this app to BigAutoField
    default_auto_field = "django.db.models.BigAutoField"
    # Set the name of the app
    name = "inventory"
