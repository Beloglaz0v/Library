import json
from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from oauth2_provider.models import get_access_token_model, get_application_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils import timezone

from library.models import Book, Author, Tag
from library.serializers import BooksSerializer, AuthorsSerializer, TagsSerializer

Application = get_application_model()
AccessToken = get_access_token_model()
UserModel = get_user_model()


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1')
        self.book_1 = Book.objects.create(title='Book 1', pages=226)
        self.book_2 = Book.objects.create(title='Book 2', pages=1226)
        self.book_3 = Book.objects.create(title='Book 3', pages=126)
        self.tag_1 = Tag.objects.create(title='First', description='qeqe1')
        self.tag_2 = Tag.objects.create(title='Second', description='qeqe2')

        self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.application.save()
        self.access_token = AccessToken.objects.create(
            user=self.user,
            scope="read write",
            expires=timezone.now() + timezone.timedelta(seconds=300),
            token="secret-access-token-key",
            application=self.application
        )

    def test_get(self):
        url = reverse('books-list')
        response = self.client.get(url)
        serialazer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        pagination = OrderedDict([('count', 3), ('next', None), ('previous', None), ('results', serialazer_data)])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(pagination, response.data)

    def test_create1(self):
        url = reverse('books-list')
        data = {
            'title': 'Hi',
            'pages': 123,
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('books-list')
        data = {
            'title': 'Hi',
            'pages': 123,
            'tags': []
        }
        self.auth = "Bearer {0}".format(self.access_token.token)
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())

    def test_get_search(self):
        url = reverse('books-list')
        response = self.client.get(url, data={'search': 'book'})
        serialazer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        pagination = OrderedDict([('count', 3), ('next', None), ('previous', None), ('results', serialazer_data)])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(pagination, response.data)

    def test_update(self):
        url = reverse('books-detail', args=(self.book_1.id,))
        data = {
            'title': 'Hello',
            'tags': [self.tag_1.id],
        }
        self.auth = "Bearer {0}".format(self.access_token.token)
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(['Hello', self.tag_1.id], [self.book_1.title, self.book_1.tags.all()[0].id])

    def test_delete(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('books-detail', args=(self.book_2.id,))
        self.auth = "Bearer {0}".format(self.access_token.token)
        response = self.client.delete(url, content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())


class AuthorsApiTestCase(APITestCase):
    def setUp(self):
        self.test_user = UserModel.objects.create_user("user", "test@example.com", "123456")
        self.author_1 = Author.objects.create(name='Author 1', year_of_birth=1903)
        self.author_2 = Author.objects.create(name='Author 2', year_of_birth=1926)
        self.author_3 = Author.objects.create(name='Author 3', year_of_birth=2000)
        self.author_3.books.create(title='Book 1', pages=226)
        self.book_2 = Book.objects.create(title='Book 2', pages=209)
        self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.test_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.application.save()
        self.access_token = AccessToken.objects.create(
            user=self.test_user,
            scope="read write",
            expires=timezone.now() + timezone.timedelta(seconds=300),
            token="secret-access-token-key",
            application=self.application
        )
        self.auth = "Bearer {0}".format(self.access_token.token)

    def test_get(self):
        url = reverse('authors-list')

        self.auth = "Bearer {0}".format(self.access_token.token)
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        serialazer_data = AuthorsSerializer([self.author_1, self.author_2, self.author_3], many=True).data
        pagination = OrderedDict([('count', 3), ('next', None), ('previous', None), ('results', serialazer_data)])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(pagination, response.data)

    def test_get_search401(self):
        url = reverse('authors-list')
        response = self.client.get(url, data={'search': 1926})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_search200(self):
        url = reverse('authors-list')
        response = self.client.get(url, data={'search': 1926}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        serialazer_data = AuthorsSerializer([self.author_2], many=True).data
        pagination = OrderedDict([('count', 1), ('next', None), ('previous', None), ('results', serialazer_data)])
        self.assertEqual(pagination, response.data)


    def test_create(self):
        url = reverse('authors-list')
        data = {
            'name': 'Ivan',
            'year_of_birth': 1253,
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create2(self):
        url = reverse('authors-list')
        data = {
            'name': 'Ivan',
            'year_of_birth': 1253,
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_update(self):
        url = reverse('authors-detail', args=(self.author_1.id,))
        data = {
            'name': 'Vitaly',
            'books': [self.book_2.id],
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.author_1.refresh_from_db()
        self.assertEqual(['Vitaly', self.book_2.id], [self.author_1.name, self.author_1.books.all()[0].id])

    def test_delete(self):
        self.assertEqual(3, Author.objects.all().count())
        url = reverse('authors-detail', args=(self.author_1.id,))
        response = self.client.delete(url, content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())


class TagsApiTestCase(APITestCase):
    def setUp(self):
        self.test_user = UserModel.objects.create_user("user", "test@example.com", "123456")
        self.tag_1 = Tag.objects.create(title='tag 1', description='ke1')
        self.tag_2 = Tag.objects.create(title='tag 2', description='ko2')
        self.tag_3 = Tag.objects.create(title='tag 3', description='ka3')
        self.book_1 = Book.objects.create(title='Book 1', pages=209)
        self.book_2 = Book.objects.create(title='Book 2', pages=169)
        self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.test_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.application.save()
        self.access_token = AccessToken.objects.create(
            user=self.test_user,
            scope="read write",
            expires=timezone.now() + timezone.timedelta(seconds=300),
            token="secret-access-token-key",
            application=self.application
        )
        self.auth = "Bearer {0}".format(self.access_token.token)

    def test_get(self):
        url = reverse('tags-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        serialazer_data = TagsSerializer([self.tag_1, self.tag_2, self.tag_3], many=True).data
        pagination = OrderedDict([('count', 3), ('next', None), ('previous', None), ('results', serialazer_data)])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(pagination, response.data)

    def test_create(self):
        url = reverse('tags-list')
        data = {
            'title': 'tag 4',
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create2(self):
        url = reverse('tags-list')
        data = {
            'title': 'tag 4',
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_update(self):
        url = reverse('tags-detail', args=(self.tag_1.id,))
        data = {
            'title': 'taaaaaag',
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.tag_1.refresh_from_db()
        self.assertEqual('taaaaaag', self.tag_1.title)

    def test_delete(self):
        self.assertEqual(3, Tag.objects.all().count())
        url = reverse('tags-detail', args=(self.tag_1.id,))
        response = self.client.delete(url, content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())
