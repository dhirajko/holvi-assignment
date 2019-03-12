from django.test import TestCase

# Create your tests here.
from django.urls import reverse, resolve


class testDetail:

    def test_an_admin_view(admin_client):
        response = admin_client.get('/admin/')
        assert response.status_code == 200
