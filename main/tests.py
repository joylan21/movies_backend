from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Movie
from rest_framework_simplejwt.tokens import RefreshToken 
from django.contrib.auth.models import User

class MoviesViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)

        self.movie_data = {
            'title': 'Test Movie',
            'genre': 'Test Genre',
            'release_date': '2023-09-23',
            'director': 'Test Director',
        }
        self.movie = Movie.objects.create(**self.movie_data)
        self.client.force_authenticate(user=self.user)

    def get_headers(self):
        return {
            'HTTP_AUTHORIZATION': f'Bearer {self.access_token}',
        }

    def test_list_movies(self):
        url = reverse('movie-list-create')
        response = self.client.get(url, headers = self.get_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_movie(self):
        url = reverse('movie-detail', args=[self.movie.id])
        response = self.client.get(url, headers = self.get_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_movie(self):
        url = reverse('movie-list-create')
        response = self.client.post(url, self.movie_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_movie(self):
        url = reverse('movie-detail', args=[self.movie.id])
        updated_data = {
            'title': 'Updated Movie Title',
            'genre': 'Updated Genre',
            'release_date': '2023-09-24',
            'director': 'Updated Director',
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_movies_by_genre(self):
        url = reverse('movie-list-create') + '?genre=Test Genre'
        response = self.client.get(url, headers = self.get_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_movies_by_director(self):
        url = reverse('movie-list-create') + '?director=Test Director'
        response = self.client.get(url, headers = self.get_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_title_max_length_validation(self):
        data = {
            'title': 'A' * 256,  
            'genre': 'Test Genre',
            'release_date': '2023-09-23',
            'director': 'Test Director',
        }
        url = reverse('movie-list-create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_genre_max_length_validation(self):
        data = {
            'title': 'Test Movie',
            'genre': 'A' * 101,
            'release_date': '2023-09-23',
            'director': 'Test Director',
        }
        url = reverse('movie-list-create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_release_date_format_validation(self):
        data = {
            'title': 'Test Movie',
            'genre': 'Test Genre',
            'release_date': '2023/09/23',
            'director': 'Test Director',
        }
        url = reverse('movie-list-create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_director_max_length_validation(self):
        data = {
            'title': 'Test Movie',
            'genre': 'Test Genre',
            'release_date': '2023-09-23',
            'director': 'A' * 101,
        }
        url = reverse('movie-list-create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)