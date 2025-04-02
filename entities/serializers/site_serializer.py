from rest_framework import serializers

from entities.models import Site
from authentication.models import User

class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = '__all__'
        read_only_fields = ['author']  # Rend le champ 'author' en lecture seule

    def create(self, validated_data):
        return Site.objects.create(**validated_data)

    def __str__(self):
        return self.name