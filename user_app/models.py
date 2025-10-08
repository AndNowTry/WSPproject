from django.db import models
from django.contrib.auth.models import User
from main_app.models import Products



class Profiles(models.Model):
    """
        Профиль юзера
    """
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'user_profiles')

    avatar = models.ImageField(upload_to = 'avatars/', blank=True, null = True)
    bonuses = models.PositiveIntegerField(default = 0)
    about_user = models.TextField(default = "Пока еще пусто")




class Favorites(models.Model):
    """
        Избранное юзера
    """
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_favorites')
    product = models.ForeignKey(Products, on_delete = models.CASCADE, related_name = 'product_favorites')
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_favorites'
            )
        ]


class Comparisons(models.Model):
    """
        Сравнения юзера
    """
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_comparisons')
    product = models.ForeignKey(Products, on_delete = models.CASCADE, related_name = 'product_comparisons')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_comparisons'
            )
        ]



class Orders(models.Model):
    """
        Заказы юзера
    """
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_orders')
    product = models.ForeignKey(Products, on_delete = models.CASCADE, related_name = 'product_orders')
    address = models.CharField(max_length = 300)
    quantity = models.PositiveIntegerField(default = 1)
    is_paid = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_orders'
            )
        ]



class Purchases(models.Model):
    """
        Покупки юзера
    """
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_purchases')
    product = models.ForeignKey(Products, on_delete = models.CASCADE, related_name = 'product_purchases')
    quantity = models.PositiveIntegerField(default = 1)
    created_at = models.DateTimeField(auto_now_add = True)
    address = models.CharField(max_length = 300)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_purchases'
            )
        ]



