from django.db.models import ImageField

from users.models import CustomUser
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    isbn = models.CharField(max_length=17)
    book_picture = ImageField(default='Screenshot_from_2024-08-30_14-44-16.png')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=123)
    last_name = models.CharField(max_length=123)
    email = models.EmailField()
    bio = models.CharField(max_length=123)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.book.title} by {self.author.first_name}'


class BookReview(models.Model):
    comment = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stars_given = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment to {self.book.title} by {self.user.username}'
