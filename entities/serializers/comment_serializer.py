from rest_framework import serializers

from entities.models import Comment

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author']  # Rend le champ 'author' en lecture seule

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def __str__(self):
        return self.name