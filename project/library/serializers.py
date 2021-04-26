from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=500)
    image = serializers.FileField()
    pdf_file = serializers.FileField()