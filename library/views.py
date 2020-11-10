from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from library.models import Book, Author, Tag
from library.serializers import BooksSerializer, AuthorsSerializer, TagsSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated]
    filter_fields = ['title', 'pages']
    search_fields = ['title', 'pages']
    order_fields = ['title', 'pages', 'authors.name']


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorsSerializer
    permission_classes = [IsAuthenticated]


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticated]


def auth(request):
    return render(request, 'oauth.html')