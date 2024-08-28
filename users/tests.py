from django.contrib.auth import login
from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserCreateTestCase(TestCase):
    def test_user_create(self):
        self.client.post(reverse('users:register'),
                         data={
                             'username': 'some_user',
                             'first_name': 'some_first_name',
                             'last_name': 'some_last_name',
                             'email': 'some@gmail.com',
                             'password': 'some_password'
                         })

        user = User.objects.filter(username='some_user').first()

        self.assertEqual(user.first_name, 'some_first_name')
        self.assertEqual(user.last_name, 'some_last_name')
        self.assertEqual(user.email, 'some@gmail.com')
        self.assertNotEqual(user.password, 'some_password')
        self.assertTrue(user.check_password('some_password'))

    def test_required_field(self):
        response = self.client.post(reverse('users:register'),
                                    data={'first_name': 'some_first_name',
                                          'email': 'some@gmail.com'})
        user_count = User.objects.count()
        self.assertEqual(user_count, 0)
        # ToDo fix error below
        # self.assertFormError(response, 'form', 'username', 'This field is required.')
        # self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_valid_email(self):
        response = self.client.post(reverse('users:register'),
                                    data={
                                        'username': 'some_user',
                                        'first_name': 'some_first_name',
                                        'last_name': 'some_last_name',
                                        'email': 'some_gmail_com',
                                        'password': 'some_password'
                                    })
        user_count = User.objects.count()
        self.assertEqual(user_count, 0)
        # ToDo fix error below
        # self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_recreate_user_with_exist_username(self):
        self.client.post(reverse('users:register'),
                         data={
                             'username': 'first_username',
                             'password': 'first_password'
                         })
        response = self.client.post(reverse('users:register'),
                                    data={
                                        'username': 'first_username',
                                        'password': 'first_password'
                                    })
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
        # ToDo fix error below
        # self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')


class LoginTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='some_username', first_name='some_name')
        user.set_password('some_password')
        user.save()


    def test_user_login(self):
        self.client.post(reverse('users:login'),
                         data={
                             'username': 'some_username',
                             'password': 'some_password'
                         })
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_logout(self):
        self.client.post(reverse('users:login'),
                         data={
                             'username': 'some_username',
                             'password': 'some_password'
                         })
        self.client.get(reverse('users:logout'))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


    def test_username_or_password_is_incorrect(self):
        self.client.post(reverse('users:login'),
                         data={
                             'username': 'incorrect_username',
                             'password': 'some_password'
                         })
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(reverse('users:login'),
                         data={
                             'username': 'some_username',
                             'password': 'incorrect_password'
                         })
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):

    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login'))

    def test_profile_exists(self):
        user = User.objects.create(username='username1', first_name='first_name1', last_name='last_name1',
                                   email='email1@.com')
        user.set_password('password1')
        user.save()
        self.client.login(username='username1', password='password1')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)
