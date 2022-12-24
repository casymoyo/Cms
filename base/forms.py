from django.forms import ModelForm
from . models import Debtor, Work, Product

class debtorForm(ModelForm):
    
    class Meta:
        model = Debtor
        exclude = ("status", "user", "first_payment_date", "second_payment_date", "final_payment_date")

class workForm(ModelForm):
    
    class Meta:
        model = Work
        exclude = ("debtor",)

class productForm(ModelForm):
    
    class Meta:
        model = Product
        exclude = ("debtor", "deposit", "first_payment", "second_payment", "final_payment",)

class paymentForm(ModelForm):
    
    class Meta:
        model = Product
        exclude = ("debtor", "product", "product_sn",)

