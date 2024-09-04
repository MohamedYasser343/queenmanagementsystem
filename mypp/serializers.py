from rest_framework import serializers
from .models import Name, Entry

class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Name
        fields = ['id', 'name']

class EntrySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name.name')
    class Meta:
        model = Entry
        fields = ['name', 'service', 'price', 'comment']

    def create(self, validated_data):
        name_input = validated_data.pop('name')
        name_obj = Name.objects.filter(name=name_input).first()

        if not name_obj:
            raise serializers.ValidationError(f"Name '{name_input}' does not exist.")

        # Create the Entry instance
        return Entry.objects.create(name=name_obj, **validated_data)
