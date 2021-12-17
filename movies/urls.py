from django.urls import path

from movies.views import (
    MovieView,
    DetailMovieView,
    DetailReviewView,
    ReviewVoteView
)
urlpatterns = [
    path('', MovieView.as_view()),
    path('/<int:movie_id>', DetailMovieView.as_view()),
    path('/<int:movie_id>/reviews/<int:review_id>', DetailReviewView.as_view()),
    path('/<int:movie_id>/reviews/<int:review_id>/votes/<int:review_vote_id>', ReviewVoteView.as_view())
]