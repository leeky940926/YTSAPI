from django.db.models import (
    Q,
    Avg
)
from movies.models    import Movie

class MovieFilter :
    def __init__(self, page, year, rating, title, genre) :
        self.page   = page
        self.year   = year
        self.rating = rating
        self.title  = title
        self.genre  = genre
    
    def filter_movies(page, year, rating, title, genre) :
        
        movie_filter = Q()
        
        limit  = 10
        offset = limit * (int(page)-1)
        
        if year :
            movie_filter.add(Q(year = year), Q.AND)
        
        if title :
            movie_filter.add(Q(title__icontains = title), Q.AND)
        
        if genre :
            movie_filter.add(Q(moviegenre__genre_id = genre), Q.AND)
     
        if rating == 'h' :
            movies = Movie.objects.prefetch_related('review_set', 'genre').filter(movie_filter).annotate(review_rating=Avg('review__rating')).order_by('-review_rating', '-created_at')[offset:offset+limit]
            return movies
        
        movies = Movie.objects.prefetch_related('review_set', 'genre').filter(movie_filter).order_by('-created_at')[offset:offset+limit]
            
        return movies 