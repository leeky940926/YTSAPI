from django.views import View
from django.http  import JsonResponse

from movies.filterlists import MovieFilter

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