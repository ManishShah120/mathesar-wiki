import os
import re
import shutil
import logging

import requests

from authentication import authenticate

BASE_IMAGE_DIR = "assets"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("replace-external-links")

HACKMD_EMAIL = os.environ["HACKMD_EMAIL"]
HACKMD_PASSWORD = os.environ["HACKMD_PASSWORD"]
HACKMD_URL = "https://hackmd.io/login"

def get_image_links(md_file):
    """
    Given a markdown file, find all external image links

    Args:
        md_file: str, path to a markdown file
    Returns:
        links: list of external image link strings
    """
    with open(md_file, 'r') as f:
        # Matches markdown image syntax, capturing image link and image name
        pattern = r'!\[[^\]]*\]\((.*?)\s*("(?:.*[^"])")?\s*\)'
        links = re.findall(pattern, f.read())
    # Currently throw out names, consider using down the line
    links = [link for link, name in links]
    links = list(filter(is_url, links))
    return links

def make_image_paths(md_file, link):
    """
    Generate a path to save to and a relative link that points to it

    Args:
        md_file: str, path to a markdown file
        link: str, external image link
    Returns:
        tuple containing:
            save_path: str, path to save image locally
            rel_path: str, relative link that points to save_path
    """
    md_file = md_file.lstrip("./")
    # Remove '.md'
    md_file = md_file[:-3]

    name = link.split("/")[-1]
    name_parts = name.split(" ")
    name = name_parts[0]
    styling = " ".join(name_parts[1:])

    save_path = os.path.join(BASE_IMAGE_DIR, md_file, name)
    rel_path = "/" + save_path + (" " if styling else "") + styling
    return save_path, rel_path

def download_image(session, link, save_path):
    """
    Download an image

    Args:
        session: requests.Session, current session to make requests with
        link: str, external image link
        save_path: str, path to save the image to
    Returns:
        status_code: int, the status code of the request
    """
    response = session.get(link, stream=True)
    if response.status_code == 200:
        logger.info(f"  Saving {link} to {save_path}...")
        response.raw.decode_content = True
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
    else:
        logger.warning(f"  Failed to download {link}! "
                       f"Error code {response.status_code}")
    return response.status_code

def is_url(link):
    """
    Checks is a link is a url or relative link
    """
    # Looks for text followed by '://' to identify a url
    pattern = r'^[a-z0-9]*:\/\/.*$'
    if re.search(pattern, link):
        return True
    else:
        return False

def get_markdown_files(root):
    """
    Gathers markdown file paths recursively
    """
    logger.info("Gathering markdown files...")
    all_files = []
    for dir_path, dirs, files in os.walk(root):
        all_files.extend([os.path.join(dir_path, f) for f in files
                          if f.endswith(".md")])
    return all_files

def update_markdown_file(md_file, replace_links):
    """
    Replaces urls in a markdown file with relative links

    Args:
        md_file: str, path to a markdown file
        replace_links: list of tuples, where each tuple is of the form (url,
        relative_link). Each url in the markdown file will be replaced with
        it's respective relative link.
    """
    if not replace_links:
        return
    logger.info(f" Replacing links...")
    with open(md_file, 'r') as f:
        text = f.read()
    for link, rel_link in replace_links:
        text = text.replace(link, rel_link)
        logger.info(f"  {link} -> {rel_link}")
    with open(md_file, 'w') as f:
        f.write(text)

def replace_links():
    """
    Iterates over markdown files in the root directory, downloading any
    external images and replacing the urls with relative links
    """
    logger.info("Logging into HackMD...")
    session = authenticate(HACKMD_EMAIL, HACKMD_PASSWORD, HACKMD_URL)
    if session is None:
        logger.warning("HackMD log in unsuccesful!")
        session = requests.Session()
    else:
        logger.info("Logged into HackMD")

    logger.info("Starting image update process...")
    md_files = get_markdown_files(".")
    for md_file in md_files:
        image_links = get_image_links(md_file)
        if image_links:
            logger.info(f"External links found in {md_file}!")
            logger.info(" Starting image download...")
            replace_links = []
            for link in image_links:
                save_path, rel_path = make_image_paths(md_file, link)
                status_code = download_image(session, link, save_path)
                if status_code == 200:
                    replace_links.append((link, rel_path))
            update_markdown_file(md_file, replace_links)

if __name__ == "__main__":
    replace_links()