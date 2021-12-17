from django.urls import path

from movies.views import (
    MovieView,
    DetailMovieView,
    DetailReviewView
)
urlpatterns = [
    path('', MovieView.as_view()),
    path('/<int:movie_id>', DetailMovieView.as_view()),
    path('/<int:movie_id>/<int:review_id>', DetailReviewView.as_view())
]