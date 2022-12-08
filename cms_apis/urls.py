from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    #debtors apis
    path('debtors', views.DebtorstList.as_view()),
    path('debtorApi/<int:pk>/', views.DebtorDetail.as_view()),
    
    #product apis
    path('products', views.ProductstList.as_view()),
    path('productApi/<int:pk>/', views.ProductDetail.as_view()),

    #work apis
    path('work/', views.WorkList.as_view()),
    path('workApi/<int:pk>/', views.WorkDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
