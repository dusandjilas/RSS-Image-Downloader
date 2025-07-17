# RSS & Image Downloader

A simple desktop GUI app for downloading RSS feeds and all related images to a user-defined folder. Built with Python and Tkinter.

---

## Features

- Accepts any RSS feed URL  
- Downloads:
  - The full RSS feed as XML
  - All images found in the feed (via `<img>` tags and media content)
- Easy-to-use GUI (Tkinter)
- Downloads run in a separate thread (no freezing UI)
- Lets user pick the target download folder
- Fully self-contained app – can be converted into a `.exe` file



---

## Getting Started

### Requirements

- Python 3.8+
- `feedparser`
- `requests`

Install dependencies:

```bash
pip install feedparser requests
```

Run the App
```bash
python main.py
```
Made by Dušan Đilas
