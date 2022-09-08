from django.urls import include, path
from rest_framework import routers

from orders.views import OrderViewSet

order_router = routers.DefaultRouter()
order_router.register('orders', OrderViewSet)

urlpatterns = [
    path('', include(order_router.urls)),
]