from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Order

class StatsSerializer(serializers.Serializer):
    sum_rub = serializers.FloatField(
        label='сумма отгрузок в рублях'
    )
    sum_usd = serializers.FloatField(
        label='сумма отгрузок в долларах'
    )
    overall_amt = serializers.IntegerField(
        label='общее количество отгрузок'
    )
    overdue_amt = serializers.IntegerField(
        label='количество просроченных отгрузок'
    )

    overdue_sum_usd = serializers.FloatField(
        label='сумма просроченных отгрузок в долларах'
    )
    overdue_sum_rub = serializers.FloatField(
        label='сумма просроченных отгрузок в рублях'
    )