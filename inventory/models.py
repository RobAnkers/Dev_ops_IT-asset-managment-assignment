# models.py
from django.db import models
from django.contrib.auth.models import User


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

    # Method returning a string representation of the item
    def __str__(self):
        return self.name


class Category(models.Model):
    # Field to store the name of the category
    name = models.CharField(max_length=200)

    # Metadata for the model
    class Meta:
        # Creat the plural form of the model
        verbose_name_plural = "categories"

    # Method returning a string representation of the category
    def __str__(self):
        return self.name
