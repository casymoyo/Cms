from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    #debtors apis
    path('debtors', views.DebtorstList.as_view()),
    path('debtor/<int:pk>/', views.DebtorDetail.as_view()),
    
    #product apis
    path('products', views.ProductstList.as_view()),
    path('product/<int:pk>/', views.ProductDetail.as_view()),

    #work apis
    path('works/', views.WorkList.as_view()),
    path('work/<int:pk>/', views.WorkDetail.as_view()),

    #user apis
    path('users/', views.UserList.as_view()),
    path('user/<int:pk>/', views.UserDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
