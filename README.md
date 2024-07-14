# Comics Downloader

A simple python comic book downloader template script that can be used on legal websites that you have the permission to download comics or manga from.

## Requirements - Python

### Download and Install Python (Windows):

- Go to the official Python website.
- Download the latest version of Python for your operating system.
- Run the downloaded installer.
- Ensure you check the option "Add Python to PATH" during installation.
- Complete the installation process.

### Download and Install Python (Linux):

```sh
sudo apt update
sudo apt install python3 python3-venv
```

## Setup

1. Optional - create a virtual environment (Windows)
2. Install necessary packages

```sh
python -m venv .venv
.venv\Scripts\activate
pip install requests beautifulsoup4 img2pdf Pillow
```

1. Optional - create a virtual environment (Linux)
2. Install necessary packages

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4 img2pdf Pillow
```

## Usage (comics_downloader)

You can invoke the --help or -h command.

```sh
# (or python3)
python comics_downloader.py -h
```

Example:

```sh
python comics_downloader.py -filetype pdf -folder "comic name (year)" -filename "comic name v001" -url "http://www.example.com/comic/issue/1"
```

### Tweaks

Update get_image_urls so that only relevant images get updated. For example:

```python
    # only include relevant images based on the domain
    if domain == "comic.example.com":
        img_tags = soup.find_all('img', id=lambda x: x and x.startswith("image_"))
    elif domain == "example.com":
        img_tags = soup.find_all('img', alt=lambda x: x and "Page" in x)
    elif domain == "example2.com":
        img_tags = soup.find_all('img', class_=lambda x: x and "image_" in x)
    else:
        img_tags = soup.find_all('img')
    img_urls = [img['src'] for img in img_tags if 'src' in img.attrs]
```

## Usage (create_file)

You can invoke the --help or -h command.

```sh
# (or python3)
python create_file.py -h
```

Example:

```sh
python create_file.py -filetype cbz -folder "comic name (year)" -filename "comic name v003"
```

## Usage (batch_create_comics.py)

You can invoke the --help or -h command.

```sh
# (or python3)
python batch_create_comics.py -h
```

Example:

```sh
python batch_create_comics.py -filetype pdf -baseurl "http://www.example.com/comic/issue/{issue}" -folder "comic name (year)" -start 1 -end 100
```
