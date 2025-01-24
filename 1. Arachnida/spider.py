import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse

# En-têtes HTTP pour simuler un navigateur
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def fetch_page_content(url):
    """Télécharge le contenu HTML d'une URL."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'accès à {url}: {e}")
        return None


def extract_image_urls(html_content, base_url):
    """Extrait les URLs des images à partir du contenu HTML."""
    soup = BeautifulSoup(html_content, "html.parser")
    image_urls = []

    for img_tag in soup.find_all("img"):
        img_url = img_tag.get("src")
        if img_url:
            img_url = urljoin(base_url, img_url)  # Résoudre les URLs relatifs
            image_urls.append(img_url)

    return image_urls


def download_image(url, output_folder):
    """Télécharge une image à partir de son URL et l'enregistre dans le dossier spécifié."""
    try:
        response = requests.get(url, headers=HEADERS, stream=True)
        response.raise_for_status()

        # Extraire le nom du fichier de l'URL
        filename = os.path.basename(urlparse(url).path)
        if not filename:  # Si aucun nom, ignorer l'image
            return

        filepath = os.path.join(output_folder, filename)

        # Écrire l'image sur le disque
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Image téléchargée : {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement de l'image {url}: {e}")


def scrape_images(url, output_folder, depth, visited):
    """Télécharge les images d'une page web et explore récursivement selon la profondeur spécifiée."""
    if depth == 0 or url in visited:
        return

    visited.add(url)
    print(f"Exploration de : {url} (profondeur restante : {depth})")

    html_content = fetch_page_content(url)
    if not html_content:
        return

    # Extraire et télécharger les images de la page
    image_urls = extract_image_urls(html_content, url)
    for img_url in image_urls:
        download_image(img_url, output_folder)

    # Si la récursivité est activée, explorer les autres liens
    soup = BeautifulSoup(html_content, "html.parser")
    for link in soup.find_all("a"):
        next_url = link.get("href")
        if next_url:
            next_url = urljoin(url, next_url)  # Résoudre les URLs relatifs
            if urlparse(next_url).netloc == urlparse(url).netloc:  # Limiter au même domaine
                scrape_images(next_url, output_folder, depth - 1, visited)


def main():
    parser = argparse.ArgumentParser(description="Télécharge les images d'une page web.")
    parser.add_argument("url", type=str, help="L'URL du site web à analyser.")
    parser.add_argument("-r", action="store_true", help="Télécharger récursivement toutes les images du site.")
    parser.add_argument("-l", type=int, default=5, help="Profondeur maximale pour la récursivité (par défaut : 5).")
    parser.add_argument("-p", type=str, default="./data/", help="Chemin du dossier de sauvegarde (par défaut : ./data/).")

    args = parser.parse_args()

    # Créer le dossier de sortie s'il n'existe pas
    output_folder = args.p
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    visited = set()  # Ensemble des URLs visitées
    if args.r:
        scrape_images(args.url, output_folder, args.l, visited)
    else:
        html_content = fetch_page_content(args.url)
        if html_content:
            image_urls = extract_image_urls(html_content, args.url)
            for img_url in image_urls:
                download_image(img_url, output_folder)


if __name__ == "__main__":
    main()