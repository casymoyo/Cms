from django.contrib import admin
from . models import Debtor, Work, Product, User

admin.site.register(User)
admin.site.register(Debtor)
admin.site.register(Work)
admin.site.register(Product)
