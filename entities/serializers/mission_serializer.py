from rest_framework import serializers

from entities.models import Mission

class MissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mission
        fields = '__all__'
        read_only_fields = ['author']  # Rend le champ 'author' en lecture seule

    def create(self, validated_data):
        return Mission.objects.create(**validated_data)

    def __str__(self):
        return self.name