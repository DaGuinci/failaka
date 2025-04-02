from rest_framework import serializers

from entities.models import Site
from authentication.models import User

class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = '__all__'
        read_only_fields = ['author']  # Rend le champ 'author' en lecture seule

    # def validate_author(self, value):
    #     if value == '':
    #         raise serializers.ValidationError("Author cannot be empty")
    #     try:
    #         author = User.objects.get(email=value)
    #     except User.DoesNotExist:
    #         raise serializers.ValidationError("No user found with this email")
    #     return author

    def create(self, validated_data):
        return Site.objects.create(**validated_data)

    def __str__(self):
        return self.name