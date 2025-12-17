from django.test import TestCase
from products.models import Product, Inventory

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Sample", price=20.0, sku="SMP01", about="Sample Product")
        self.inventory = Inventory.objects.create(product=self.product, quantity=50)

    def test_inventory_linked_to_product(self):
        self.assertEqual(self.inventory.product, self.product)
        self.assertEqual(self.inventory.quantity, 50)
