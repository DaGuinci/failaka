from rest_framework.serializers import (
    ModelSerializer,
    )

from entities.models import Site
# import user
from authentication.models import User

class SiteSerializer(ModelSerializer):

    class Meta:
        model = Site
        fields = [
            'uuid',
            'author',
            'name',
            'type',
            'description',
            'keywords',
            'chrono',
            'location',
            'location_name',
            'geology',
            'geo_description',
            'historio',
            'justification'
        ]

    def validate_author(self, value):
        if value == '':
            raise serializers.ValidationError("Author cannot be empty")
        author= User.objects.get(email=value)
        return author

    def create(self, validated_data):
        # get author user
        author = User.objects.get(email=validated_data['author'])
        validated_data['author'] = author
        return Site.objects.create(**validated_data)

    def __str__(self):
        return self.name