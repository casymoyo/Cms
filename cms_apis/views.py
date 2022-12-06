from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import generics
from . serializers import DebtorSerializer, ProductSerializer
from rest_framework.response import Response
from base.models import Debtor, Product


# def debtor(request, pk):
#     try:
#         deb = Debtor.objects.get(pk=pk)
#     except Debtor.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = DebtorSerializer(deb)
#         return Response(serializer.data)

class DebtorstList(generics.ListCreateAPIView):
    queryset = Debtor.objects.all()
    serializer_class = DebtorSerializer

class DebtorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Debtor.objects.all()
    serializer_class = DebtorSerializer

class ProductstList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer