import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, args):
        self.args = args

    def fetch_content(self):
        try:
            response = requests.get(self.args.URL)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching URL content: {e}")
            return None

    def run(self):
        content = self.fetch_content()
        images = content.find_all('img') if content else []
        for img in images:
            print(img.get('src'))
        # get content using url
        # get all images using the url
        # recursivly get images