from http.client import responses

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
        response = self.client.get(reverse('books:books_list') + '?page_size=2')
        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)
        response = self.client.get(reverse('books:books_list') + '?page=2&?page_size=2')
        self.assertContains(response, book3.title)


    def test_book_search(self):
        book1 = Book.objects.create(title='Health', description='some_description1', isbn='some9498341')
        book2 = Book.objects.create(title='Cambridge', description='some_description2', isbn='some94982341')
        book3 = Book.objects.create(title='Atomic habits', description='some_description3', isbn='some94983341')

        response = self.client.get(reverse('books:books_list') + '?q=health')

        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:books_list') + '?q=cambridge')

        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:books_list') + '?q=atomic')

        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)
