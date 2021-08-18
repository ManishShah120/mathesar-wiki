import os
import sys
import logging
import urllib3
from concurrent import futures
import multiprocessing as mp
from collections import defaultdict

from actions_toolkit import core

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util import get_files, get_image_links, get_links, is_url
from authentication import authenticate_hackmd, USER_AGENT

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("link-rot-detection")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SKIP_LINKS = {
    "http://matrix.mathesar.org/",
    "https://github.com/centerofci/mathesar-wiki"
}
HEADERS = {"User-Agent": USER_AGENT}
TIMEOUT = 10.0


def link2path(link):
    """
    Convert wiki.js style relative link to file path
    """
    # Remove styling that might be part of image links
    link = link.split(" ")[0]
    # Add .md extension is there is no extension
    _, ext = os.path.splitext(link)
    if not ext:
        link += ".md"
    return link


def is_success_code(return_code):
    """
    Returns true if return_code is a success code, otherwise false
    """
    if return_code >= 200 and return_code < 400:
        return True
    return False


def check_external_link(session, link):
    """
    Checks if an external link exists
    """
    response = session.get(link,
                           verify=False,
                           headers=HEADERS,
                           timeout=TIMEOUT)
    return response.status_code


def resolve_dot_path(link, file):
    """
    Resolves paths that start with dots
    """
    file = os.path.dirname(file)
    while link and link.startswith("./") or link.startswith("../"):
        if link.startswith("./"):
            link = link[2:]
        elif link.startswith("../"):
            link = link[3:]
            file = os.path.dirname(file)
    return os.path.join(file, link)


def resolve_dir_path(link, file):
    """
    Resolves paths that search from a directory
    """
    # Directory name would be filename without extension
    dir_name = os.path.splitext(file)[0]
    if os.path.exists(dir_name):
        return os.path.join(dir_name, link)
    # If dir doesn't exist, we assume we search from current directory
    else:
        parent_dir = os.path.dirname(file)
        return os.path.join(parent_dir, link)


def relative2absolute(link, file):
    """
    Converts a relative link to an absolute link

    Three modes of relative path:
        './': Search from parent directory of file
        '../': Search from parent of parent directory of file
        No prefix: Search inside directory of same name as file
    """
    if link.startswith("./") or link.startswith("../"):
        return resolve_dot_path(link, file)
    else:
        return resolve_dir_path(link, file)


def check_local_link(link, file):
    """
    Checks if a local link exists
    """
    link = link2path(link)
    if not link.startswith("/"):
        link = relative2absolute(link, file)
    else:
        link = link.lstrip("/")

    if link is not None and os.path.exists(link):
        return 200
    else:
        return 404


def check_link(session, cache, link):
    """
    Checks to see if a link is valid

    Args:
        session: requests.Session, current session to make requests with
        cache: dict, a cache of links mapped to their responses
        link: dict, link of the form:
            {"link": "link.com", "file": "parent.md"}
    Returns:
        link: dict, link of the form:
            {"link": "link.com", "file": "parent.md", "return_code": 200}
    """
    if is_url(link["link"]):
        if link["link"] in cache:
            link["return_code"] = cache[link["link"]]
        else:
            link["return_code"] = check_external_link(session, link["link"])
            cache[link["link"]] = link["return_code"]
    else:
        link["return_code"] = check_local_link(link["link"], link["file"])

    core.info(f"[{link['return_code']}] link: {link['link']} | "
              f"parent: {link['file']}")
    return link


def check_links(session, links):
    """
    Checks a list of links and returns a dict of errors

    Args:
        session: requests.Session, current session to make requests with
        links: list of dicts, where each dict is a link of the form:
            {"link": "link.com", "file": "parent.md"}
    Returns:
        links: list of dicts, where each dict is a link of the form:
            {"link": "link.com", "file": "parent.md", "return_code": 200}
    """
    cache = {}
    num_threads = mp.cpu_count() * 4
    with futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        links = executor.map(lambda link: check_link(
            session,
            cache,
            link,
        ), links)
    return links


def detect_link_rot(skip_links):
    """
    Gathers all links (image and otherwise) in the root directory, then
    checks whether they are reachable or not.

    Args:
        skip_links: list of links to skip over
    """
    session = authenticate_hackmd(logger)

    # Get all files
    md_files = get_files(".", logger, [".md"])
    md_files = md_files[".md"]

    # Get all links
    links = []
    for md_file in md_files:
        f = md_file.lstrip("./")
        links += [{"link": l, "file": f} for l in get_links(md_file)]
        links += [{"link": l, "file": f} for l in get_image_links(md_file)]

    # Process links
    skip_links = set(skip_links)
    links = [l for l in links if l["link"] not in skip_links]
    links = check_links(session, links)

    # Map errors to files
    all_errors = defaultdict(list)
    for link in links:
        if not is_success_code(link["return_code"]):
            error = f"[{link['return_code']}] {link['link']}"
            all_errors[link["file"]].append(error)

    # Build final error message
    count = 0
    error_msg = ""
    for md_file, errors in all_errors.items():
        error_msg += f"\n{md_file}:"
        count += len(errors)
        for error in errors:
            error_msg += f"\n  {error}"
    if error_msg:
        error_msg = f"{count} Broken links found!" + error_msg
        core.set_failed(error_msg)


if __name__ == "__main__":
    detect_link_rot(SKIP_LINKS)
