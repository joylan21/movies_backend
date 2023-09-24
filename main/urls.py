from django.urls import path
from .views import MoviesViewSet

urlpatterns = [
    path('movies/', MoviesViewSet.as_view({'get':'list', 'post':'create'}), name='movie-list-create'),
    path('movies/<int:pk>/', MoviesViewSet.as_view({'get':'retrieve', 'put':'update'}), name='movie-detail'),
]
