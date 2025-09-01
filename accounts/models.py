from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator,FileExtensionValidator
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    user_role=(
        ('user','User'),
        ('seller','Seller'),
        ('admin','Admin'),
    )
    user_type= models.CharField(max_length=10,choices=user_role,default='user')
    user_profile=models.ImageField(
        upload_to='user_images', 
        default='null',
        blank=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg','webp'])]
        )
    seller_profile=models.ImageField(
        upload_to='seller_images', 
        default='null',
        blank=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg','webp'])]
        )


    mobile = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r'^\+91\s?\d{10}$', 'Enter a valid mobile number with country code.')],
        verbose_name='Mobile Number'
    )
    
    address = models.TextField(
        max_length=150,
        blank=False,
        verbose_name='Address'
    )
    username = models.CharField(
        max_length=150,  # You can change this if needed
        unique=True, 
        blank=False, 
        null=False,
        validators=[RegexValidator(r'^[a-zA-Z][a-zA-Z0-9]*$','Username only starts with alphabetic characters')]
    )
    first_name = models.CharField(
        max_length=50, 
        blank=False,
        validators=[RegexValidator(r'^[a-zA-Z]+$', 'Only alphabetic characters are allowed.')]
    )
    last_name = models.CharField(
        max_length=50, 
        blank=False,
        validators=[RegexValidator(r'^[a-zA-Z]+$', 'Only alphabetic characters are allowed.')]
        )
    email = models.EmailField(
        blank=False, 
        unique=True)
    is_active = models.BooleanField(default=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mobile']  
    
    def __str__(self):
        return self.username

class Products(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'seller'})
    image=models.ImageField(upload_to='product_images/')
    product_name=models.CharField(max_length=25,
        validators=[RegexValidator(r'^[a-zA-Z][a-zA-Z]*$','Enter a valid product name.')]
    )
    colour=models.CharField(max_length=20,
        validators=[RegexValidator(r'^[a-zA-Z][a-zA-Z]*$','Enter a valid colour.')]
    )
    description=models.CharField(max_length=200,
        validators=[RegexValidator(r'^[a-zA-Z0-9\s.,-]*$','Only alphanumeric characters and certain punctuation are allowed.')]
    )
    price=models.PositiveIntegerField()
    discount=models.PositiveIntegerField(max_length=3,
        validators=[RegexValidator(r'^\d{1,2}%?$', 'Enter a valid discount amount.')]
    )
    delivery_charge=models.PositiveIntegerField()
    stock=models.PositiveIntegerField()

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'user'})
    products=models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    # date_time=models.DateTimeField(default=timezone.now)

    def total_price(self):
        return self.products.price * self.quantity
    
    def delivery_charge_total(self):
        return self.total_price() + self.products.delivery_charge
    
    def discount_price(self):
        discount = self.products.discount
        total = self.total_price()
        return int(total - (total * discount / 100))
    
    def total_amount(self):
        return self.discount_price() + (self.products.delivery_charge)

class PlaceOrder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'user'})
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    quantity= models.IntegerField()
    price=models.IntegerField()
    door_no=models.CharField(max_length=10)
    street_name=models.CharField(max_length=20)
    city_name=models.CharField(max_length=20)
    zip_code=models.IntegerField(null=True,blank=True)
    mobile=models.CharField(max_length=14,
        validators=[RegexValidator(r'^\+91\s\d{10}$', 'Enter a valid mobile number with country code.')],
        verbose_name='Mobile Number')
    district=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    country=models.CharField(max_length=20,default='India')
    payment_method = models.CharField( max_length=20,
        choices=[('Cash on Delivery', 'Cash on Delivery'), ('Credit or Debit', 'Credit or Debit'),
                 ('UPI Payment','UPI Payment')]
    )
    date_time = models.DateTimeField(auto_now_add=True)

    def delivery_charge_total(self):
        return (self.product.price * self.quantity) + self.product.delivery_charge

    def discount_price(self):
        discount = self.product.discount
        total = self.product.price * self.quantity
        return int(total * discount / 100)
    
    def total_amount(self):
        discount = self.product.discount
        total = self.product.price * self.quantity
        discounted_price = int(total - (total * discount / 100))
        return discounted_price + self.product.delivery_charge
