from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static
from urllib.parse import unquote
from source.main import *

@csrf_exempt
def refreshStaticDatabase(request):
    videos = getVideos()
    saveToStatic(videos, "staticfiles/database.json")
    return redirect("/")

@csrf_exempt
def viewStaticDatabase(request):
    videos = readFromStatic("staticfiles/database.json")
    filteredVideos = getFilteredVideos(
        videos=videos,
        guest=unquote(request.GET.get("guest", "")),
        category=unquote(request.GET.get("category", "all")),
        sort=request.GET.get("sort", "publishedAt"),
        order=request.GET.get("order", "descending")
    )
    return JsonResponse(
        data=filteredVideos,
        json_dumps_params={"indent": 4},
        safe=False
    )
