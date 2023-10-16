from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

# For test purpose only
def index(request):
    """To be used for Testing purpose"""
    return JsonResponse({"msg": "Home View"}, safe=False)
