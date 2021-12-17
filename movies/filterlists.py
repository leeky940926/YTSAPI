from django.db.models import Q

from movies.models    import Movie

class MovieFilter :
    def __init__(self, page, year, rating, title) :
        self.page   = page
        self.year   = year
        self.rating = rating
        self.title  = title
    
    def filter_movies(page, year, rating, title) :
        
        movie_filter = Q()
        
        limit  = 10
        offset = limit * (int(page)-1)
        
        if year :
            movie_filter.add(Q(year = year), Q.AND)
        
        if title :
            movie_filter.add(Q(title__icontains = title), Q.AND)
     
        if rating == 'h' :
            movies = Movie.objects.prefetch_related('genre').filter(movie_filter).order_by('-rating', '-created_at')[offset:offset+limit]
            return movies
        
        movies = Movie.objects.prefetch_related('genre').filter(movie_filter).order_by('-created_at')[offset:offset+limit]
            
        return movies