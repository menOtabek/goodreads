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
        book1 = Book.objects.create(title='some_title1', description='some_description1', isbn='some9498341')
        book2 = Book.objects.create(title='some_title2', description='some_description2', isbn='some94982341')
        book3 = Book.objects.create(title='some_title3', description='some_description3', isbn='some94983341')
        response = self.client.get(reverse('books:books_list'))
        for book in [book1, book2]:
            self.assertContains(response, book.title)
        response = self.client.get(reverse('books:books_list') + '?page=2')
        self.assertContains(response, book3.title)