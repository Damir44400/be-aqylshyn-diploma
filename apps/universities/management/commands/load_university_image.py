import time
import requests
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from apps.universities.models import University


class Command(BaseCommand):
    def _get_driver(self):
        options = Options()
        options.add_argument("--headless")  # run in background
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)

    def _search_image(self, query):
        driver = self._get_driver()
        try:
            search_url = f"https://www.google.com/search?tbm=isch&q={query}"
            driver.get(search_url)
            time.sleep(2)
            thumbnails = driver.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
            if thumbnails:
                thumbnails[0].click()
                time.sleep(2)
                images = driver.find_elements(By.CSS_SELECTOR, "img.n3VNCb")
                for img in images:
                    src = img.get_attribute("src")
                    if src and src.startswith("http"):
                        return requests.get(src).content
        except Exception as e:
            print(f"Error for query {query}: {e}")
        finally:
            driver.quit()
        return None

    def handle(self, *args, **options):
        universities = University.objects.all()
        for university in universities:
            print(f"Searching image for: {university.name}")
            image_data = self._search_image(university.name)
            if image_data:
                image_file = ContentFile(image_data)
                university.image.save(f"{university.name}.jpg", image_file)
                university.save()
                print(f"Saved image for: {university.name}")
            else:
                print(f"No image found for: {university.name}")
