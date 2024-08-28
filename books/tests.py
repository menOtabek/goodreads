from django.test import TestCase
from django.urls import reverse
from .models import Book
class BookTestCase(TestCase):
    def test_book_exists(self):
        book = Book.objects.create(title='some_title', description='some_description', isbn='some949834')
        response = self.client.get(reverse('books:books_list'))
        self.assertContains(response, book.title)


    def test_books_not_found(self):
        response = self.client.get(reverse('books:books_list'))
        self.assertContains(response, 'Books not found')


    def test_book_detail(self):
        book = Book.objects.create(title='some_title1', description='some_description1', isbn='some9498341')
        response = self.client.get(reverse('books:book_detail', kwargs={'pk': book.id}))
        self.assertContains(response, book.title)
        self.assertContains(response, book.description)