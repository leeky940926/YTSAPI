from django.test import (
    TestCase,
    Client
)

from movies.models import (
    Language,
    Movie,
    Genre,
    MovieGenre
)

class TestMovieView(TestCase) :
    
    TestCase.maxDiff = None
    
    def setUp(self) :
        language_list = [
            Language(id=1, language='kr'),
            Language(id=2, language='en'),
            Language(id=3, language='ja')
        ]
        Language.objects.bulk_create(language_list)
        
        genre_list = [
            Genre(id=1, genre='drama test'),
            Genre(id=2, genre='action test'),
            Genre(id=3, genre='sriller test'),
            Genre(id=4, genre='adventure test'),
            Genre(id=5, genre='sad test'),
        ]
        Genre.objects.bulk_create(genre_list)
        
        movie_list = [
            Movie(id=1, language_id=1, year=2021, runtime=90, summary='good movie1', title='new movie1', rating=3.2),
            Movie(id=2, language_id=2, year=2020, runtime=90, summary='good movie2', title='bad movie1', rating=9.5),
            Movie(id=3, language_id=1, year=2021, runtime=90, summary='good movie3', title='sad movie1', rating=5.2),
            Movie(id=4, language_id=3, year=2021, runtime=80, summary='good movie4', title='fun movie1', rating=7.2),
            Movie(id=5, language_id=2, year=2021, runtime=80, summary='good movie5', title='new movie2', rating=8.2),
            Movie(id=6, language_id=3, year=2020, runtime=80, summary='good movie6', title='new movie3', rating=10),
            Movie(id=7, language_id=1, year=2021, runtime=100, summary='good movie7', title='good movie1', rating=8.5),
            Movie(id=8, language_id=1, year=2021, runtime=90, summary='good movie8', title='bad movie2', rating=7.5),
            Movie(id=9, language_id=1, year=2020, runtime=100, summary='good movie9', title='bad movie3', rating=7.5),
            Movie(id=10, language_id=3, year=2019, runtime=110, summary='good movie10', title='new movie4', rating=2.5),
            Movie(id=11, language_id=1, year=2019, runtime=90, summary='good movie11', title='sad movie2', rating=3.5),
            Movie(id=12, language_id=1, year=2019, runtime=90, summary='good movie12', title='fun movie2', rating=9.5),
            Movie(id=13, language_id=2, year=2021, runtime=130, summary='good movie13', title='old movie1', rating=5.5),
            Movie(id=14, language_id=1, year=2021, runtime=90, summary='good movie14', title='old movie2', rating=4.5),
            Movie(id=15, language_id=2, year=2017, runtime=140, summary='good movie15', title='old movie3', rating=6.5),
            Movie(id=16, language_id=2, year=2021, runtime=90, summary='good movie16', title='action movie1', rating=8.5),
            Movie(id=17, language_id=1, year=2021, runtime=150, summary='good movie17', title='action movie2', rating=6.7),
            Movie(id=18, language_id=1, year=2016, runtime=90, summary='good movie18', title='action movie3', rating=8.7),
            Movie(id=19, language_id=1, year=2021, runtime=90, summary='good movie19', title='action movie4', rating=7.7),
            Movie(id=20, language_id=1, year=2021, runtime=90, summary='good movie20', title='action movie5', rating=4.7)
        ]
        Movie.objects.bulk_create(movie_list)
        
        movie_genre_list = [
            MovieGenre(id=1, movie_id=1, genre_id=1),
            MovieGenre(id=2, movie_id=1, genre_id=2),
            MovieGenre(id=3, movie_id=2, genre_id=1),
            MovieGenre(id=4, movie_id=3, genre_id=4),
            MovieGenre(id=5, movie_id=4, genre_id=5),
            MovieGenre(id=6, movie_id=5, genre_id=3),
            MovieGenre(id=7, movie_id=5, genre_id=5),
            MovieGenre(id=8, movie_id=6, genre_id=2),
            MovieGenre(id=9, movie_id=7, genre_id=4),
            MovieGenre(id=10, movie_id=8, genre_id=1),
        ]
        MovieGenre.objects.bulk_create(movie_genre_list)
    
    def tearDown(self) :
        Language.objects.all().delete()
        Movie.objects.all().delete()
        Genre.objects.all().delete()
        MovieGenre.objects.all().delete()
    
    def test_success_get_movie_list(self) :
        client = Client()
        
        respone = client.get('/movies?page=1&year=2021&title=new')
        
        self.assertEqual(respone.status_code, 200)
        self.assertEqual(respone.json(),{
            'movie_list' : [
                {
                'id'     : 5,
                'title'  : 'new movie2',
                'rating' : '8.20',
                'summary' : 'good movie5',
                'genres' : [
                    {
                        'id'    : 3,
                        'genre' : 'sriller test'
                    },
                    {
                        'id'    : 5,
                        'genre' : 'sad test'
                    }
                ]
            },
                {
                'id'     : 1,
                'title'  : 'new movie1',
                'rating' : '3.20',
                'summary' : 'good movie1',
                'genres' : [
                    {
                        'id'    : 1,
                        'genre' : 'drama test'
                    },
                    {
                        'id'    : 2,
                        'genre' : 'action test'
                    }
                ]
            }
            ]
        })