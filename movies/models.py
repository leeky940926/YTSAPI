from django.db   import models
from django.db.models.deletion import CASCADE

from core.models import TimeStampModel

class Genre(TimeStampModel) :
    genre = models.CharField(max_length=20)
    
    class Meta : 
        db_table = 'genres'

class Language(TimeStampModel) :
    language = models.CharField(max_length=20)
    
    class Meta :
        db_table = 'languages'

class Movie(TimeStampModel) :
    title    = models.CharField(max_length=300)
    year     = models.PositiveIntegerField()
    runtime  = models.PositiveIntegerField(null=True)
    genre    = models.ManyToManyField(Genre, through='MovieGenre')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    summary  = models.CharField(max_length=300)
    
    class Meta :
        db_table = 'movies'

class MovieGenre(TimeStampModel) :
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    
    class Meta :
        db_table = 'movies_genres'

class Review(TimeStampModel) :
    movie  = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text   = models.TextField()
    rating = models.DecimalField(max_digits=5, decimal_places=3)
    vote   = models.IntegerField(default=0)
    
    class Meta :
        db_table = 'reviews'

class ReivewVote(TimeStampModel) :
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    
    class Meta :
        db_table = 'review_votes'