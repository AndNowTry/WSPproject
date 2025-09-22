from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)


class UserFavorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(#Product, on_delete=models.CASCADE) # доделать продукцию


class UserOrders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(#Product, on_delete=models.CASCADE) # доделать продукцию
    quantity=models.IntegerField(default=1)

