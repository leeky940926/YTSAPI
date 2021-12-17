from django.urls import path

from movies.views import (
    MovieView,
    DetailMovieView
)
urlpatterns = [
    path('', MovieView.as_view()),
    path('/<int:movie_id>', DetailMovieView.as_view())
]