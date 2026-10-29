from rest_framework import serializers
from .models import Site,Check

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['id', 'name', 'url', 'is_active', 'created_at']

class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        exclude=['id']


