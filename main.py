import feedparser
import requests
import os
import re
import threading
import tkinter as tk
from tkinter import messagebox, ttk, filedialog





def download_feed(rss_url, download_folder):
    
    images_folder = os.path.join(download_folder, 'images')
    rss_feed_folder = os.path.join(download_folder, 'RSS feed')
    
    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(rss_feed_folder, exist_ok=True)

    base_url = '/'.join(rss_url.split('/')[:3])
    
    try:
        log_message("Downloading RSS feed")
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()

        rss_xml_path = os.path.join(rss_feed_folder, 'rss.xml')
        with open(rss_xml_path, 'wb') as f:
            f.write(response.content)

        log_message(f"RSS feed saved to:{download_folder} / {rss_xml_path}")
    except Exception as e:
        log_message(f"Failed to download RSS feed: {e}")
        return

    feed = feedparser.parse(rss_url)

    for entry in feed.entries:
        

        image_urls = []

        if 'media_content' in entry and entry.media_content:
            for media in entry.media_content:
                url = media.get('url')
                if url:
                    image_urls.append(url)

        if 'content' in entry:
            html = entry.content[0].value
            imgs = re.findall(r'<img[^>]+src="([^">]+)"', html)

            for img_url in imgs:
                if img_url.startswith('/'):
                    img_url = base_url + img_url
                image_urls.append(img_url)

        image_urls = list(set(image_urls))

        log_message(f"Downloading Images")

        for image_url in image_urls:
            image_name = os.path.join(images_folder, os.path.basename(image_url.split("?")[0]))
            try:
                img_data = requests.get(image_url, timeout=10).content
                with open(image_name, 'wb') as x:
                    x.write(img_data)
                log_message(f"Downloaded: {image_name}")
            except Exception as e:
                log_message(f"Failed to download {image_url}: {e}")

    log_message("Download complete")


def start_download_thread():
    rss_url = entry.get().strip()
    download_folder = folder_path_var.get().strip()

    if not rss_url:
        log_message("Please enter a valid RSS feed URL.")
        return
    
    if not download_folder:
        log_message("Please select a valid download folder.")
        return
    
    thread = threading.Thread(target=download_feed, args=(rss_url,download_folder))
    thread.start()


def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path_var.set(folder_selected)

def log_message(msg):
    log_text.config(state='normal')
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)
    log_text.config(state='disabled')


# GUI Setup
root = tk.Tk()
root.title("RSS And Image Downloader")
root.geometry("500x450")
root.resizable(True, True)

frame = tk.Frame(root)
frame.pack(pady=10)

label = tk.Label(frame, text="Download RSS feed and images from:")
label.pack()

entry = tk.Entry(frame, width=50)
entry.insert(0, "Enter RSS feed url")
entry.pack(pady=5)

folder_frame = tk.Frame(root)
folder_frame.pack(pady=5)

folder_label = tk.Label(folder_frame, text="Download folder:")
folder_label.pack(side=tk.LEFT)

folder_path_var = tk.StringVar()
folder_entry = tk.Entry(folder_frame, textvariable=folder_path_var, width=45)
folder_entry.pack(side=tk.LEFT, padx=5)

browse_button = tk.Button(folder_frame, text="Browse", command=browse_folder)
browse_button.pack(side=tk.LEFT)

start_button = tk.Button(frame, text="Download", command=start_download_thread)
start_button.pack(pady=10)

log_text = tk.Text(root, height=15, state='disabled', wrap='word')
log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

root.mainloop()
