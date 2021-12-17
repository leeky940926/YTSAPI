import json
import requests

from django.views import View
from django.http  import JsonResponse

class MovieView(View) :
    def get(self, request) :         
        return JsonResponse({'message' : 'Initial Setting'}, status=200)