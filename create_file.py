import os
import img2pdf
from zipfile import ZipFile
import argparse
import shutil

def create_cbz(image_files, cbz_filename):
    print(f"Creating CBZ file: {cbz_filename}")
    with ZipFile(cbz_filename, 'w') as cbz:
        for img_file in image_files:
            cbz.write(img_file, os.path.basename(img_file))
    print(f"CBZ file created successfully: {cbz_filename}")

def create_pdf(image_files, pdf_filename):
    print(f"Creating PDF file: {pdf_filename}")
    try:
        with open(pdf_filename, 'wb') as f:
            f.write(img2pdf.convert(image_files))
        print(f"PDF file created successfully: {pdf_filename}")
    except Exception as e:
        print(f"Error creating PDF file: {e}")

def main():
    parser = argparse.ArgumentParser(description='Create a CBZ or PDF file from images in a specified folder.')
    parser.add_argument('-filetype', type=str, choices=['all', 'cbz', 'pdf'], default='all', help='The file type to save the comic as (default: all)')
    parser.add_argument('-folder', type=str, required=True, help='The folder containing downloaded images')
    parser.add_argument('-filename', type=str, required=True, help='The filename for the comic')
    parser.add_argument('--delete', dest='delete', action='store_true', help='Delete the downloaded_images folder after creating the files')
    parser.add_argument('--no-delete', dest='delete', action='store_false', help='Do not delete the downloaded_images folder after creating the files')
    parser.set_defaults(delete=False)
    args = parser.parse_args()

    file_type = args.filetype
    folder_name = args.folder
    file_name = args.filename 
    delete_folder = args.delete

    if not os.path.exists(folder_name):
        print(f"The folder {folder_name} does not exist.")
        return

    download_folder = os.path.join(folder_name, 'downloaded_images')
    print(download_folder)
    if not os.path.exists(download_folder):
        print("Download folder does not exist. Exiting.")
        return

    image_files = sorted([os.path.join(download_folder, file) for file in os.listdir(download_folder) if file.endswith(('.jpg', '.jpeg', '.png'))])

    if not image_files:
        print(f"No images found in the folder {folder_name}.")
        return

    cbz_filename = os.path.join(folder_name, f"{file_name}.cbz")
    pdf_filename = os.path.join(folder_name, f"{file_name}.pdf")

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
