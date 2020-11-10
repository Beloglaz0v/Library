from django.contrib import admin
from django.contrib.admin import ModelAdmin

from library.models import Book, Author, Tag


@admin.register(Author)
class AuthorAdmin(ModelAdmin):
    list_display = ('name', 'year_of_birth')


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ('title', 'display_authors', 'display_tags')
