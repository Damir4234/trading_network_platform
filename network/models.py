from django.db import models
from django.contrib.auth.models import User


class NetworkNode(models.Model):
    LEVEL_CHOICES = [
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель'),
    ]

    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    products = models.TextField()  # Simplified for this example
    supplier = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(choices=LEVEL_CHOICES)

    def __str__(self):
        return self.name


class ActiveEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
