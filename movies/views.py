import json

from django.views    import View
from django.http     import JsonResponse
from django.db       import transaction
from django.db.utils import IntegrityError

from movies.filterlists import MovieFilter
from movies.models      import (
    Movie,
    MovieGenre,
    Review
)
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
                'rating'  : round(sum([val.rating for val in movie.review_set.all()]) / len(movie.review_set.all()) if movie.review_set.all() else 0, 2),
                'summary' : movie.summary,
                'genres'  : [{
                    'id'    : genre.id,
                    'genre' : genre.genre
                }for genre in movie.genre.all()]
            }
        for movie in movies]
        
        return JsonResponse({'movie_list' : movie_list}, status=200)

    def post(self, request) :
        try :
            with transaction.atomic() :
                data = json.loads(request.body)
                
                title   = data['title']
                year    = int(data['year'])
                genres  = data['genres']
                summary = data['summary']
                
                movie = Movie.objects.create(
                    title   = title,
                    year    = year,
                    summary = summary
                )
                
                for genre_id in genres :
                    MovieGenre.objects.create(movie=movie, genre_id=genre_id)
                
                return JsonResponse({'message' : 'CREATED_SUCCESS'}, status=201)

        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except IntegrityError :
            return JsonResponse({'message' : 'INTEGRITY_ERROR'}, status=400)

        except TypeError : 
            return JsonResponse({'message' : 'TYPE_ERROR'}, status=400)
        
class DetailMovieView(View) :
    def get(self, request, movie_id) :
        try :
            movie = Movie.objects.prefetch_related('review_set', 'genre').get(id=movie_id)
            
            detail_movie = {
                'id'     : movie.id,
                'title'  : movie.title,
                'year'   : movie.year,
                'rating' : round(sum([val.rating for val in movie.review_set.all()]) / len(movie.review_set.all()) if movie.review_set.all() else 0, 2),
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
    
    def post(self, request, movie_id) :
        try :
            with transaction.atomic() :
                data = json.loads(request.body)
                
                text   = data['text']
                rating = data['rating']
            
                Review.objects.create(
                    movie_id = movie_id,
                    text     = text,
                    rating   = rating
                )
                
                return JsonResponse({'message' : 'CREATED_SUCCESS'}, status=201)
        
        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except IntegrityError :
            return JsonResponse({'message' : 'INTEGRITY_ERROR'}, status=400)

class DetailReviewView(View) :
    def get(self, request, movie_id, review_id) :
        try :
            review = Review.objects.prefetch_related('movie').get(movie__id=movie_id, id=review_id)
            
            detail_review = {
                'id'         : review.id,
                'title'      : review.text,
                'rating'     : round(review.rating, 2),
                'created_at' : review.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return JsonResponse({'detail_review' : detail_review}, status=200)
        
        except Review.DoesNotExist :
            return JsonResponse({'message' : 'REVIEW_DOES_NOT_EXIST'}, status=400)