from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# Test client used to make requests to API and check response
from rest_framework.test import APIClient
# Get human-readable test codes
from rest_framework import status

# Create a 'create user' url and assign it to this variable
#  -> This will cause an error until we wire up the URLs to the user view
CREATE_USER_URL = reverse('user:create')
# This is going to be the URL used to make the HTTP POST request used to
#  generate our token
TOKEN_URL = reverse('user:token')
# The url for the specific user where they have access to their profile
#  information
ME_URL = reverse('user:me')


# dynamic list of arguments to pass directly into the create user model
def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """ Test the users API (public) """

    def setUp(self):
        # Not adding authentication for this setup
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ Test creating user with valid payload is successful """
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'Test name'
        }
        # This will make an HTTP POST request to our client to our url for
        #  for creating users and make sure the outcome is what we expect.
        #  We expect an HTTP 201 response
        res = self.client.post(CREATE_USER_URL, payload)
        # Assert correct status code
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Take the res.data and pass it in as the params for the GET
        user = get_user_model().objects.get(**res.data)
        # Assert that the password is true
        self.assertTrue(user.check_password(payload['password']))
        # Assure that the password itself is not in the response (security)
        self.assertNotIn('password', res.data)

    # Next we will test what happens when a user is attempted to be created
    #  when one already exists
    def test_user_exists(self):
        """ Test creating a user that already exists fails """
        payload = {
                'email': 'test@londonappdev.com',
                'password': 'testpass',
                'name': 'Test'
        }
        create_user(**payload)

        # Make the request
        res = self.client.post(CREATE_USER_URL, payload)
        # Ensure correct status code
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Test if password is too short
    def test_password_too_short(self):

        """ Test that the password must be more than 5 characters """

        payload = {
                'email': 'test@londonappdev.com',
                'password': 'pw',
                'name': 'Test',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # filter for any user with this email address
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        # database is refreshed every time a test is ran, so prevously-made
        #  users will not be present in this test
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ Test that a token is created for the user """
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        # check that there is a key called token in the response data
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ Test that token is not created if invalid credentials are given """
        create_user(email='test@londonappdev.com', password="testpass")
        # This request shoul respond with http 400 bad request
        payload = {'email': 'test@londonappdev.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """ Test htat token is not created if user does not exist """
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ Test that email and password are required """
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """ Test that authentication is required for users """
        res = self.client.get(ME_URL)
        # Test to ensure that we receive an error when we attempt to connect
        #  to the ME page without authorization
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """ Test API requests that require authentication """

    def setUp(self):
        self.user = create_user(
            email='test@londonappdev.com',
            password='testpass',
            name='name'
        )
        self.client = APIClient()
        # Helper function used to simulate making authenticated requests
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """ Test retrieving profile for logged in user """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """ Test that POST is not allowed on the me url """
        # send empty object here just for test
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ Test updating the user profile for authenticated user """
        payload = {'name': 'new name', 'password': 'newpassword123'}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
