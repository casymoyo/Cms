from rest_framework import serializers
from base.models import Debtor

class DebtorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Debtor
        fields = "__all__"