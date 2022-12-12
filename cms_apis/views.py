from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import generics
from . serializers import DebtorSerializer, ProductSerializer, WorkSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import authentication, permissions
from base.models import Debtor, Product, Work, User


class DebtorstList(generics.ListCreateAPIView):
    queryset = Debtor.objects.all()
    serializer_class = DebtorSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

class DebtorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Debtor.objects.all()
    serializer_class = DebtorSerializer

    authentication_classes = [authentication.TokenAuthentication]
class ProductstList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    authentication_classes = [authentication.TokenAuthentication]
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    authentication_classes = [authentication.TokenAuthentication]
class WorkList(generics.ListCreateAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    authentication_classes = [authentication.TokenAuthentication]
class WorkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    authentication_classes = [authentication.TokenAuthentication]
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [authentication.TokenAuthentication]
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [authentication.TokenAuthentication]