from django.core.management.base import BaseCommand, CommandError
from source.main import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("I'm working!")
        videos = getVideos()
        saveToStatic(videos, "static/database.json")
