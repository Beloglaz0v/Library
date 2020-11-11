from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from library.models import Book, Author, Tag
from library.serializers import BooksSerializer, AuthorsSerializer, TagsSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated]
    # filter_fields = ['title', 'pages']
    # search_fields = ['title', 'pages']
    # order_fields = ['title', 'pages']

    @action(detail=True, methods=["GET"])
    def authors(self, request, pk=None):
        book = self.get_object()
        authors = Author.objects.filter(book=book)
        serializer = AuthorsSerializer(authors, many=True)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["GET"])
    def tags(self, request, pk=None):
        book = self.get_object()
        tags = Tag.objects.filter(book=book)
        serializer = AuthorsSerializer(tags, many=True)
        return Response(serializer.data, status=200)


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorsSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["GET"])
    def books(self, request, pk=None):
        author = self.get_object()
        books = Book.objects.filter(author=author)
        serializer = BooksSerializer(books, many=True)
        return Response(serializer.data, status=200)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticated]


def auth(request):
    return render(request, 'oauth.html')