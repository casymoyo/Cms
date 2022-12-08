from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser
from datetime import datetime, date, time, timedelta
import datetime
import uuid

gender = (
    ('Male','MALE'),
    ('female','FEMALE'),
)
#System User
class User(AbstractUser):
    # email = models.EmailField(unique=True, max_length=254, null = True, blank = True)
    position = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile', blank = True, default = 'profile/avatar.svg')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username
        
#Debtor
class Debtor(models.Model):
    user = models.ForeignKey("base.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    maiden = models.CharField(max_length=50, null = True, blank = True)
    surname = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices = gender)
    address = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=10)
    id_number = models.CharField(max_length=14)
    status = models.CharField(max_length=50, default = '', blank = True )
    created = models.DateField(auto_now_add=True)
    is_fully_paid = models.CharField(max_length=50, default = 'no', null=True, blank = True)
    first_payment_date = models.DateField(default = date.today() + timedelta(days=30), null = True)
    second_payment_date = models.DateField(default = date.today() + timedelta(days=60), null = True)
    final_payment_date = models.DateField(default = date.today() + timedelta(days=90), null = True)
   
    @property
    def due_in_thirty(self):
        debtor_due = Debtor.objects.filter(first_payment_date__lte = date.today()) & Debtor.objects.filter(product__first_payment__lte = 0)
        return debtor_due

    @property
    def due_in_sixty(self):
        debtor_due = Debtor.objects.filter(second_payment_date__lte = date.today()) & Debtor.objects.filter(product__second_payment__lte = 0) 
        return debtor_due
    
    @property
    def due_in_ninety(self):
        debtor_due = Debtor.objects.filter(final_payment_date__lte = date.today())& Debtor.objects.filter(product__final_payment__lte = 0)
        return debtor_due
    
    @property
    def total(self):
        debtor_thirty_amounts = Debtor.objects.aggregate(Sum('product__first_payment'))
        debtor_sixty_amounts = Debtor.objects.aggregate(Sum('product__second_payment')) 
        debtor_final_amounts = Debtor.objects.aggregate(Sum('product__final_payment')) 

        return debtor_thirty_amounts, debtor_sixty_amounts, debtor_final_amounts

    def __str__(self):
        return self.name
    
 
    
#work
class Work(models.Model):
    debtor = models.OneToOneField("base.Debtor", on_delete=models.CASCADE, primary_key=True)
    employer = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    employer_contact = models.CharField(max_length=50)

    def __str__(self):
        return self.employer

#Product
class Product(models.Model):
    debtor = models.OneToOneField("base.Debtor", on_delete=models.CASCADE, primary_key=True)
    product = models.CharField(max_length=50)
    product_sn = models.CharField(max_length=50)
    product_amount = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True, default= 0)
    deposit = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True, default= 0)
    product_details = models.CharField(max_length= 100)
    first_payment = models.DecimalField(max_digits=5, decimal_places=2,  default= 0)
    second_payment = models.DecimalField(max_digits=5, decimal_places=2,   default= 0)
    final_payment = models.DecimalField(max_digits=5, decimal_places=2, default= 0)
    total = models.DecimalField(max_digits=5, decimal_places=2, blank = True, null = True, default= 0)
    created = models.DateField(auto_now_add=True, null = True)
    updated = models.DateField(auto_now=True, null = True)

    def __str__(self):
        return self.product
    