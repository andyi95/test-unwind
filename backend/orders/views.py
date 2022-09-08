from datetime import date

from django.db.models import Count, Q, Sum
from django.db.models.functions import Coalesce
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer, StatsSerializer
from .tasks import update_tables


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (AllowAny, )

    @extend_schema(request=None, responses={201: None})
    @action(('post', ), detail=False)
    def update_data(self, request):
        """Обновить """
        update_tables.delay()
        return Response(status=status.HTTP_201_CREATED)

    @action(('get', ), detail=False)
    def stats(self, request):
        """Получение общей статистики по отгрузкам."""
        overdue_f = Q(delivery_term__lt=date.today())
        qs = Order.objects.aggregate(
            sum_rub=Coalesce(Sum('price_rub'), 0.0),
            sum_usd=Coalesce(Sum('price_usd'), 0.0),
            overall_amt=Coalesce(Count('id'), 0),
            overdue_amt=Coalesce(Count('id', filter=overdue_f), 0),
            overdue_sum_usd=Coalesce(Sum('price_usd', filter=overdue_f), 0.0),
            overdue_sum_rub=Coalesce(Sum('price_rub', filter=overdue_f), 0.0)
        )
        serializer = StatsSerializer(qs, many=False, read_only=True)
        return Response(serializer.data)
