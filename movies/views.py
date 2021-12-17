from django import views
from django.views import View
from django.http  import JsonResponse

from movies.filterlists import MovieFilter
from movies.models import Movie

class MovieView(View) :
    def get(self, request) :  
        page   = request.GET.get('page', 1)
        year   = request.GET.get('year')
        rating = request.GET.get('rating')
        title  = request.GET.get('title')
        
        movies = MovieFilter.filter_movies(page, year, rating, title)

        movie_list = [
            {
                'id'      : movie.id,
                'title'   : movie.title,
                'rating'  : round(movie.rating, 2),
                'summary' : movie.summary,
                'genres'  : [{
                    'id'    : genre.id,
                    'genre' : genre.genre
                }for genre in movie.genre.all()]
            }
        for movie in movies]
        
        return JsonResponse({'movie_list' : movie_list}, status=200)

class DetailMovieView(View) :
    def get(self, request, movie_id) :
        try :
            movie = Movie.objects.prefetch_related('review_set', 'genre').get(id=movie_id)
            
            detail_movie = {
                'id'     : movie.id,
                'title'  : movie.title,
                'year'   : movie.year,
                'rating' : round(movie.rating, 2),
                'genres' : [{
                    'id'    : genre.id,
                    'genre' : genre.genre
                }for genre in movie.genre.all()],
                'summary' : movie.summary,
                'reviews' : [{
                    'review_id'     : review.id,
                    'review_text'   : review.text,
                    'review_rating' : round(review.rating),
                    'review_vote'   : review.vote
                }for review in movie.review_set.all()]
            }
            
            return JsonResponse({'detail_movie' : detail_movie}, status=200)

        except Movie.DoesNotExist :
            return JsonResponse({'message' : 'MOVIE_DOES_NOT_EXIST'}, status=400)