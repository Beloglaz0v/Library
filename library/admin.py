from django.contrib import admin
from django.contrib.admin import ModelAdmin

from library.models import Book, Author, Tag


@admin.register(Book)
class BookAdmin(ModelAdmin):
    pass


@admin.register(Author)
class BookAdmin(ModelAdmin):
    pass


@admin.register(Tag)
class BookAdmin(ModelAdmin):
    pass
