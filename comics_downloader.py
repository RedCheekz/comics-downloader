import requests
from bs4 import BeautifulSoup
import os
import img2pdf
from zipfile import ZipFile
import argparse
from PIL import Image
from io import BytesIO
import sys
from urllib.parse import urlparse
import shutil

def is_valid_image(image_data):
    try:
        image = Image.open(BytesIO(image_data))
        image.verify()
        return True
    except Exception as e:
        print(f"Image validation error: {e}")
        return False

def get_image_urls(url, soup):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # only include relevant images based on the domain
    # update here

    img_tags = soup.find_all('img')
    img_urls = [img['src'] for img in img_tags if 'src' in img.attrs]

    return img_urls

def download_images(url, download_folder):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"Fetching content from URL: {url}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    img_urls = get_image_urls(url, soup)

    print(f"Found {len(img_urls)} images")

    image_files = []
    for i, img_url in enumerate(img_urls):
        if not img_url.startswith(('http', 'https')):
            img_url = requests.compat.urljoin(url, img_url)

        # Display progress on the same line
        print(f"Downloading image {i + 1} of {len(img_urls)}: {img_url}", end='\n')
        try:
            img_response = requests.get(img_url, headers=headers)
            img_response.raise_for_status()
            img_data = img_response.content

            if is_valid_image(img_data):
                img_filename = os.path.join(download_folder, f'image_{i + 1}.jpg')
                with open(img_filename, 'wb') as handler:
                    handler.write(img_data)
                image_files.append(img_filename)
            else:
                print(f"Invalid image format for URL: {img_url}")

        except requests.RequestException as e:
            print(f"Error downloading image {img_url}: {e}")

    print()  # Move to the next line after downloading all images
    return image_files

def create_cbz(image_files, cbz_filename):
    print(f"Creating CBZ file: {cbz_filename}")
    with ZipFile(cbz_filename, 'w') as cbz:
        for img_file in image_files:
            cbz.write(img_file, os.path.basename(img_file))
    print(f"CBZ file created successfully: {cbz_filename}")
    print()

def create_pdf(image_files, pdf_filename):
    print(f"Creating PDF file: {pdf_filename}")
    try:
        with open(pdf_filename, 'wb') as f:
            f.write(img2pdf.convert(image_files))
        print(f"PDF file created successfully: {pdf_filename}")
    except Exception as e:
        print(f"Error creating PDF file: {e}")
    print()

def main():
    parser = argparse.ArgumentParser(description='Download a comic book from a given URL and save it as a CBZ or PDF file.')
    parser.add_argument('-filetype', type=str, choices=['all', 'cbz', 'pdf'], default='all', help='The file type to save the comic as (default: all)')
    parser.add_argument('-url', type=str, required=True, help='The URL of the comic book page')
    parser.add_argument('-folder', type=str, required=True, help='The subfolder to store downloaded images and comic file')
    parser.add_argument('-filename', type=str, required=True, help='The filename for the comic')
    parser.add_argument('--delete', dest='delete', action='store_true', help='Delete the downloaded_images folder after creating the files')
    parser.add_argument('--no-delete', dest='delete', action='store_false', help='Do not delete the downloaded_images folder after creating the files')
    parser.set_defaults(delete=False)
    args = parser.parse_args()

    comic_url = args.url
    file_type = args.filetype
    main_folder = args.folder
    file_name = args.filename 
    delete_folder = args.delete

    # Ensure the main folder exists
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)

    download_folder = os.path.join(main_folder, 'downloaded_images')
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    cbz_filename = os.path.join(main_folder, f"{file_name}.cbz")
    pdf_filename = os.path.join(main_folder, f"{file_name}.pdf")

    image_files = download_images(comic_url, download_folder)

    if not image_files:
        print("No valid images downloaded. Exiting.")
        return

    if (file_type == 'cbz') or (file_type == 'all'):
        create_cbz(image_files, cbz_filename)
    if (file_type == 'pdf') or (file_type == 'all'):
        create_pdf(image_files, pdf_filename)

    if delete_folder:
        print(f"Deleting folder: {download_folder}")
        shutil.rmtree(download_folder)
        print(f"Folder {download_folder} deleted successfully.")

if __name__ == '__main__':
    main()
