from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from library.models import Book, Author, Tag
from library.serializers import BooksSerializer, AuthorsSerializer, TagsSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_fields = ['title', 'pages']
    search_fields = ['title', 'pages']
    order_fields = ['title', 'pages']

    @action(detail=True, methods=["GET"])
    def authors(self, request, pk=None, tag_pk=None):
        book = self.get_object()
        authors = Author.objects.filter(books=book)
        serializer = AuthorsSerializer(authors, many=True)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["GET"])
    def tags(self, request, pk=None, author_pk=None):
        book = self.get_object()
        tags = Tag.objects.filter(book=book)
        serializer = TagsSerializer(tags, many=True)
        return Response(serializer.data, status=200)


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'year_of_birth']
    order_fields = ['name', 'year_of_birth']
    filter_fields = ['name', 'year_of_birth', 'books']

    @action(detail=True, methods=["GET"])
    def books(self, request, pk=None,):
        author = self.get_object()
        books = Book.objects.filter(author=author,)
        serializer = BooksSerializer(books, many=True)
        return Response(serializer.data, status=200)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["GET"])
    def books(self, request, pk=None):
        tag = self.get_object()
        books = Book.objects.filter(tags=tag)
        serializer = BooksSerializer(books, many=True)
        return Response(serializer.data, status=200)


class SearchBooks(ModelViewSet):
    serializer_class = BooksSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        tags = self.request.query_params.get('tags', None)
        if tags:
            tags = tags.split(',')
            queryset = Book.objects.filter(tags__in=tags)
        return queryset
