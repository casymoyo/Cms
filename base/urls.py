from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginpage, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logoutpage, name='logout'),

    # debtors
    path("debtors/", views.debtors, name="debtors"),
    path('debtor/<int:pk>/', views.debtor, name = 'debtor'),
    path('payment', views.payment, name = 'payment'),

    # create
    path('createDebtor', views.createDebtor, name = 'createDebtor'),
    path('createWork/<int:pk>/', views.createWork, name = 'createWork'),
    path('createProduct/<int:pk>/', views.createProduct, name = 'createProduct'),

    # update
    path('updateWork/<int:pk>/', views.updateWork, name = 'updateWork'),
    path('updateProduct/<int:pk>/', views.updateProduct, name = 'updateProduct'),
    path('updatePayment/<int:pk>/', views.updatePayment, name = 'updatePayment'),

    # overdues
    path('overdues/', views.overdues, name='overdues'),
    path('overdues/firstOverdues', views.firstOverdues, name='firstOverdues'),
    path('overdues/secondOverdues', views.secondOverdues, name='secondOverdues'),
    path('overdues/finalOverdues', views.finalOverdues, name='finalOverdues'),

]
