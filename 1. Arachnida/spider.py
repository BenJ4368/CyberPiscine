import sys          #Import the system module
import argparse     #Import the parse module
import os           #Import the os module
import requests     #Import the requests module
from bs4 import BeautifulSoup  #Import the BeautifulSoup module
from urllib.parse import urljoin, urlparse  #Import the urljoin and urlparse modules



# HTTP Headers to simulate a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
# Target image extensions
TARGET_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}

# Fetch the HTML content of a web page
def fetch_page_content(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error while accessing {url}: {e}")
        return None

# Extract image URLs from the HTML content of a web page
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

# Download an image from a URL and save it to a folder
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

        print(f"Downloaded : {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"Error while downloading {url}: {e}")


def scrape_images_recursively(url, output_folder, depth, visited):
    # check if the depth is 0 or if the URL has already been visited
    if depth == 0 or url in visited:
        return
    
    visited.add(url) # set the URL as visited

    html_content = fetch_page_content(url)
    if not html_content:
        return
    image_urls = extract_image_urls(html_content, url)
    for img_url in image_urls:
        download_image(img_url, output_folder)
    
    soup = BeautifulSoup(html_content, "html.parser")
    for link in soup.find_all("a"):
        next_url = link.get("href")
        if (next_url):
            next_url - urljoin(url, next_url)
            if urlparse(next_url).netloc == urlparse(urlparse(url).netloc):
                scrape_images_recursively(next_url, output_folder, depth - 1, visited)
    

def main():
    parser = argparse.ArgumentParser(description="Spider: scraping tool")   # Create a parser object
    
    parser.add_argument("url", type=str, help="Target URL")
    parser.add_argument("-r", action="store_true", help="Recursive")
    parser.add_argument("-l", type=int, default=5, help="Max recursion depth (default: 5)")
    parser.add_argument("-p", type=str, default="./data/", help="Output folder (default: ./data/)")
    # "url" is a positional argument, while "-r", "-l", and "-p" are optional because of their "-"

    args = parser.parse_args()  # store all arguments in the args variable
                                # args.url | args.r | args.l | args.p

    # Create the output folder if it doesn't exist
    output_folder = args.p
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    visisted = set()  # Set to store visited URLs (unordered list wuithout duplicates)
    if args.r:
        scrape_images_recursively(args.url, output_folder, args.l, visisted)
    else:
        html_content = fetch_page_content(args.url)
        if html_content:
            image_urls = extract_image_urls(html_content, args.url)
            for img_url in image_urls:
                download_image(img_url, output_folder)


# Entry point of the script
if __name__ == "__main__":
    sys.exit(main())