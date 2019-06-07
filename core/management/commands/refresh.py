from django.core.management.base import BaseCommand, CommandError
from source.main import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        videos = getVideos()
        saveToStatic(videos, "staticfiles/database.json")
