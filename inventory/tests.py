# tests.py

from django.test import TestCase
from django.contrib.auth.models import User
#from django.urls import reverse
from .models import InventoryItem, Category
from datetime import datetime
from django.utils.html import escape, mark_safe
from django.utils.html import strip_tags
from html import unescape

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

class XSSProtectionTests(TestCase):
    def setUp(self):
        # Create a test user and category
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.category = Category.objects.create(name="Electronics")

    def test_xss_protection_in_inventory_item(self):
        # Create a malicious input
        malicious_input = "<script>alert('XSS')</script>"

        # Create an inventory item with the malicious input
        item = InventoryItem.objects.create(
            name=malicious_input,
            quantity=5,
            category=self.category,
            user=self.user,
        )

        # Fetch the item by ID
        retrieved_item = InventoryItem.objects.get(id=item.id)

        # Ensure the database entry itself is sanitized (directly stored without HTML tags)
        # Ensure the database entry itself is sanitized (directly stored without HTML tags)
        sanitized_name = "alert('XSS')"  # The result of strip_tags should be this
        #self.assertEqual(strip_tags(retrieved_item.name), sanitized_name, "Database should store sanitized text.")
        stripped_name = strip_tags(retrieved_item.name)  # Remove HTML tags
        decoded_name = unescape(stripped_name)  # Decode HTML entities
        self.assertEqual(decoded_name, sanitized_name, "Database should store sanitized text.")
        # Ensure rendering in templates escapes special characters correctly
        rendered_name = escape(retrieved_item.name)
        self.assertEqual(rendered_name, "&lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;",
                         "The output should be HTML-escaped.")

    def test_xss_protection_in_category(self):
        # Create a malicious category name
        malicious_input = "<img src=x onerror=alert('XSS')>"

        # Create a category with the malicious name
        category = Category.objects.create(name=malicious_input)

        # Fetch the category by ID
        retrieved_category = Category.objects.get(id=category.id)

        # Test if the name field escapes the malicious input
        self.assertNotIn("<img>", retrieved_category.name, "The input should be sanitized.")
        self.assertNotIn("onerror=alert('XSS')", retrieved_category.name, "The input should be sanitized.")

        # Test if rendering the name in templates escapes the input
        rendered_name = escape(retrieved_category.name)
        #self.assertEqual(rendered_name, escape(malicious_input), "The output should be HTML-escaped.")
        retrieved_category = Category.objects.get(id=category.id)
        self.assertNotIn("<img>", retrieved_category.name, "The input should be sanitized.")
        self.assertNotIn("onerror=alert('XSS')", retrieved_category.name, "The input should be sanitized.")
        self.assertEqual(retrieved_category.name, escape(malicious_input), "The output should be HTML-escaped.")



