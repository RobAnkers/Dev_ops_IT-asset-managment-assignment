# admin.py

from django.contrib import admin
from .models import InventoryItem, Category
# Registering models with Django admin site

# Custom admin class for InventoryItem


class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'category', 'date_created', 'user')
    readonly_fields = ('date_created', 'last_edited')
# Register the InventoryItem model with the admin site


admin.site.register(InventoryItem, InventoryItemAdmin)
# Register the Category model with the admin site
admin.site.register(Category)
