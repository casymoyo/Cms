from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.loginpage, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logoutpage, name='logout'),

    #users
    path('userManagement/', views.userManagement, name='userManagement'),
    path('createUser/', views.createUser, name='createUser'),

    # debtors
    path("debtors", views.debtors, name="debtors"),
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

    # cancel
    path('cancelledDebtors/', views.cancelledDebtorList, name='cancelledDebtorList'),
    path('cancelDebtor/<int:pk>/', views.cancelDebtor, name='cancelDebtor'),
    path('revertCancellation/<int:pk>', views.revertCancellation, name='revertCancellation'),
    path('deleteDebtor/<int:pk>/', views.deleteDebtor, name='deleteDebtor'),

    #user 
    path('userDebtors/<int:pk>/', views.userDebtors, name ='userDebtors'),
    path('userSettings/<int:pk>/', views.userSettings, name ='userSettings'),
    path('updateUser/<int:pk>/', views.updateUser, name ='updateUser')
]
urlpatterns = format_suffix_patterns(urlpatterns)
