from django.db import models
from django.contrib.auth.models import User


class NetworkNode(models.Model):
    LEVEL_CHOICES = [
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель'),
    ]

    name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    products = models.CharField(max_length=200)
    debt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(choices=LEVEL_CHOICES, editable=True)
    supplier = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='supplied_nodes')
    network = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.supplier:

            self.level = self.supplier.level + 1
            self.network = self.supplier.network
        else:
            self.level = 0
            if not self.network:
                self.network = self.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
