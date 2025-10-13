import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
from dns import resolver, exception
from urllib.robotparser import RobotFileParser
from ..constants import SubcommandChoices, EXTENSIONS, USER_AGENT
from selenium import webdriver
import base64
import uuid


class Scraper:
    def __init__(self, args):
        self.args = args
        self.emails_set = set()

    def fetch_content(self, url) -> BeautifulSoup | None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        content = driver.page_source
        driver.quit()
        return BeautifulSoup(content, "html.parser")

    def scrape_images(self, content, url):
        print("Scraping images...")
        images = content.find_all("img") if content else []

        for img in images:
            image_src = img.get("src")
            print("image_src", image_src)
            if not image_src:
                continue

            if image_src.startswith("data:image/"):
                self.save_base64_image(image_src)
                continue

            self.save_image_from_url(image_src, url)

    def save_base64_image(self, base64_str):
        print("Found base64 image...")
        try:
            image_data = base64.b64decode(base64_str.split(",")[1])
            image_extension = self.get_extension_from_base64(base64_str)
            image_filename = f"image_{uuid.uuid4()}{image_extension}"
            image_path = os.path.join(self.args.path, image_filename)

            with open(image_path, "wb") as file:
                file.write(image_data)
            print(f"Saved base64 image as {image_filename}")
        except Exception as e:
            print(f"Error saving base64 image: {e}")

    def get_extension_from_base64(self, base64_str):
        """Guess the extension from the base64 string."""
        mime_type = base64_str.split(";")[0].split("/")[1]
        return f".{mime_type}"

    def save_image_from_url(self, image_src, base_url):
        image_extension = os.path.splitext(os.path.basename(image_src))[-1].lower()
        if image_extension not in EXTENSIONS:
            print(f"Skipping unsupported image extension: {image_extension}")
            return

        image_url = image_src if image_src.startswith("http") or image_src.startswith("https") else urljoin(base_url, image_src)
        try:
            response = requests.get(image_url, headers={"User-Agent": USER_AGENT})
            response.raise_for_status()
            image_filename = os.path.basename(image_url)
            image_path = os.path.join(self.args.path, image_filename)

            with open(image_path, "wb") as file:
                file.write(response.content)
            print(f"Saved image from URL: {image_filename}")
        except requests.RequestException as e:
            print(f"Error downloading image: {e}")

    @classmethod
    def dns_lookup(cls, domain):
        try:
            answers = resolver.resolve(domain, "MX", lifetime=5)
            return bool(answers)
        except resolver.NoAnswer:
            try:
                answers = resolver.resolve(domain, "A", lifetime=5)
                return bool(answers)
            except (resolver.NoAnswer, exception.Timeout, resolver.NXDOMAIN):
                return False
        except (exception.Timeout, resolver.NXDOMAIN):
            return False
        except exception.DNSException:
            return False

    def scrape_emails(self, content: BeautifulSoup | None):
        print("Scraping emails...")
        if not content:
            return
        text = content.get_text()
        emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text))
        # to remove later
        links = content.find_all("a", href=True)
        for link in links:
            href = link.get("href")
            if isinstance(href, (list, tuple)):
                href = href[0] if href else None
            if not href or not isinstance(href, str):
                continue
            if href.startswith("mailto:"):
                print(f"Processing mailto link: {href}")
                email = href.split("mailto:")[1].split("?")[0]
                emails.add(email)

        new_emails = emails - self.emails_set
        valid_emails = set()
        for email in new_emails:
            domain = email.split("@")[-1]
            if not self.dns_lookup(domain):
                print(f"Invalid email domain, skipping: {email}")
                continue
            print(f"Valid email found: {email}")
            valid_emails.add(email)
        self.emails_set.update(valid_emails)
        print(f"Found {len(valid_emails)} emails in text.")
        if self.args.path and valid_emails:
            emails_file = os.path.join(self.args.path, "emails.txt")
            print(f"Saving {len(valid_emails)} unique emails to {emails_file}")
            with open(emails_file, "a") as file:
                for email in sorted(valid_emails):
                    file.write(email + "\n")

    def check_robot_txt(self, url, user_agent: str = "*") -> bool:
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        robots_url = f"{base_url}/robots.txt"
        if not self.dns_lookup(parsed_url.netloc):
            print(f"Invalid domain, skipping: {url}")
            return True
        rp = RobotFileParser()
        rp.set_url(robots_url)
        try:
            rp.read()
        except Exception as e:
            print(f"Could not read robots.txt: {e}")
            return True

        return rp.can_fetch(user_agent, url)

    def scrape_links(self, content, url):
        print("scrapping links ....")
        if not content:
            return

        links = content.find_all("a") if content else []
        for link in links:
            href = link.get("href")
            if isinstance(href, (list, tuple)):
                href = href[0] if href else None
            if not href or not isinstance(href, str):
                continue
            href = href.split("#")[0]
            full_url = href if href.startswith(("http://", "https://")) else urljoin(url, href)
            links_file = os.path.join(self.args.path, "links.txt")
            with open(links_file, "a") as file:
                file.write(full_url + "\n")

    def scrape_phones(self, content, url):
        if not content:
            return
        print("scraping phone numbers...")
        # need more work
        text = content.get_text()
        numbers = re.findall(r"(?:\+212|00212|0)[\d\.\-\s(\)]{8, 20}", text)
        numbers_file = os.path.join(self.args.path, "numbers.txt")
        for number in numbers:
            with open(numbers_file, "a") as file:
                file.write(number + "\n")

    def run(self, url=None, current_depth=0, visited=None):
        """Recursively scrape content from URLs."""

        if visited is None:
            visited = set()
        url = url or self.args.URL
        url = url.rstrip("/")
        if url in visited:
            return
        if not self.check_robot_txt(url):
            print(f"Access to {url} is disallowed by robots.txt")
            return
        visited.add(url)
        if self.args.recursive and current_depth >= self.args.level:
            return
        print("Waiting for browser...")
        content = self.fetch_content(url)
        subcommand = self.args.subcommand

        if subcommand == SubcommandChoices.IMAGES:
            self.scrape_images(content, url)
        elif subcommand == SubcommandChoices.LINKS:
            self.scrape_links(content, url)
        elif subcommand == SubcommandChoices.EMAILS:
            self.scrape_emails(content)
        elif subcommand == SubcommandChoices.PHONES:
            self.scrape_phones(content, url)
        elif subcommand == SubcommandChoices.ADDRESS:
            print("Address scraping not implemented yet.")
        elif subcommand == SubcommandChoices.ALL:
            self.scrape_images(content, url)
            self.scrape_emails(content)
            self.scrape_links(content, url)

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
