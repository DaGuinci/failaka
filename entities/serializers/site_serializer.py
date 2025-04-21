from rest_framework import serializers

from entities.models import Site
from authentication.models import User

class SiteSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = '__all__'
        read_only_fields = ['author']  # Rend le champ 'author' en lecture seule

    def create(self, validated_data):
        return Site.objects.create(**validated_data)

    def get_author_name(self, obj):
        if obj.author:
            name = obj.author.first_name + ' ' + obj.author.last_name
            return name
        return None

    def __str__(self):
        return self.name