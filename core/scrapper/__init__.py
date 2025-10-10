import requests
from bs4 import BeautifulSoup
import os
from ..constants import SubcommandChoices, EXTENSIONS, USER_AGENT
from urllib.parse import urljoin
import re


class Scraper:
    def __init__(self, args):
        self.args = args
        self.emails_set = set()

    def fetch_content(self, url) -> BeautifulSoup | None:
        try:
            headers = {
                "User-Agent": USER_AGENT,
            }
            # response = requests.options(self.args.URL, headers=headers)
            # response.raise_for_status()
            # if response.status_code == 200:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            print(f"Error fetching URL content: {e}")
            return None

    def scrape_images(self, content, url):
        images = content.find_all("img") if content else []
        for img in images:
            image_src = img.get("src")
            if not image_src:
                continue
            image_extension = os.path.splitext(os.path.basename(image_src))[-1].lower()
            if image_extension not in EXTENSIONS:
                continue
            image_url = image_src if image_src.startswith("http") or image_src.startswith("https") else urljoin(url, image_src)
            print(image_url)
            try:
                response = requests.get(image_url, headers={"User-Agent": USER_AGENT})
                response.raise_for_status()
                with open(os.path.join(self.args.path, os.path.basename(image_url)), "wb") as file:
                    file.write(response.content)
            except requests.RequestException as e:
                print(f"Error downloading image: {e}")

    def scrape_emails(self, content: BeautifulSoup | None):
        print("Scraping emails...")
        if not content:
            return
        text = content.get_text()
        emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text))
        print(f"Found {len(emails)} emails in text.")
        links = content.find_all("a", href=True)
        for link in links:
            href = link.get("href")
            if isinstance(href, (list, tuple)):
                href = href[0] if href else None
            if not href or not isinstance(href, str):
                continue
            if href.startswith("mailto:"):
                print(f"Processing link: {link}")
                email = href.split("mailto:")[1].split("?")[0]
                emails.add(email)
        new_emails = emails - self.emails_set
        self.emails_set.update(new_emails)
        if new_emails and self.args.path:
            with open(os.path.join(self.args.path, "emails.txt"), "a") as file:
                print(f"Saving {len(new_emails)} new emails to {os.path.join(self.args.path, 'emails.txt')}")
                for email in new_emails:
                    file.write(email + "\n")

    def run(self, url=None, current_depth=0, visited=None):
        """Recursively scrape content from URLs."""

        if visited is None:
            visited = set()
        url = url or self.args.URL
        url = url.rstrip("/")
        if url in visited:
            return
        visited.add(url)
        if self.args.recursive and current_depth >= self.args.level:
            return

        content = self.fetch_content(url)
        subcommand = self.args.subcommand

        if subcommand == SubcommandChoices.IMAGES:
            self.scrape_images(content, url)
        elif subcommand == SubcommandChoices.LINKS:
            pass
        elif subcommand == SubcommandChoices.EMAILS:
            self.scrape_emails(content)
        elif subcommand == SubcommandChoices.PHONES:
            pass
        elif subcommand == SubcommandChoices.ADDRESS:
            pass
        elif subcommand == SubcommandChoices.ALL:
            pass

        if self.args.recursive and current_depth < self.args.level:
            links = content.find_all("a") if content else []
            for link in links:
                href = link.get("href")
                if isinstance(href, (list, tuple)):
                    href = href[0] if href else None
                if not href or not isinstance(href, str):
                    continue
                href = href.split("#")[0]
                next_url = href if href.startswith(("http://", "https://")) else urljoin(url, href)
                self.run(url=next_url, current_depth=current_depth + 1, visited=visited)
