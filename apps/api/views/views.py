from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def index(request):
    """Test endpoint"""
    return JsonResponse({"msg": "API View"}, safe=False)
