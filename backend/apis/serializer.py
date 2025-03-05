from rest_framework import serializers
from .models import APIModel, APIModelFile

class APISerializer(serializers.ModelSerializer):
    class Meta:
        model = APIModel
        fields = '__all__'
        # fields = ['id', 'message', 'pdf', 'sender', 'created_at']
        
class APIFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIModelFile
        fields = '__all__'