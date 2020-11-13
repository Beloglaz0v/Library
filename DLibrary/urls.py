"""DLibrary URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

from library.views import BookViewSet, AuthorViewSet, TagViewSet, SearchBooks


router = routers.DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'books', BookViewSet, basename='books')
router.register(r'search_books', SearchBooks, basename='search_books')

tag_router = routers.NestedDefaultRouter(router, r'tags', lookup='tag')
tag_router.register(r'books', BookViewSet, basename='books')

author_router = routers.NestedDefaultRouter(router, r'authors', lookup='author')
author_router.register(r'books', BookViewSet, basename='books')

book_router = routers.NestedDefaultRouter(router, r'books', lookup='book')
book_router.register(r'authors', AuthorViewSet, basename='author')
book_router.register(r'tags', TagViewSet, basename='tag')


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^', include(tag_router.urls)),
    url(r'^', include(book_router.urls)),
    url(r'^', include(author_router.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
