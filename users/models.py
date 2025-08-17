from datetime import date

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from materials.models import Course, Lesson


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("У пользователя должна быть почта")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="почта", help_text="Введите почту"
    )

    phone = models.CharField(
        max_length=35,
        verbose_name="телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="аватар",
        blank=True,
        null=True,
        help_text="Загрузите аватар",
    )
    town = models.CharField(
        max_length=35,
        verbose_name="город",
        blank=True,
        null=True,
        help_text="Введите название города",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    payment_date = models.DateField(default=date.today, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный курс",
        blank=True,
        null=True,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный урок",
        blank=True,
        null=True,
    )
    payment_amount = models.DecimalField(
        decimal_places=2, max_digits=20, verbose_name="Сумма"
    )
    PAYMENT_CHOICES = [
        ("BANK_TRANSFER", "Банковский перевод"),
        ("CASH", "Наличными"),
    ]
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_CHOICES, verbose_name="Способ оплаты"
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID сессии",
    )

    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

        def __str__(self):
            return f"{self.user} {self.payment_method()} {self.payment_amount}"
