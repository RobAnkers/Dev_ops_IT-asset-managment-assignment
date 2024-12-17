# models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import strip_tags

# Model representing an inventory item
class InventoryItem(models.Model):
    # Field to store the name of the item
    name = models.CharField(max_length=200)
    # Field to store the quantity of the item
    quantity = models.IntegerField()

    # Foreign key to the Category model, representing the category of the item
    # on_delete=models.SET_NULL ensures that if the category is deleted, the item won't be deleted
    # but its category will be set to NULL
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, blank=True, null=True
    )
    # Field to store the date and time when the item was created
    date_created = models.DateTimeField(auto_now_add=True)
    # Field to track the last date and time the item was modified
    last_edited = models.DateTimeField(auto_now=True)
    # Foreign key to the User model to track which user created the inventory item
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Field to store the date when the item was assigned to a user
    assigned_date = models.DateTimeField(auto_now_add=True)

    # Override save method to add custom logic before saving an InventoryItem
    def save(self, *args, **kwargs):
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        # Sanitise name input if it contains potentially harmful HTML or JavaScript code
        if "<script>" in self.name or "<img" in self.name:
            self.name = strip_tags(self.name)   # Strip tags to avoid XSS
        # Call the parent class save method to actually save the item to the database
        super().save(*args, **kwargs)

    # Method returning a string representation of the item
    def __str__(self):
        return self.name

# Model representing a category for inventory items
class Category(models.Model):
    # Field to store the name of the category
    name = models.CharField(max_length=200)

    # Sanitise input by overriding save method to remove harmful content
    def save(self, *args, **kwargs):
        # Strip harmful HTML or JavaScript tags from the category name before saving
        if "<script>" in self.name or "<img" in self.name:
            self.name = strip_tags(self.name)  # Only strip if potentially harmful content
        # Call the parent class save method to save the category to the database
        super().save(*args, **kwargs)

    # Metadata for the model
    class Meta:
        # Create the plural form of the model
        verbose_name_plural = "categories"

    # Method returning a string representation of the category
    def __str__(self):
        return self.name
