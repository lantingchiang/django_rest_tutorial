from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


"""
class SnippetSerializer(serializers.Serializer):
    # DEFINE FIELDS THAT GET SERIALIZED
    id = serializers.IntegerField(read_only=True)
    # allow_blank is only used for CharField, makes "" a valid entry
    title = serializers.CharField(required=False, allow_blank=True)
    code = serializers.CharField(style={"base_template": "textarea.html"})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default="python")
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default="friendly")

    def create(self, validated_data):
        # Creates and returns new Snippet instance from validated data
        # ** unpackes/flattens the keyword argument (dictionary) to its values
        # Creates new instance but doesn't save it
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update and return existing snippet instance from validated data
        # validated_data is ordered dict; .get() gets the value for given key
        # .get() returns instance.title is validated_data['title'] doesn't exist
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        # updates existing instance
        instance.save()
        return instance
"""


class SnippetSerializer(serializers.ModelSerializer):
    # has default create() & update() methods
    class Meta:
        model = Snippet
        fields = ["id", "title", "code", "linenos", "language", "style"]
