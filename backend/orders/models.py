from django.db import models


class Order(models.Model):
    price_usd = models.DecimalField(
        verbose_name='стоимость, $', decimal_places=2, max_digits=8, default=0.0
    )
    price_rub = models.DecimalField(
        verbose_name='стоимость, руб', decimal_places=2, max_digits=10, default=0.0
    )
    delivery_term = models.DateField(
        verbose_name='срок поставки', null=True, default=None
    )

    class Meta:
        verbose_name = 'поставка'
        verbose_name_plural = 'поставки'
