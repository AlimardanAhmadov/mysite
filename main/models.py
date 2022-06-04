"""Declare models for YOUR_APP app."""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
#from django.utils.translation import ugettext_lazy as _
# for Django v4
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    trendyol_api_key = models.CharField(max_length=200)
    woocommerce_api_key = models.CharField(max_length=200)
    woocommerce_api_secret = models.CharField(max_length=200)
    woocommerce_sitename = models.CharField(max_length=200)
    parasut_firma_no = models.CharField(max_length=20)
    parasut_client_id = models.CharField(max_length=200)
    parasut_client_secret = models.CharField(max_length=200)
    parasut_username = models.CharField(max_length=200)
    parasut_password = models.CharField(max_length=200)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager() ## This is the new line in the User model. ##

# Create your models here.
class ToDoList(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text

class Products(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products", null=True )
    name = models.CharField(max_length=200)
    main_id = models.CharField(max_length=200)
    variation_id = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    sku = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    sale_price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    weight = models.DecimalField(max_digits=20, decimal_places=2)
    length = models.DecimalField(max_digits=20, decimal_places=2)
    height = models.DecimalField(max_digits=20, decimal_places=2)
    width = models.DecimalField(max_digits=20, decimal_places=2)
    images = ArrayField(models.CharField(max_length=500))
    color_options = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", null=True )
    date = models.CharField(max_length=1000)
    order_id = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    shipping_address = models.CharField(max_length=2000)
    shipping_city = models.CharField(max_length=30)
    shipping_state = models.CharField(max_length=30)
    name_surname = models.CharField(max_length=30)
    billing_address = models.CharField(max_length=2000)
    billing_city = models.CharField(max_length=30)
    billing_state = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    line_items = ArrayField(models.JSONField())
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    platform = models.CharField(max_length=30)
    takip_no = models.CharField(max_length=30)

    def __str__(self):
        return str(self.id)

