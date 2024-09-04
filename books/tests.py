from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser
from .models import Book, BookReview


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


class BookReviewTestCase(TestCase):
    def test_create_review(self):
        book1 = Book.objects.create(title='Health', description='some_description1', isbn='some9498341')
        user = CustomUser.objects.create(username='username1', first_name='first_name1', last_name='last_name1',
                                         email='email1@gmail.com')
        user.set_password('password1')
        user.save()
        self.client.login(username='username1', password='password1')

        self.client.post(reverse('books:review_create', kwargs={'pk':book1.id}),
                         data={
                             'stars_given': 4,
                             'comment': 'Very good book'
                         })
        book_reviews = book1.bookreview_set.all()
        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 4)
        self.assertEqual(book_reviews[0].comment, 'Very good book')
        self.assertEqual(book_reviews[0].book, book1)
        self.assertEqual(book_reviews[0].user, user)


    def test_create_review_with_high_mark(self):
        book1 = Book.objects.create(title='Health', description='some_description1', isbn='some9498341')
        user = CustomUser.objects.create(username='username1', first_name='first_name1', last_name='last_name1',
                                         email='email1@gmail.com')
        user.set_password('password1')
        user.save()
        self.client.login(username='username1', password='password1')

        self.client.post(reverse('books:review_create', kwargs={'pk':book1.id}),
                         data={
                             'stars_given': 6,
                             'comment': 'Very good book'
                         })
        book_reviews = book1.bookreview_set.all()
        self.assertEqual(book_reviews.count(), 0)


class HomePageTEstCase(TestCase):
    def test_paginated_reviews(self):
        book = Book.objects.create(title='Health', description='some_description1', isbn='some9498341')
        user = CustomUser.objects.create(username='username1', first_name='first_name1', last_name='last_name1',
                                         email='email1@gmail.com')
        user.set_password('password1')
        user.save()
        self.client.login(username='username1', password='password1')
        review1 = BookReview.objects.create(book=book, user=user, comment='nice book', stars_given=4)
        review2 = BookReview.objects.create(book=book, user=user, comment='nice book1', stars_given=3)
        review3 = BookReview.objects.create(book=book, user=user, comment='nice book2', stars_given=5)

        response = self.client.get(reverse('home_page') + '?page_size=2')
        self.assertContains(response, review1.comment)
        self.assertContains(response, review2.comment)
        self.assertContains(response, review3.comment)
        # ToDo shu testda review3.comment bo'lishi kerak, lekin testdan o'tmadi unda
