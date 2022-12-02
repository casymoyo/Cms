from django.urls import path
from . import views

urlpatterns = [
    path('activity/<int:pk>/', views.activity, name = 'activity'),
    path('userActivity/<int:pk>/', views.userActivity, name = 'userActivity')
]
