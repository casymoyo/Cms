from rest_framework import serializers
from base.models import Debtor, Product, Work, User

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

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
