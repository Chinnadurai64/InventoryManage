from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from .models import Item

class ItemTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.item = Item.objects.create(name='TestItem', description='Test description', quantity=10)

    def test_create_item(self):
        response = self.client.post('/inventory/items/', {'name': 'NewItem', 'description': 'New description', 'quantity': 5})
        self.assertEqual(response.status_code, 201)

    def test_read_item(self):
        response = self.client.get(f'/inventory/items/{self.item.id}/')
        self.assertEqual(response.status_code, 200)

    def test_update_item(self):
        response = self.client.put(f'/inventory/items/{self.item.id}/', {'name': 'UpdatedItem', 'description': 'Updated description', 'quantity': 15})
        self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        response = self.client.delete(f'/inventory/items/{self.item.id}/')
        self.assertEqual(response.status_code, 204)
