from django.db import models


# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100)
    year_of_birth = models.IntegerField(blank=True)

    def __str__(self):
        return f'{self.id} {self.name}'

    class Meta:
        ordering = ('name',)

    @property
    def books(self):
        return self.book_set.all()


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
        return f'{self.id} {self.title} {self.authors.name}, {self.tags}'

    def display_tags(self):
        """
        Creates a string for the Tags. This is required to display genre in Admin.
        """
        return ', '.join([tag.title for tag in self.tags.all()[:3]])

    display_tags.short_description = 'Tags'

    def display_authors(self):
        """
        Creates a string for the Tags. This is required to display genre in Admin.
        """
        return ', '.join([author.name for author in self.authors.all()[:3]])

    display_authors.short_description = 'Authors'

    class Meta:
        ordering = ('title',)
