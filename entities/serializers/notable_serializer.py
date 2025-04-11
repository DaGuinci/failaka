from rest_framework import serializers

from entities.models import Notable

class NotableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notable
        fields = '__all__'
        read_only_fields = ['author']  # Rend le champ 'author' en lecture seule

    def create(self, validated_data):
        return Notable.objects.create(**validated_data)

    def __str__(self):
        return self.name