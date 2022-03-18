from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@londonappdev.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@londonappdev.com',
            password='password123',
            name='Test user full name'
        )

    def test_users_listed(self):
        """ Test that users are listed on user page """
        url = reverse('admin:core_user_changelist')
        # use test client to perform http get on the url that we have found
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """ Test that the user edit page works """
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/:id
        res = self.client.get(url)

        # Test that this page renders okay
        # Fails until we customize user admin field sets
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """ Test that the create user page works """
        # This is the standard url alias for the add page for our user model
        url = reverse('admin:core_user_add')
        # Our test client is going to make an http get to this url
        res = self.client.get(url)
        # Fails with an error until a username is specified for the user
        self.assertEqual(res.status_code, 200)
