from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static
from urllib.parse import unquote
from source.main import *

@csrf_exempt
def requestYouTubeDataAPI(request):
    videos = getVideos()
    saveToStatic(videos, "static/database.json")
    return redirect("/")

@csrf_exempt
def requestStaticDatabase(request):
    videos = readFromStatic("static/database.json")
    filteredVideos = getFilteredVideos(
        videos=videos,
        guest=unquote(request.GET.get("guest", "")),
        category=unquote(request.GET.get("category", "All")),
        sort=request.GET.get("sort", "Date"),
        order=request.GET.get("order", "Descending")
    )
    return JsonResponse(
        data=filteredVideos,
        json_dumps_params={"indent": 4},
        safe=False
    )
