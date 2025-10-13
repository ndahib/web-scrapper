# 🕷️ Spider Web Scraper

A command-line web scraper tool written in Python to extract images, links, emails, phone numbers, and physical addresses from a given URL. Supports recursive scraping with configurable depth levels.

---

## Features

- Scrape:
  - 🌐 Links
  - 🖼️ Images
  - 📧 Emails
  - 📞 Phone numbers
  - 🏠 Physical addresses
- Recursive scraping up to a specified depth
- Save output to a custom file path
- Simple CLI interface

---

## Usage

```bash
python spider.py [-h] [-r] [-l [LEVEL]] [-p [PATH]] {images,links,emails,phones,address,all} URL
