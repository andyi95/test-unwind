from django.shortcuts import render
from .serializers import OrderSerializer, StatsSerializer
from .models import Order
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models import Sum, Count, Q
from datetime import date
from .tasks import update_tables


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (AllowAny, )

    @action(('post', ), detail=False)
    def update_data(self, request):
        """Обновить """
        update_tables.delay()
        return Response()

    @action(('get', ), detail=False)
    def stats(self, request):
        """Получение общей статистики по отгрузкам."""
        overdue_f = Q(delivery_term__lt=date.today())
        qs = Order.objects.aggregate(
            sum_rub=Sum('price_rub'),
            sum_usd=Sum('price_usd'),
            overall_amt=Count('id'),
            overdue_amt=Count('id', filter=overdue_f),
            overdue_sum_usd=Sum('price_usd', filter=overdue_f),
            overdue_sum_rub=Sum('price_rub', filter=overdue_f)
        )
        serializer = StatsSerializer(qs, many=False, read_only=True)
        return Response(serializer.data)
