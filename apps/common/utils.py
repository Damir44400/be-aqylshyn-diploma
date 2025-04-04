import re

import requests
from bs4 import BeautifulSoup


def get_image_url(image_query: str) -> str | None:
    search_url = f"https://www.google.com/search?q={image_query}&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    scripts = soup.find_all("script")

    for script in scripts:
        if 'AF_initDataCallback' in script.text:
            matches = re.findall(r'"(https://[^"]+\.(?:jpg|jpeg|png))"', script.text)
            if matches:
                return matches[0]

    return None
