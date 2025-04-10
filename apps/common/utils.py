import requests
from bs4 import BeautifulSoup


def get_image_url(image_query: str) -> str | None:
    search_url = f"https://www.google.com/search?q={image_query}&tbm=isch"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")
    img_tag = soup.find("img", {"class": "yWs4tf"})
    if img_tag is not None:
        img_link = img_tag.get("src")
        return img_link
    else:
        print("No image found on the page.")
