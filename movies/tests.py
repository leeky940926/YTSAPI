import json
from django.db import transaction

from django.test import (
    TestCase,
    TransactionTestCase,
    Client
)

from movies.models import (
    Language,
    Movie,
    Genre,
    MovieGenre,
    Review
)

class TestMovieView(TransactionTestCase) :
    
    TransactionTestCase.maxDiff = None
    
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
            Movie(id=1, language_id=1, year=2021, runtime=90, summary='good movie1', title='new movie1'),
            Movie(id=2, language_id=2, year=2020, runtime=90, summary='good movie2', title='bad movie1'),
            Movie(id=3, language_id=1, year=2021, runtime=90, summary='good movie3', title='sad movie1'),
            Movie(id=4, language_id=3, year=2021, runtime=80, summary='good movie4', title='fun movie1'),
            Movie(id=5, language_id=2, year=2021, runtime=80, summary='good movie5', title='new movie2'),
            Movie(id=6, language_id=3, year=2020, runtime=80, summary='good movie6', title='new movie3'),
            Movie(id=7, language_id=1, year=2021, runtime=100, summary='good movie7', title='good movie1'),
            Movie(id=8, language_id=1, year=2021, runtime=90, summary='good movie8', title='bad movie2'),
            Movie(id=9, language_id=1, year=2020, runtime=100, summary='good movie9', title='bad movie3'),
            Movie(id=10, language_id=3, year=2019, runtime=110, summary='good movie10', title='new movie4'),
            Movie(id=11, language_id=1, year=2019, runtime=90, summary='good movie11', title='sad movie2'),
            Movie(id=12, language_id=1, year=2019, runtime=90, summary='good movie12', title='fun movie2'),
            Movie(id=13, language_id=2, year=2021, runtime=130, summary='good movie13', title='old movie1'),
            Movie(id=14, language_id=1, year=2021, runtime=90, summary='good movie14', title='old movie2'),
            Movie(id=15, language_id=2, year=2017, runtime=140, summary='good movie15', title='old movie3'),
            Movie(id=16, language_id=2, year=2021, runtime=90, summary='good movie16', title='action movie1'),
            Movie(id=17, language_id=1, year=2021, runtime=150, summary='good movie17', title='action movie2'),
            Movie(id=18, language_id=1, year=2016, runtime=90, summary='good movie18', title='action movie3'),
            Movie(id=19, language_id=1, year=2021, runtime=90, summary='good movie19', title='action movie4'),
            Movie(id=20, language_id=1, year=2021, runtime=90, summary='good movie20', title='action movie5')
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
        
        review_list = [
            Review(movie_id=1, text='재밌어요', rating=9, vote=1),
            Review(movie_id=5, text='별로에요', rating=5, vote=0)
        ]
        Review.objects.bulk_create(review_list)
    
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
                'rating' : '5.00',
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
                'rating' : '9.00',
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
    
    def test_success_post_movie(self) :
        client = Client()
        
        data = {
            'title' : 'test title',
            'year' : 20201,
            'genres' : [1,4],
            'summary' : 'test summary'
        }
        
        response = client.post('/movies', json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'CREATED_SUCCESS'})
    
    def test_failure_post_movie_raise_key_error(self) :
        client = Client()
        
        data = {
            
        }
        
        response = client.post('/movies', json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})
    
    def test_failure_post_movie_raise_type_error(self) :
        client = Client()
        
        data = {
            'title' : 'test title',
            'year' : 20201,
            'genres' : 1444,
            'summary' : 'test summary'
        }
        
        response = client.post('/movies', json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'TYPE_ERROR'})
    
    def test_failure_post_movie_raise_integrity_error(self) :
        client = Client()
        
        data = {
            'title' : 'test title',
            'year' : 20201,
            'genres' : [1,2,1111],
            'summary' : 'test summary'
        }
        
        response = client.post('/movies', json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INTEGRITY_ERROR'})
    
class DetailMovieView(TransactionTestCase) :
    
    TransactionTestCase.maxDiff = None
    
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
            Movie(id=1, language_id=1, year=2021, runtime=90, summary='good movie1', title='new movie1'),
            Movie(id=2, language_id=2, year=2020, runtime=90, summary='good movie2', title='bad movie1'),
            Movie(id=3, language_id=1, year=2021, runtime=90, summary='good movie3', title='sad movie1'),
            Movie(id=4, language_id=3, year=2021, runtime=80, summary='good movie4', title='fun movie1'),
            Movie(id=5, language_id=2, year=2021, runtime=80, summary='good movie5', title='new movie2'),
            Movie(id=6, language_id=3, year=2020, runtime=80, summary='good movie6', title='new movie3'),
            Movie(id=7, language_id=1, year=2021, runtime=100, summary='good movie7', title='good movie1'),
            Movie(id=8, language_id=1, year=2021, runtime=90, summary='good movie8', title='bad movie2'),
            Movie(id=9, language_id=1, year=2020, runtime=100, summary='good movie9', title='bad movie3'),
            Movie(id=10, language_id=3, year=2019, runtime=110, summary='good movie10', title='new movie4'),
            Movie(id=11, language_id=1, year=2019, runtime=90, summary='good movie11', title='sad movie2'),
            Movie(id=12, language_id=1, year=2019, runtime=90, summary='good movie12', title='fun movie2'),
            Movie(id=13, language_id=2, year=2021, runtime=130, summary='good movie13', title='old movie1'),
            Movie(id=14, language_id=1, year=2021, runtime=90, summary='good movie14', title='old movie2'),
            Movie(id=15, language_id=2, year=2017, runtime=140, summary='good movie15', title='old movie3'),
            Movie(id=16, language_id=2, year=2021, runtime=90, summary='good movie16', title='action movie1'),
            Movie(id=17, language_id=1, year=2021, runtime=150, summary='good movie17', title='action movie2'),
            Movie(id=18, language_id=1, year=2016, runtime=90, summary='good movie18', title='action movie3'),
            Movie(id=19, language_id=1, year=2021, runtime=90, summary='good movie19', title='action movie4'),
            Movie(id=20, language_id=1, year=2021, runtime=90, summary='good movie20', title='action movie5')
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
        
        review_list = [
            Review(id=1, movie_id=1, text='재밌어요', rating=9, vote=1),
            Review(id=2, movie_id=1, text='별로에요', rating=5, vote=0)
        ]
        Review.objects.bulk_create(review_list)
    
    def tearDown(self) :
        Language.objects.all().delete()
        Movie.objects.all().delete()
        Genre.objects.all().delete()
        MovieGenre.objects.all().delete()
        Review.objects.all().delete()
    
    def test_success_detail_movie(self) :
        client = Client()
        
        response = client.get('/movies/1')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            'detail_movie' : {
                'id' : 1,
                'title' : 'new movie1',
                'year' : 2021,
                'rating' : '7.00',
                'genres' : [{
                    'id'    : 1,
                    'genre' : 'drama test'
                },
                {
                    'id'    : 2,
                    'genre' : 'action test'
                }],
                'summary' : 'good movie1',
                'reviews' : [{
                    'review_id'     : 1,
                    'review_text'   : '재밌어요',
                    'review_rating' : 9,
                    'review_vote'   : 1
                },
                {
                    'review_id'     : 2,
                    'review_text'   : '별로에요',
                    'review_rating' : 5,
                    'review_vote'   : 0
                }]
            }
        })
    
    def test_failure_detail_movie_raise_movie_does_not_exist(self) :
        client = Client()
        
        response = client.get('/movies/11111')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'message' : 'MOVIE_DOES_NOT_EXIST'
        })
    
    def test_success_post_review(self) :
        client = Client()
        
        data = {
            'text'   : 'new review',
            'rating' : 9.21
        }
        
        response = client.post('/movies/1', json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'CREATED_SUCCESS'})
    
    def test_failure_post_review_raise_key_error(self) :
        client = Client()
        
        data = {
            'text'   : 'new review'
        }
        
        response = client.post('/movies/1', json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})

