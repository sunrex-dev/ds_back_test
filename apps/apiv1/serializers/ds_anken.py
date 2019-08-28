from rest_framework import serializers
from apps.ds.models import Anken

class DsAnkenSerializer(serializers.ModelSerializer):
    class Meta:
        model=Anken
        fields = '__all__'

#    def save(self, **kwargs):
#        try:
#            ds_anken = Ds_Anken.objects.get(no=self.initial_data.pop('no',None))
#            self.instance = ds_anken
#        except Ds_Anken.DoesNotExist:
#            pass
#        return super(DsAnkenSerializer, self).save(**kwargs)
