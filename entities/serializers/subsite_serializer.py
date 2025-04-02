from rest_framework import serializers

from entities.models import Subsite
from authentication.models import User

class SubsiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subsite
        fields = '__all__'
        read_only_fields = ['author']  # Rend le champ 'author' en lecture seule

    def create(self, validated_data):
        return Subsite.objects.create(**validated_data)

    def __str__(self):
        return self.name