from django.db import models


# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100)
    year_of_birth = models.IntegerField(blank=True)

    def __str__(self):
        return f'{self.id} {self.name}'

    class Meta:
        ordering = ('name',)


class Tag(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.id} {self.title}'


class Book(models.Model):
    title = models.CharField(max_length=150)
    pages = models.IntegerField(blank=True)
    authors = models.ManyToManyField(Author)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'{self.id} {self.title} {self.authors.name}'

    class Meta:
        ordering = ('title',)
