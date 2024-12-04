from django.test import TestCase
from django.contrib.auth.models import User
from .models import InventoryItem, Category
from datetime import datetime
from django.utils.html import escape, strip_tags

# Test cases for the Category model
class CategoryModelTests(TestCase):
    def setUp(self):
        # Create a test category for use in tests
        self.category = Category.objects.create(name="Electronics")

    def test_string_representation(self):
        # Test the string representation of the Category model
        self.assertEqual(str(self.category), "Electronics")

    def test_category_creation(self):
        # Test that the category is created with the correct name.
        self.assertEqual(self.category.name, "Electronics")

# Test cases for the InventoryItem model
class InventoryItemModelTests(TestCase):
    def setUp(self):
        # Create a test user and category
        self.user = User.objects.create_user(username="testuser", password="password123")
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
        # Test if the InventoryItem is created with correct attributes
        self.assertEqual(self.item.name, "Laptop")
        self.assertEqual(self.item.quantity, 10)
        self.assertEqual(self.item.category.name, "Electronics")
        self.assertEqual(self.item.user.username, "testuser")

    def test_auto_now_add_fields(self):
        # Test if the auto_now_add and auto_now fields work correctly populated
        self.assertTrue(isinstance(self.item.date_created, datetime))
        self.assertTrue(isinstance(self.item.last_edited, datetime))
        self.assertTrue(isinstance(self.item.assigned_date, datetime))

    def test_negative_quantity(self):
        # Attempt to create an item with a negative quantity
        item = InventoryItem(
            name="Test Item Negative Quantity",
            quantity=-1,
            category=self.category,
            user=self.user,
        )
        with self.assertRaises(ValueError):  # Now correctly triggers ValueError
            item.full_clean()
            item.save()

    def test_large_quantity(self):
        # Test that creating an item with an extremely large quantity is handled correctly
        large_quantity = 10 ** 9  # Example large number
        item = InventoryItem.objects.create(
            name="Test Large Quantity",
            quantity=large_quantity,
            category=self.category,
            user=self.user,
        )
        self.assertEqual(item.quantity, large_quantity)

# Test cases for SQL injection protection
class SQLInjectionTest(TestCase):
    def setUp(self):
        # Create a test user and category
        self.user = User.objects.create_user(username="testuser", password="password")
        self.category = Category.objects.create(name="Test Category")
        # Create a test inventory item
        self.item = InventoryItem.objects.create(
            name="Test Item",
            quantity=10,
            category=self.category,
            user=self.user,
        )

    def test_sql_injection_protection(self):
        initial_count = InventoryItem.objects.count()

        # Malicious input designed to exploit SQL injection
        malicious_input = "'; DROP TABLE inventoryitem; --"

        # Attempt to filter with malicious input
        result = InventoryItem.objects.filter(name=malicious_input)

        # Verify that no items were deleted or modified
        remaining_count = InventoryItem.objects.count()
        self.assertEqual(initial_count, remaining_count, "Database should remain unaffected by SQL injection attempt")
        self.assertFalse(result.exists(), "Malicious input should not return any results")

# Test cases for XSS (Cross-Site Scripting) protection
class XSSProtectionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.category = Category.objects.create(name="Electronics")

    def test_xss_protection_in_inventory_item(self):
        malicious_input = "<script>alert('XSS')</script>"

        item = InventoryItem.objects.create(
            name=malicious_input,
            quantity=5,
            category=self.category,
            user=self.user,
        )

        # Fetch the item from the database
        retrieved_item = InventoryItem.objects.get(id=item.id)

        # Ensure the HTML tags are stripped (i.e., stored without the <script> tag)
        stripped_name = strip_tags(retrieved_item.name)
        self.assertEqual(stripped_name, "alert('XSS')")

        # Ensure rendering in templates escapes special characters correctly
        rendered_name = escape(retrieved_item.name)
        self.assertEqual(rendered_name, "alert(&#x27;XSS&#x27;)", "The output should be HTML-escaped.")

    def test_xss_protection_in_category(self):
        malicious_input = "<img src=x onerror=alert('XSS')>"

        category = Category.objects.create(name=malicious_input)

        # Fetch the category from the database
        retrieved_category = Category.objects.get(id=category.id)

        # Ensure the HTML tags are stripped (i.e., no <img> tag is stored)
        stripped_name = strip_tags(retrieved_category.name)
        self.assertEqual(stripped_name, "", "The input should be fully sanitized.")

        # Test if rendering the name in templates escapes the input
        rendered_name = escape(retrieved_category.name)
        self.assertEqual(rendered_name, "", "The output should be an empty string because it was sanitized.")
