from django.core.management.base import BaseCommand, CommandError
from source.main import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        print(powerful_api_key)
        videos = getVideos()
        saveToStatic(videos, "static/database.json")
