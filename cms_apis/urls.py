from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # apis
    path('debtors', views.DebtorstList.as_view()),
    path('debtorApi/<int:pk>/', views.DebtorDetail.as_view()),
    
    path('products', views.ProductstList.as_view()),
    path('productApi/<int:pk>/', views.ProductDetail.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)
