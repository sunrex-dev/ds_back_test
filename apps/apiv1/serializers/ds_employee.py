from rest_framework import serializers
from apps.ds.models import Employee

class DsEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields = '__all__'
