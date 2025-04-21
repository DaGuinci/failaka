from rest_framework import serializers
from entities.models import Item

class ItemSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    site_name = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['author']  # Rend le champ 'author' en lecture seule

    def create(self, validated_data):
        return Item.objects.create(**validated_data)

    def get_author_name(self, obj):
        if obj.author:
            name = obj.author.first_name + ' ' + obj.author.last_name
            return name
        return None
    
    def get_site_name(self, obj):
        if obj.site:
            return obj.site.name
        return None

        
    def __str__(self):
        return self.name