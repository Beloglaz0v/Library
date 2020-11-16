from collections import OrderedDict

from django.test import TestCase

from library.models import Book, Author
from library.serializers import BooksSerializer, AuthorsSerializer


class BookSerializerCase(TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(title='Book 1', pages=226)
        book_2 = Book.objects.create(title='Book 2', pages=1226)
        data = BooksSerializer([book_1, book_2], many=True).data
        expexcted_data = [
            OrderedDict(
                [
                    ('id', book_1.id),
                    ('title', 'Book 1'),
                    ('pages', 226),
                    ('tags', [])
                ]),
            OrderedDict(
                [
                    ('id', book_2.id),
                    ('title', 'Book 2'),
                    ('pages', 1226),
                    ('tags', [])
                ])]
        self.assertEqual(expexcted_data, data)


class AuthorSerializerCase(TestCase):
    def test_ok(self):
        author_1 = Author.objects.create(name='Author 1', year_of_birth=1226)
        author_2 = Author.objects.create(name='Author 2', year_of_birth=1926)
        author_1.books.create(title='Book 1', pages=226)
        data = AuthorsSerializer([author_1, author_2], many=True).data
        expexcted_data = [
            OrderedDict(
                [
                    ('id', author_1.id),
                    ('name', 'Author 1'),
                    ('year_of_birth', 1226),
                    ('books', [author_1.books.get().id]),
                ]),
            OrderedDict(
                [
                    ('id', author_2.id),
                    ('name', 'Author 2'),
                    ('year_of_birth', 1926),
                    ('books', []),
                ])]
        self.assertEqual(expexcted_data, data)
