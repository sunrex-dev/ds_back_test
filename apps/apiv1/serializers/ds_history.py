from rest_framework import serializers
from apps.ds.models import History

class DsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=History
        fields = '__all__'
