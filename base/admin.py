from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import Debtor, Work, Product, User

admin.site.register(User, UserAdmin)
admin.site.register(Debtor)
admin.site.register(Work)
admin.site.register(Product)