class TestDetailReviewView(TransactionTestCase) :

    TransactionTestCase.maxDiff = None
    
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
            Movie(id=1, language_id=1, year=2021, runtime=90, summary='good movie1', title='new movie1'),
            Movie(id=2, language_id=2, year=2020, runtime=90, summary='good movie2', title='bad movie1'),
            Movie(id=3, language_id=1, year=2021, runtime=90, summary='good movie3', title='sad movie1'),
            Movie(id=4, language_id=3, year=2021, runtime=80, summary='good movie4', title='fun movie1'),
            Movie(id=5, language_id=2, year=2021, runtime=80, summary='good movie5', title='new movie2'),
            Movie(id=6, language_id=3, year=2020, runtime=80, summary='good movie6', title='new movie3'),
            Movie(id=7, language_id=1, year=2021, runtime=100, summary='good movie7', title='good movie1'),
            Movie(id=8, language_id=1, year=2021, runtime=90, summary='good movie8', title='bad movie2'),
            Movie(id=9, language_id=1, year=2020, runtime=100, summary='good movie9', title='bad movie3'),
            Movie(id=10, language_id=3, year=2019, runtime=110, summary='good movie10', title='new movie4'),
            Movie(id=11, language_id=1, year=2019, runtime=90, summary='good movie11', title='sad movie2'),
            Movie(id=12, language_id=1, year=2019, runtime=90, summary='good movie12', title='fun movie2'),
            Movie(id=13, language_id=2, year=2021, runtime=130, summary='good movie13', title='old movie1'),
            Movie(id=14, language_id=1, year=2021, runtime=90, summary='good movie14', title='old movie2'),
            Movie(id=15, language_id=2, year=2017, runtime=140, summary='good movie15', title='old movie3'),
            Movie(id=16, language_id=2, year=2021, runtime=90, summary='good movie16', title='action movie1'),
            Movie(id=17, language_id=1, year=2021, runtime=150, summary='good movie17', title='action movie2'),
            Movie(id=18, language_id=1, year=2016, runtime=90, summary='good movie18', title='action movie3'),
            Movie(id=19, language_id=1, year=2021, runtime=90, summary='good movie19', title='action movie4'),
            Movie(id=20, language_id=1, year=2021, runtime=90, summary='good movie20', title='action movie5')
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
        
        review_list = [
            Review(id=1, movie_id=1, text='재밌어요', rating=9, vote=1),
            Review(id=2, movie_id=1, text='별로에요', rating=5, vote=0)
        ]
        Review.objects.bulk_create(review_list)
    
    def tearDown(self) :
        Language.objects.all().delete()
        Movie.objects.all().delete()
        Genre.objects.all().delete()
        MovieGenre.objects.all().delete()
        Review.objects.all().delete()
    
    def test_success_get_detail_review(self) :
        client = Client()
        
        response = client.get('/movies/1/1')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'detail_review' : {
                'id'         : 1,
                'title'      : '재밌어요',
                'rating'     : '9.00',
                'created_at' : Review.objects.get(id=1).created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    
    def test_failure_get_detail_review_raise_review_does_not_exist(self) :
        client = Client()
        
        response = client.get('/movies/1/111')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'REVIEW_DOES_NOT_EXIST'})
    
    def test_success_update_review(self) :
        client = Client()
        
        data = {
            'text' : 'hihi',
            'rating' : 5.5
        }
        
        response = client.put('/movies/1/1', json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'UPDATED_SUCCESS'})
    
    def test_failure_update_review_raise_review_does_not_exist(self) :
        client = Client()
        
        data = {
            'text' : 'hihi',
            'rating' : 5.5
        }
        
        response = client.put('/movies/1/11111', json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'REVIEW_DOES_NOT_EXIST'})
    
    def test_success_delete_review(self) :
        client = Client()
        
        response = client.delete('/movies/1/1')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'DELETED_SUCCESS'})
    
    def test_failure_delete_review_raise_review_does_not_exist(self) :
        client = Client()
        
        response = client.delete('/movies/1/111111')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'REVIEW_DOES_NOT_EXIST'})