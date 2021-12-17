from django.db   import models

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
    rating   = models.DecimalField(max_digits=5, decimal_places=3)
    runtime  = models.PositiveIntegerField()
    genre    = models.ForeignKey(Genre, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    summary  = models.CharField(max_length=300)
    
    class Meta :
        db_table = 'movies'