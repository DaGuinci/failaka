from rest_framework import serializers

from entities.models import Item

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['author']  # Rend le champ 'author' en lecture seule

    def create(self, validated_data):
        return Item.objects.create(**validated_data)

    def __str__(self):
        return self.name