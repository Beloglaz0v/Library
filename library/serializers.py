from rest_framework.serializers import ModelSerializer
from library.models import Book, Author, Tag


class AuthorsSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class TagsSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class BooksSerializer(ModelSerializer):
    # authors = AuthorsSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'