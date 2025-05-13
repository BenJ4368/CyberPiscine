import sys
import argparse
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import shutil

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
TARGET_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}

visited = set()

def print_downloading(msg, jump):
    if jump is False:
        term_width = shutil.get_terminal_size().columns
        msg = msg[:term_width - 1]
        sys.stdout.write("\r" + msg)
        sys.stdout.write("\033[K")
        sys.stdout.flush()
    else:
        term_width = shutil.get_terminal_size().columns
        msg = msg[:term_width - 1]
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.flush()
        print(msg)


def fetch_page_content(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print_downloading("Error: " + str(e), False)
        return None
    

def extract_image_urls(html_content, base_url):
    soup = BeautifulSoup(html_content, "html.parser")
    image_urls = []

    for img_tag in soup.find_all("img"):
        img_url = img_tag.get("src")
        if img_url:
            img_url = urljoin(base_url, img_url)
            if os.path.splitext(urlparse(img_url).path)[1].lower() in TARGET_EXTENSIONS:
                image_urls.append(img_url)
    return image_urls


def download_image(url, output_folder):
    try:
        response = requests.get(url, headers=HEADERS, stream=True)
        response.raise_for_status()

        filename = os.path.basename(urlparse(url).path)
        if not filename:
            return
        filepath = os.path.join(output_folder, filename)

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print_downloading(f"Downloaded: {filename}", False)

    except requests.exceptions.RequestException as e:
        print_downloading("Error: " + str(e), False)


def scrape_images(url, output_folder, depth, prefix="", is_last=True):
    if depth <= 0 or url in visited:
        return

    visited.add(url)

    connector = "└── " if is_last else "├── "
    print_downloading(f"{prefix}{connector}[{depth}] {url}", True)

    html_content = fetch_page_content(url)
    if not html_content:
        return

    image_urls = extract_image_urls(html_content, url)
    for img_url in image_urls:
        download_image(img_url, output_folder)

    soup = BeautifulSoup(html_content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a") if link.get("href")]
    child_links = []

    base_url_no_fragment = url.split("#")[0]

    for next_url in links:
        full_url = urljoin(url, next_url)
        parsed = urlparse(full_url)

        # Ignore les ancres internes
        if parsed.fragment:
            continue

        # Ne traite pas la même page plusieurs fois (même sans #)
        if full_url.split("#")[0] == base_url_no_fragment:
            continue

        if parsed.netloc == urlparse(url).netloc and full_url not in visited:
            child_links.append(full_url)

    for i, next_url in enumerate(child_links):
        last = (i == len(child_links) - 1)
        new_prefix = prefix + ("    " if is_last else "│   ")
        scrape_images(next_url, output_folder, depth - 1, new_prefix, last)

def main():
    parser = argparse.ArgumentParser(description="Spider: scraping tool")
    parser.add_argument("url", type=str, help="Target URL")
    parser.add_argument("-r", action="store_true", help="Recursive")
    parser.add_argument("-l", type=int, default=5, help="Max recursion depth (default: 5)")
    parser.add_argument("-p", type=str, default="./data/", help="Output folder (default: ./data/)")
    args = parser.parse_args()

    output_folder = args.p
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print(f"Scraping images from {args.url}")
    scrape_images(
        args.url,
        output_folder,
        args.l if args.r else 1,
        prefix="",
        is_last=True
    )

    print()  # Pour ne pas rester bloqué sur la ligne dynamique à la fin

if __name__ == "__main__":
    sys.exit(main())
