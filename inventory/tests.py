# tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import InventoryItem, Category
from datetime import datetime


class CategoryModelTests(TestCase):
    def setUp(self):
        # Create a test category
        self.category = Category.objects.create(name="Electronics")

    def test_string_representation(self):
        # Test the string representation of the Category model
        self.assertEqual(str(self.category), "Electronics")

    def test_category_creation(self):
        # Test if the category is created correctly
        self.assertEqual(self.category.name, "Electronics")


class InventoryItemModelTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")
        # Create a test category
        self.category = Category.objects.create(name="Electronics")
        # Create a test inventory item
        self.item = InventoryItem.objects.create(
            name="Laptop",
            quantity=10,
            category=self.category,
            user=self.user,
        )

    def test_string_representation(self):
        # Test the string representation of the InventoryItem model
        self.assertEqual(str(self.item), "Laptop")

    def test_inventory_item_creation(self):
        # Test if the InventoryItem is created with correct values
        self.assertEqual(self.item.name, "Laptop")
        self.assertEqual(self.item.quantity, 10)
        self.assertEqual(self.item.category.name, "Electronics")
        self.assertEqual(self.item.user.username, "testuser")

    def test_auto_now_add_fields(self):
        # Test if the auto_now_add and auto_now fields work correctly
        self.assertTrue(isinstance(self.item.date_created, datetime))
        self.assertTrue(isinstance(self.item.last_edited, datetime))
        self.assertTrue(isinstance(self.item.assigned_date, datetime))


class SQLInjectionTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password")
        # Create a test category
        self.category = Category.objects.create(name="Test Category")
        # Create a test inventory item
        InventoryItem.objects.create(
            name="Test Item",
            quantity=10,
            category=self.category,
            user=self.user,
        )



def test_sql_injection_protection(self):
    """Test that the application is protected against SQL injection attempts."""
    # Create a test inventory item first
    InventoryItem.objects.create(name="Test Item", quantity=10)

    malicious_input = "'; DROP TABLE inventoryitem; --"

    # Proper way to test would be to ensure the query fails safely
    with self.assertRaises(Exception):
        # Simulate a potentially vulnerable search method
        InventoryItem.objects.filter(name=malicious_input)

    # Verify that the table and existing items remain intact
    remaining_items = InventoryItem.objects.all()
    self.assertTrue(remaining_items.exists(), "Database should remain unaffected")

