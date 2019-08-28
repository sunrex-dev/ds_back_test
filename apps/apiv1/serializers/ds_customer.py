from rest_framework import serializers
from apps.ds.models import Customer

class DsCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields = '__all__'
