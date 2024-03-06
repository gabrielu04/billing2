from rest_framework import serializers
from .models import YourCompany


class YourCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = YourCompany
        exclude = ['user']
