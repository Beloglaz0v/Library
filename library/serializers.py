from rest_framework.serializers import ModelSerializer
from library.models import Book, Author, Tag


class BooksSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class AuthorsSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class TagsSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
