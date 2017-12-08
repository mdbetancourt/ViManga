"""Api core"""

import ast
import json
from operator import itemgetter
from types import GeneratorType


import requests
from requests import Response

from vimanga.api.constants import (
    HEADERS, API_URL, MANGA_URL, CAPS_URL, IMAGES_SERVER
)
from vimanga.api.types import (
    Mangas, Manga, Chapter, Chapters, Scan
)


def call_api(url: str = API_URL, **params) -> Response:
    """Call api and set default header"""
    return requests.get(url,
                        params=params,
                        headers=HEADERS)


def get_mangas(categorias=None,
               defecto=1,
               generos=None,
               per_page=10,
               page=1,
               puntuacion=0,
               search_by='nombre',
               sort_dir='asc',
               sorted_by='nombre',
               **params) -> Mangas:
    """Get all filters mangas"""
    while True:
        _params = {
            'categorias': categorias or [],
            'defecto': defecto,
            'generos': generos or [],
            'itemsPerPage': per_page,
            'page': page,
            'puntuacion': puntuacion,
            'searchBy': search_by,
            'sortDir': sort_dir,
            'sortedBy': sorted_by,
            **params
        }
        response = call_api(API_URL, **_params)
        try:
            response = response.json()
        except json.JSONDecodeError:
            raise Exception(response.text)
        values = {
            'total': response['total'],
            'per_page': response['per_page'],
            'current_page': response['current_page'],
            'page_count': response['last_page'],
            'data': []
        }

        for manga in response['data']:
            values['data'].append(Manga(
                id=manga['id'],
                type=manga['tipo'],
                score=manga['puntuacion'],
                name=manga['nombre'],
                synopsis=manga['info']['sinopsis'],
                genders=list(map(itemgetter('genero'), manga['generos']))
            ))

        mangas = Mangas(**values)
        if mangas.current_page < mangas.page_count:
            page += 1
            yield mangas
        else:
            yield mangas
            return


def get_chapters(manga: Manga, page: int = 1) -> Chapters:
    """Get all chapters from a manga"""
    while True:
        response = call_api(MANGA_URL.format(manga.id), page=page).json()

        values = {
            'total': response['total'],
            'per_page': response['per_page'],
            'current_page': response['current_page'],
            'page_count': response['last_page'],
            'data': []
        }

        for chapter in response['data']:
            uploads = []
            for upload in chapter['subidas']:
                uploads.append(Scan(
                    id=upload['idScan'],
                    name=upload['scanlation']['nombre']
                ))

            values['data'].append(Chapter(
                id=chapter['id'],
                name=chapter['nombre'],
                manga_id=chapter['tomo']['idManga'],
                number=chapter['numCapitulo'],
                uploads=uploads
            ))

        chapters = Chapters(**values)

        if chapters.current_page < chapters.page_count:
            yield chapters
        else:
            yield chapters
            return


def get_images(chapter: Chapter, scan=0) -> GeneratorType:
    """Get a provide chapter"""
    scanlation: Scan = chapter.uploads[scan]
    _params = {
        'idManga': chapter.manga_id,
        'idScanlation': scanlation.id,
        'numeroCapitulo': chapter.number
    }

    response = call_api(CAPS_URL, **_params).json()
    images = response['imagenes']
    images = ast.literal_eval(images)
    params = {
        'manga': chapter.manga_id,
        'scan': scanlation.id,
        'chapter': chapter.number,
    }

    for image in images:
        yield IMAGES_SERVER.format(image=image, **params)
