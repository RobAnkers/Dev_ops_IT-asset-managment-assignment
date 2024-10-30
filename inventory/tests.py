# tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import InventoryItem, Category
from django.db import IntegrityError

# Define a test case for the InventoryItem model


class InventoryItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Create test users
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user2 = User.objects.create_user(username='testuser2', password='67890')
        # Create a test category
        test_category = Category.objects.create(name='Electronics')
        # Create test inventory items
        InventoryItem.objects.create(name='Laptop', quantity=5, category=test_category, user=test_user1)
        InventoryItem.objects.create(name='Phone', quantity=10, category=test_category, user=test_user2)

    def test_inventory_item_creation(self):
        # Test the creation of an InventoryItem
        item = InventoryItem.objects.create(name='Test Item', quantity=1,
                                            category=Category.objects.get(name='Electronics'),
                                            user=User.objects.get(username='testuser1'))
        # Assert that the string representation of the item is as expected
        self.assertEqual(item.__str__(), 'Test Item')

    def test_inventory_item_update(self):
        # Test updating an InventoryItem
        item = InventoryItem.objects.get(name='Laptop')
        item.name = 'Updated Laptop'
        item.save()
        # Assert that the item's name has been updated
        self.assertEqual(item.name, 'Updated Laptop')

    def test_inventory_item_deletion(self):
        # Test deleting an InventoryItem
        item = InventoryItem.objects.get(name='Laptop')
        item.delete()
        # Assert that the item has been deleted
        items = InventoryItem.objects.filter(name='Laptop')
        self.assertEqual(len(items), 0)

    def test_category_creation(self):
        # Test the creation of a Category
        category = Category.objects.create(name='Books')
        # Assert that the string representation of the category is as expected
        self.assertEqual(category.__str__(), 'Books')

    def test_category_update(self):
        # Test updating a Category
        category = Category.objects.get(name='Electronics')
        category.name = 'Updated Electronics'
        category.save()
        # Assert that the category's name has been updated
        self.assertEqual(category.name, 'Updated Electronics')

    def test_category_deletion(self):
        # Test deleting a Category
        category = Category.objects.get(name='Electronics')
        category.delete()
        # Assert that the category has been deleted
        categories = Category.objects.filter(name='Electronics')
        self.assertEqual(len(categories), 0)

    def test_category_verbose_name_plural(self):
        # Test that the verbose_name_plural attribute of the Category model is correctly set
        self.assertEqual(Category._meta.verbose_name_plural, 'categories')

    def test_inventory_item_quantity_positive(self):
        # Test that the quantity of an InventoryItem is always positive
        item = InventoryItem.objects.create(name='Test Item', quantity=1,
                                            category=Category.objects.get(name='Electronics'),
                                            user=User.objects.get(username='testuser1'))
        # Assert that the quantity is greater than or equal to 0
        self.assertGreaterEqual(item.quantity, 0)

    def test_inventory_item_name_length_integrity_error(self):
        # Test that an IntegrityError is raised when attempting to create an
        # InventoryItem with a name exceeding the maximum length
        with self.assertRaises(IntegrityError):
            InventoryItem.objects.create(name='A' * 201, quantity=1, category=Category.objects.get(name='Electronics'),
                                         user=User.objects.get(username='testuser1'))
