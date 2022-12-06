from rest_framework import serializers
from base.models import Debtor, Product

class DebtorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Debtor
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"