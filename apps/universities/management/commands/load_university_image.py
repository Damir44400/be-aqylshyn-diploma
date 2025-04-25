import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from apps.universities.models import University

UNSPLASH_ACCESS_KEY = "7Eh_JiJRhfq_B-TIzziQF8uyYhBTlariJDnGfTgh6gQ"
UNSPLASH_URL = "https://api.unsplash.com/search/photos"


def get_unsplash_image(query):
    params = {
        "query": query,
        "per_page": 1,
        "orientation": "landscape",
        "client_id": UNSPLASH_ACCESS_KEY,
    }
    try:
        response = requests.get(UNSPLASH_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data["results"]:
            img_url = data["results"][0]["urls"]["full"]
            img_data = requests.get(img_url, timeout=10).content
            return img_data
    except Exception as e:
        print(f"Failed to fetch from Unsplash for '{query}': {e}")
    return None


class Command(BaseCommand):
    help = "Load and save university images from Unsplash"

    def handle(self, *args, **options):
        universities = University.objects.all()
        for university in universities:
            self.stdout.write(f"Searching Unsplash for: {university.name}")
            image_data = get_unsplash_image(university.name)

            if image_data:
                university.image.save(f"{university.name}.jpg", ContentFile(image_data))
                university.save()
                self.stdout.write(self.style.SUCCESS(f"Saved image for: {university.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"No image found for: {university.name}"))
