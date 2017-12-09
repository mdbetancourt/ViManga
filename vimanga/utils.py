"""Utilities functions"""

import io
import os
from multiprocessing.dummy import Pool
from types import GeneratorType

import requests

from tqdm import tqdm

def download_image(info):
    """Download and convert image"""
    index, link = info
    success = False

    while not success:
        data = requests.get(link)
        success = data.ok

    return index, data.content


def download_chapter(link_list: GeneratorType, threads=4, progress=None):
    """Return a list of images"""
    links = list(link_list)
    enumerate_links = enumerate(links)
    len_links = len(links)
    images = []
    pool = Pool(processes=threads)
    generator = pool.imap_unordered(download_image, enumerate_links)

    wrapper = progress or tqdm
    for index, image in wrapper(generator, total=len_links):
        images.append((index, image))

    pool.close()
    return sorted(images)


def convert_to_pdf(name: str, images: list, directory='.'):
    """Convert a list of images in pdf"""
    try:
        from reportlab.lib.utils import ImageReader
        from reportlab.pdfgen.canvas import Canvas
    except ImportError:
        raise ImportError('Reportlab is required for convert to pdf')

    filename = os.path.join(directory, name)

    canva = Canvas(filename)
    for _, image in images:
        image_bytes = io.BytesIO(image)
        buffer = ImageReader(image_bytes)

        canva.setPageSize(buffer.getSize())
        canva.drawImage(buffer, 0, 0)
        canva.showPage()

    canva.save()


def convert_to_images(name: str, folder: str, images: list, directory='.'):
    """Convert to a folder of images"""
    folder = os.path.join(directory, folder)

    for idx, image in images:
        filename = os.path.join(folder, name.format(idx))
        with open(filename, 'wb') as file:
            file.write(image)
