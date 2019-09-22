#! /usr/bin/env python3.7

"""
Image Downloader.

A program that takes a plain text file with a list of urls (one per line)
as an argument and downloads all images, storing them on the local hard disk.
"""
import logging
import os
import shutil
from pathlib import Path
from urllib import request
from urllib import parse
from urllib import error

URL_LENGTH_MIN = 10  # too short for a valid URL of an image

IMAGE_COUNTER = 0

RET_OK = 0
RET_PARAM_MISSING = 1
RET_FILE_INVALID = 2


class InvalidInputFileException(Exception):
    """Common exception if the input file in not valid in some way."""

    pass


def check_file(fname):
    """Check if the file with links is usable."""
    infile = Path(fname).resolve()
    if not infile.is_file() or not os.access(infile, os.R_OK):
        raise InvalidInputFileException("File not found or not accessible.")

    return infile


def is_valid(url, scheme):
    """Verify the validity of the url (very simple)."""
    if url == "" or len(url) < URL_LENGTH_MIN:
        return False

    parts = parse.urlparse(url)
    if parts.scheme not in scheme:
        return False

    if not parts.netloc or not parts.path:
        return False

    try:
        request.urlopen(url)
    except error.HTTPError:
        return False
    return True


def get_size(url):
    """Get image size."""
    img_data = request.urlopen(url).info()
    return int(img_data.get("Content-Length", 0))


def gen_fname(url):
    """Extract file name from url."""
    global IMAGE_COUNTER
    fname = url.split("/")[-1].strip()
    if fname == "":
        LOGGER.warning("Couldn't extract the file name, using default")
        fname = "image{}".format(IMAGE_COUNTER)
    return fname


def get_image(url, fname):
    """Download the image as fname."""
    global IMAGE_COUNTER
    try:
        request.urlretrieve(url, fname)
        IMAGE_COUNTER += 1
    except error.URLError:
        LOGGER.warning("Download failed for the url {}".format(url))


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("This program expects one parameter, a name of a file", end=" ")
        print("(incl. path if necessary)")
        print("containing the links to the image files, one link per line.")
        sys.exit(RET_PARAM_MISSING)

    LOGGER = logging.getLogger("idl")
    LOGGER.setLevel("INFO")

    try:
        INFILE = check_file(sys.argv[1])
    except InvalidInputFileException as e:
        LOGGER.error(e.args[0])
        sys.exit(RET_FILE_INVALID)

    FS_FREE = shutil.disk_usage(Path(os.getcwd())).free

    with open(INFILE, "r") as f:
        for LINK in f:
            LINK = LINK.strip()
            LOGGER.debug("Processing url {}".format(LINK))
            # maybe too restrictive - but can be easily modified
            if is_valid(LINK, scheme=["https", "http"]):
                FNAME = gen_fname(LINK)
                IMGSIZE = get_size(LINK)
                if IMGSIZE == 0:
                    # no Content-Length was provided
                    IMGSIZE = os.stat(Path(FNAME).resolve()).st_size
                if IMGSIZE < FS_FREE:
                    get_image(LINK, FNAME)
                    FS_FREE -= IMGSIZE
                else:
                    LOGGER.error("Not enough space on the disk.")
                    LOGGER.error("Couldn't download {}".format(LINK))
            else:
                LOGGER.warning(
                    "URL {} is invalid or inaccessible, skipping.".format(
                        LINK.strip()
                    )
                )
    LOGGER.info(
        "Downloaded {} files to the current folder".format(IMAGE_COUNTER)
    )
