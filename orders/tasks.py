from celery import shared_task

@shared_task
def order_created(order_id):
    print(f"Order {order_id} created")