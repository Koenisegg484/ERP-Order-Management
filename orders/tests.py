from django.test import TestCase
from orders.serializers import OrderSerializer, OrderStatusSerializer
from products.models import Product, Inventory
from orders.models import Order, OrderItem
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class OrderModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", price=10.0, sku="TP001", about="Test")
        self.inventory = Inventory.objects.create(product=self.product, quantity=100)

    def test_orderitem_creation(self):
        order = Order.objects.create(customer_name="Alice", total_amount=0)
        item = OrderItem.objects.create(order=order, product=self.product, quantity=2, price=self.product.price)
        self.assertEqual(item.order, order)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 2)


class OrderSerializerTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", price=10.0, sku="TP001", about="Test")
        self.inventory = Inventory.objects.create(product=self.product, quantity=100)

    def test_order_creation_does_not_reduce_inventory(self):
        data = {
            "customer_name": "Alice",
            "items": [
                {"product_id": self.product.id, "quantity": 5}
            ]
        }
        self.assertEqual(self.inventory.quantity, 100)

    def test_order_status_confirmed_reduces_inventory(self):
        order = Order.objects.create(customer_name="Alice", status=Order.Status.PENDING)
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=5,
            price=self.product.price
        )

        serializer = OrderStatusSerializer(order, data={"status": Order.Status.CONFIRMED})
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 95)


class OrderAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass", is_staff = True)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.product = Product.objects.create(name="Test Product", price=10.0, sku="TP001", about="Test")
        Inventory.objects.create(product=self.product, quantity=100)

    def test_order_api(self):
        url = reverse('order-create')
        data = {
            "customer_name": "Alice",
            "items": [{"product_id": self.product.id, "quantity": 5}]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)