import requests
from bs4 import BeautifulSoup
from bson import ObjectId
import os

class ScraperService:
    def get_metadata(self, url):
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        print(soup)
        title = soup.title.string if soup.title else ''
        description = soup.find('meta', attrs={'name': 'description'})
        description = description['content'] if description else ''
        image = soup.find('meta', attrs={'property': 'og:image'})
        image = image['content'] if image else ''

        return {'title': title, 'description': description, 'image': image}