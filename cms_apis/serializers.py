from rest_framework import serializers
from base.models import Debtor, Product, Work

class DebtorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Debtor
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"

class WorkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Work
        fields = "__all__"