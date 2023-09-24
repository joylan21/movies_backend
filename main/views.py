from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

class MoviesViewSet(viewsets.ModelViewSet):
    permission_classes = [ IsAuthenticated ]
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

    pagination_class = CustomPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['genre', 'director']