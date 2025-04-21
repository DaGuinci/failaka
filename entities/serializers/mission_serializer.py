from rest_framework import serializers

from entities.models import Mission

class MissionSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    # notables_name = serializers.SerializerMethodField()

    class Meta:
        model = Mission
        fields = '__all__'
        read_only_fields = ['author']  # Rend le champ 'author' en lecture seule

    def create(self, validated_data):
        return Mission.objects.create(**validated_data)

    def get_author_name(self, obj):
        if obj.author:
            name = obj.author.first_name + ' ' + obj.author.last_name
            return name
        return None

    # def get_notables_name(self, obj):
    #     notables_names = []
    #     if obj.notables:
    #         for notable in obj.notables.all():
    #             if notable.first_name and notable.last_name:
    #                 name = notable.first_name + ' ' + notable.last_name
    #                 notables_names.append(name)
    #         return notables_names
    #     return None

    def __str__(self):
        return self.name