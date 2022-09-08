import decimal
from datetime import datetime

from django.db.models import Q

from celery import shared_task

from .models import Order
from .services import CommonOrderService


@shared_task
def update_tables():
    service = CommonOrderService()
    data = service.retrieve_sheet()
    data.pop(0)
    rate = service.get_rate()
    ids = [item[1] for item in data]
    Order.objects.filter(~Q(id__in=ids)).all().delete()
    for item in data:
        order, created = Order.objects.get_or_create(id=int(item[1]))
        order.price_usd = decimal.Decimal(item[2])
        order.delivery_term = datetime.strptime(item[3], '%d.%m.%Y')
        order.price_rub = decimal.Decimal(rate) * order.price_usd
        order.save()
