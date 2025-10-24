# 🕷️ Spider & 🦂 Scorpion Toolkit

A collection of two powerful Python command-line tools for web scraping and image metadata management.

---

## 🕷️ Spider Web Scraper

A command-line web scraper tool written in Python to extract images, links, emails, phone numbers, and physical addresses from a given URL. Supports recursive scraping with configurable depth levels.

### ✨ Features

- **Scrape:**
  - 🌐 Links
  - 🖼️ Images
  - 📧 Emails
  - 📞 Phone numbers
  - 🏠 Physical addresses
- Recursive scraping up to a specified depth
- Save output to a custom file path
- Simple CLI interface

### 🧰 Usage

```bash
python spider.py [-h] [-r] [-l [LEVEL]] [-p [PATH]] {images,links,emails,phones,address,all} URL
```

### Options

| Option | Description |
|--------|-------------|
| `-h`, `--help` | Show help message and exit |
| `-r`, `--recursive` | Enable recursive scraping |
| `-l [LEVEL]`, `--level [LEVEL]` | Set recursion depth level |
| `-p [PATH]`, `--path [PATH]` | Specify output file or directory path |
| `{images,links,emails,phones,address,all}` | Choose what data to scrape |
| `URL` | Target website URL |

---

## 🦂 Scorpion Metadata Parser

A command-line tool to parse, delete, and modify image metadata. Useful for cleaning, editing, or inspecting image metadata.

### 🧰 Usage

```bash
HELP [-h] [-d] [-t TAG] [-m] [-f [FILE]] FILES [FILES ...]
```

### 📖 Description

Scorpion is designed to parse and manipulate image metadata (EXIF, IPTC, etc.). You can delete, modify, or view metadata tags for one or multiple images.

### Options

| Option | Description |
|--------|-------------|
| `FILES` | The image or list of images to be parsed |
| `-h`, `--help` | Show help message and exit |
| `-d`, `--delete` | Delete metadata of all images |
| `-t TAG`, `--tag TAG` | Delete only the specified metadata tag (used with `-d`) |
| `-m`, `--modify` | Modify metadata of all images |
| `-f [FILE]`, `--file [FILE]` | Specify a single image file to delete or modify metadata for |

---

## 🧩 Example Workflows

### 🔍 Scrape all emails and links recursively

```bash
python spider.py -r -l 2 all https://example.com
```

### 🧹 Remove all metadata from images

```bash
HELP -d *.jpg
```

### ✏️ Delete only the GPS tag from an image

```bash
HELP -d -t GPSInfo image.jpg
```

---

## ⚙️ Requirements

- Python 3.8+
- Requests, BeautifulSoup4 (for Spider)
- Pillow or ExifTool (for Scorpion)

### Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🕸️ Author

**Spider & Scorpion Toolkit** — built for developers who want clean data and clean images.
