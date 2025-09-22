from django.db import models

# Create your models here.
class Product(models.Model):

    CATEGORY_CHOICES = [
        ('RUB', 'Рубли'),
        ('USD', 'Доллары'),
    ]

    name = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=12, decimal_places=2) # макс 9 миллиард
    currency = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=False)




