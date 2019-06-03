from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static
from urllib.parse import unquote
from source.chimpanzee import *
from static.database import *

@csrf_exempt
def home(request):
    videos = getVideos()
    filteredVideos = getFilteredVideos(
        videos=videos,
        guest=unquote(request.GET.get("guest", "")),
        category=unquote(request.GET.get("category", "All")),
        sort=request.GET.get("sort", "Date"),
        order=request.GET.get("order", "ascending")
    )
    return JsonResponse(
        data=filteredVideos,
        json_dumps_params={"indent": 4},
        safe=False
    )

@csrf_exempt
def staticHome(request):
    videos = allVideos
    filteredVideos = getFilteredVideos(
        videos=videos,
        guest=unquote(request.GET.get("guest", "")),
        category=unquote(request.GET.get("category", "All")),
        sort=request.GET.get("sort", "Date"),
        order=request.GET.get("order", "ascending")
    )
    return JsonResponse(
        data=filteredVideos,
        json_dumps_params={"indent": 4},
        safe=False
    )
