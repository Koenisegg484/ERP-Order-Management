from rest_framework import serializers
from orders.tasks import order_created
from products.models import Product, Inventory
from products.serializers import ProductSerializer
from .models import Order, OrderItem, OrderHistory
from django.db import transaction

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all(),
        source = "product",
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ["product", "product_id", "quantity"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model= Order
        fields = ["id", "customer_name", "status", "created_at", "items"]
    
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            total = 0

            for item in items_data:
                product = item["product"]
                quantity = item["quantity"]
                price = product.price

                inventory = Inventory.objects.select_for_update().get(product = product)
                if inventory.quantity < quantity: 
                    raise serializers.ValidationError(f"Insufficient stock for {product.name}")

                OrderItem.objects.create(order = order, product=product, quantity = quantity, price = price)
                total += price * quantity
            order.total_amount = total
            order.save()

        transaction.on_commit(lambda: order_created.delay(order.id))
        return order

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]

    def validate_status(self, value):
        order = self.instance

        if not order:
            return value
        
        allowed = Order.ALLOWED_TRANSITIONS.get(order.status, [])

        if value not in allowed:
            raise serializers.ValidationError(
                f"Cannot move from {order.status} to {value}"
            )
        
        return value
    
    def update(self, instance, validated_data):
        new_status = validated_data["status"]
        old_status = instance.status

        with transaction.atomic():
            if old_status == Order.Status.PENDING and new_status == Order.Status.CONFIRMED:
                for item in instance.items.select_related("product"):
                    inventory = Inventory.objects.select_for_update().get(
                        product = item.product
                    )

                    if inventory.quantity < item.quantity:
                        raise serializers.ValidationError(f"Insufficient stock for {item.product.name}")
                    
                    inventory.quantity -= item.quantity
                    inventory.save()
            
            if old_status == Order.Status.CONFIRMED and new_status == Order.Status.CANCELLED:
                for item in instance.items.select_related("product"):
                    inventory = Inventory.objects.select_for_update().get(
                        product = item.product
                    )

                    inventory.quantity += item.quantity
                    inventory.save()

                OrderHistory.objects.create(
                    order=instance,
                    from_status = old_status,
                    to_status = new_status
                )
            instance.status = new_status
            instance.save()
        return instance