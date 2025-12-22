from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
from mptt.models import MPTTModel, TreeForeignKey
from django.core.exceptions import ValidationError
from django.urls import reverse
from urllib.parse import quote


class MainCategory(models.Model):
    """
        Самая главная категория товаров
    """
    name = models.CharField(max_length = 50)
    photo = models.ImageField(upload_to = "main_category_photos/", null = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'photo'],
                name='unique_main_category'
            )
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'level': 'second', 'name': self.name})


class SecondaryCategory(models.Model):
    """
        Вторичная категория товаров
    """
    category = models.ForeignKey(MainCategory, on_delete = models.CASCADE, related_name = "secondary_category")
    name = models.CharField(max_length = 100)
    photo = models.ImageField(upload_to = "secondary_category_photos/", null = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'name', 'photo'],
                name='unique_secondary_category'
            )
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'level': 'triple', 'name': self.name})



class TripleCategory(models.Model):
    """
        Третичная категория товаров
    """
    category = models.ForeignKey(SecondaryCategory, on_delete = models.CASCADE, related_name = "triple_category")
    name = models.CharField(max_length = 100)
    photo = models.ImageField(upload_to = "triple_category_photos/", null = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'name', 'photo'],
                name='unique_triple_category'
            )
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products', kwargs={'name': self.name})

#=======================================================================================================================

class Brands(models.Model):
    """
        Динамические бренды
    """
    name = models.CharField(max_length = 100)
    photo = models.ImageField(upload_to = "brand_photos/", null = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'photo'],
                name='unique_brands'
            )
        ]

    def __str__(self):
        return self.name


class CategoryBrands(models.Model):
    """
        Бренды к категории
    """
    category = models.ForeignKey(TripleCategory, on_delete = models.CASCADE, related_name = "category_category_brands")
    brand = models.ForeignKey(Brands, on_delete = models.CASCADE, related_name = "brand_category_brands")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'brand'],
                name='unique_category_brands'
            )
        ]



class Characteristics(models.Model):
    """
        Динамические характеристики
    """
    name = models.CharField(max_length = 100)
    type = models.CharField(max_length = 30)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'type'],
                name='unique_characteristics'
            )
        ]

    def __str__(self):
        return self.name



class CategoryCharacteristics(models.Model):
    """
        Характеристики к категории
    """
    category = models.ForeignKey(TripleCategory, on_delete = models.CASCADE, related_name = "category_category_characteristics")
    characteristic = models.ForeignKey(Characteristics, on_delete = models.CASCADE, related_name = "characteristic_category_characteristics")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'characteristic'],
                name='unique_category_characteristics'
            )
        ]



class Products(models.Model):
    """
        Продукты
    """
    category = models.ForeignKey(TripleCategory, on_delete = models.CASCADE, related_name = "category_products")
    brand = models.ForeignKey(Brands, on_delete = models.CASCADE, related_name = "brand_products")

    name = models.CharField(max_length = 100, unique = True)
    price = models.DecimalField(max_digits = 12, decimal_places = 2) #0000000000.00
    description = models.TextField()
    quantity = models.PositiveIntegerField(default = 0)
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'brand', 'name'],
                name='unique_products'
            )
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'name': self.name})



class ProductCharacteristics(models.Model):
    """
        Характеристики продуктов
    """
    product = models.ForeignKey(Products, on_delete = models.CASCADE, related_name = "product_characteristics")
    characteristic = models.ForeignKey(Characteristics, on_delete = models.CASCADE, related_name = "characteristic_characteristics")

    value = models.CharField(max_length = 255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'characteristic', 'value'],
                name='unique_product_characteristics'
            )
        ]

    def clean(self):
        """
            Проверяем, что выбранная характеристика допустима для категории продукта.
        """
        if self.product and self.characteristic:
            category = self.product.category
            allowed = CategoryCharacteristics.objects.filter(category=category, characteristic=self.characteristic).exists()
            if not allowed:
                raise ValidationError({'characteristic': f"Характеристика '{self.characteristic.name}' недоступна для категории '{category.name}'"})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

#=======================================================================================================================

class Product3DModels(models.Model):
    """
        3D модели продуктов
    """
    product = models.OneToOneField(Products, on_delete = models.CASCADE, related_name = "product_3dmodels")

    file_model = models.FileField(upload_to="product_3dmodels/", null = True)
    file_model_url = models.CharField(max_length = 500, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'file_model', 'file_model_url'],
                name='unique_product_3dmodels'
            )
        ]



class ProductPhotos(models.Model):
    """
        Фотки продуктов
    """
    product = models.ForeignKey(Products, on_delete = models.CASCADE, related_name = "product_photos")

    photo = models.ImageField(upload_to="product_photos/", null=True)
    photo_url = models.CharField(max_length = 500, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'photo', 'photo_url'],
                name='unique_product_photos'
            )
        ]

    def __str__(self):
        return self.product.name





class ProductVideos(models.Model):
    """
        Видео продуктов
    """
    product = models.ForeignKey(Products, on_delete = models.CASCADE, related_name = "product_videos")

    video = models.FileField(upload_to = "product_videos/", null=True)
    video_url = models.CharField(max_length = 500, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'video', 'video_url'],
                name='unique_product_videos'
            )
        ]



class Promotions(models.Model):
    """
        Акции продуктов
    """
    product = models.ForeignKey(Products, on_delete = models.CASCADE, related_name = "product_promotions")

    name = models.CharField(max_length = 100)
    promo_photo = models.ImageField(upload_to = "promo_photos/")
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'name', 'promo_photo'],
                name='unique_product_promotions'
            )
        ]

    def clean(self):
        if self.end_datetime < self.start_datetime:
            raise ValidationError("Дата окончания акции не может быть раньше даты начала")

    def __str__(self):
        return "Скидки" + self.product.name



"""
class Comments(MPTTModel):
    product = models.ForeignKey(Products, on_delete = models.CASCADE, related_name = "product_comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    likes = models.PositiveIntegerField()
    dislikes = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_updated = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        ordering = ['tree_id', 'lft']
"""
