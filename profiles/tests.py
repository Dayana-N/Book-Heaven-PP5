import uuid

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from profiles.models import UserProfile


# Create your tests here.
class ProfilePageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        ''' Create test Profile'''
        cls.user = User.objects.create(
            username='TestUser',
            password='1234pass',
            email='test@user.com',
            id='1',
        )
        cls.user_profile = UserProfile.objects.update(
            default_phone_number='0894123456',
            default_country='Ireland',
            id='bae50a5c-ec55-48c7-a822-9ebbbe4f918a'
        )

    def test_if_user_profile_created(self):
        '''
        Test if user profile is created
        '''
        user_profile = UserProfile.objects.filter().last()
        self.assertEqual(user_profile.user.username, 'TestUser')
        self.assertEqual(user_profile.default_phone_number, '0894123456')
        expected_id = uuid.UUID('bae50a5c-ec55-48c7-a822-9ebbbe4f918a')
        self.assertEqual(
            user_profile.id, expected_id)

    def test_profile_page(self):
        '''
        Test if the profile page can be accessed
        and it returns the correct template
        '''

        user = User.objects.get(username='TestUser')
        self.client.force_login(user)
        response = self.client.get(
            reverse('profile', kwargs={'pk': user.userprofile.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertContains(
            response, '<p class="text-start fs-3 fw-4">My Details:</p>')
