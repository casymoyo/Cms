from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from . models import Debtor, Work, Product, User

# class createUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'position', 'username', 'password1']
class debtorForm(ModelForm):
    
    class Meta:
        model = Debtor
        exclude = ("status", "user", "first_payment_date", "second_payment_date", "final_payment_date")

class workForm(ModelForm):
    
    class Meta:
        model = Work
        exclude = ("debtor", "work_id")

class productForm(ModelForm):
    
    class Meta:
        model = Product
        exclude = ("debtor", "first_payment", "second_payment", "final_payment", "product_id", "total", "is_fully_paid")
class updateProductForm(ModelForm):
    
    class Meta:
        model = Product
        exclude = ("debtor", "first_payment", "second_payment", "final_payment", "product_id", "total", "is_fully_paid")

class paymentForm(ModelForm):
    
    class Meta:
        model = Product
        exclude = ("debtor", "product", "product_sn", "product_id")

class UpdatePaymentForm(ModelForm):
    
    class Meta:
        model = Product
        exclude = ("debtor", "product", "product_sn","total", "is_fully_paid", "product_amount", "total","is_fully_paid")

class cancelForm(ModelForm):
    class Meta:
        model = Debtor
        fields = ("status",)

