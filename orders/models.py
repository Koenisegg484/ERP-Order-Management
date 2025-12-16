from django.db import models
import uuid

class Product(models.Model):
    name = models.CharField(max_length=200)
    about = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    


class Inventory(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="inventory"
    )
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING="PENDING"
        CONFIRMED="CONFIRMED"
        PACKED="PACKED"
        SHIPPED="SHIPPED"
        DELIVERED="DELIVERED"
        CANCELLED="CANCELLED"
    
    ALLOWED_TRANSITIONS = {
        "PENDING": ["CONFIRMED"],
        "CONFIRMED": ["PACKED", "CANCELLED"],
        "PACKED": ["SHIPPED"],
        "SHIPPED": ["DELIVERED"],
    }
    
    order_number = models.CharField(max_length=50, unique=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=100, default="User")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number
    

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    from_status = models.CharField(max_length=20)
    to_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)