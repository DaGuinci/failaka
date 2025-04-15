from rest_framework import serializers

from entities.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    item_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author']  # Rend le champ 'author' en lecture seule

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
    
    def get_author_name(self, obj):
        if obj.author:
            name = obj.author.first_name + ' ' + obj.author.last_name
            return name
        return None
    
    def get_item_name(self, obj):
        if obj.item:
            return obj.item.name
        return None

    def __str__(self):
        return self.name