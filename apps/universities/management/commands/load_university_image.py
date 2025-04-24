import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.core.management import BaseCommand

from apps.universities.models import University


class Command(BaseCommand):
    def _search_image(self, query):
        try:
            search_url = f"https://www.google.com/search?q={query}&tbm=isch"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            image_tags = soup.find_all("img")
            for img in image_tags:
                src = img.get("src")
                if src and src.startswith("http"):
                    img_data = requests.get(src, timeout=10).content
                    return img_data
        except Exception as e:
            print(f"Error fetching image for {query}: {e}")
            return None

    def handle(self, *args, **options):
        universities = University.objects.all()
        for university in universities:
            if university.image:
                continue
            print(f"Processing {university.name}")
            image_data = self._search_image(university.name)
            if image_data:
                university.image.save(f"{university.name}.jpg", ContentFile(image_data))
                university.save()
                print(f"Image saved for {university.name}")
            else:
                print(f"No image found for {university.name}")
