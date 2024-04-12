from rest_framework import serializers
from .models import *

class EventdataSerializers(serializers.ModelSerializer):
    class Meta:
        model = Eventdata
        fields = '__all__'