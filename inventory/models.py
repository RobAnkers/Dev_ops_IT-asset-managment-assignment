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
    # Field representing the category of the item
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, blank=True, null=True
    )
    # Field to store the date and time when the item was created
    date_created = models.DateTimeField(auto_now_add=True)
    # Field to track last edited date
    last_edited = models.DateTimeField(auto_now=True)
    # Field linking the item to the user who created it
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)

    # Override save method to sanitize input
    def save(self, *args, **kwargs):
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        # Only sanitize if there is potential XSS content
        if "<script>" in self.name or "<img" in self.name:
            self.name = strip_tags(self.name)  # Only strip if potentially harmful content
        super().save(*args, **kwargs)

    # Method returning a string representation of the item
    def __str__(self):
        return self.name


class Category(models.Model):
    # Field to store the name of the category
    name = models.CharField(max_length=200)

    # Sanitize input by overriding save method
    def save(self, *args, **kwargs):
        # Only sanitize if potentially harmful content exists
        if "<script>" in self.name or "<img" in self.name:
            self.name = strip_tags(self.name)  # Only strip if potentially harmful content
        super().save(*args, **kwargs)

    # Metadata for the model
    class Meta:
        # Create the plural form of the model
        verbose_name_plural = "categories"

    # Method returning a string representation of the category
    def __str__(self):
        return self.name
