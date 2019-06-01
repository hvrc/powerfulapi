from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static
from urllib.parse import unquote
from source.chimpanzee import *

@csrf_exempt
def home(request, guest):
    videos = getVideos()
    filteredVideos = getFilteredVideos(
        videos=videos,
        guest=unquote(guest) if guest != "All" else "",
        category=unquote(request.GET.get("category", "All")),
        sort=request.GET.get("sort", "Date"),
        order=request.GET.get("order", "ascending")
    )
    return JsonResponse(
        data=filteredVideos,
        json_dumps_params={"indent": 4},
        safe=False
    )
