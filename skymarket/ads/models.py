from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from users.models import User


class Ad(models.Model):

    title = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(10)],
        verbose_name="Название товара",
        help_text="Краткое название товара",
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        validators=[MinValueValidator(0)],
        verbose_name="Цена товара",
        help_text="Цена товара (только цифры)",
    )
    description = models.TextField(
        max_length=1000,
        null=True,
        verbose_name="Описание товара",
        help_text="Подробное описание товара товара",
    )
    image = models.ImageField(
        upload_to="media/",
        null=True,
        blank=True,
        verbose_name="Фото",
        help_text="Вставьте фото товара",
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):

    text = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["created_at"]

    def __str__(self):
        return self.text[:10]

