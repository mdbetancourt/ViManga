"""Cli process commands"""
import os
from itertools import chain
from functools import partial
from operator import attrgetter
from multiprocessing.dummy import Pool

from vimanga import api, utils


def find(search='',
         chapters=None,
         download=False,
         convert_to='images',
         **kwargs):
    """Find mangas cli interface"""

    threads = kwargs.pop('threads', 3)
    mangas = next(api.core.get_mangas(search, **kwargs))
    if not chapters:
        return '\n'.join(
            map(lambda x: '{}, {}'.format(x.name, x.score), mangas.data)
        )

    manga = mangas.data[0]
    print('Manga: {}'.format(manga.name))

    filters_chapters = _filter_chapters(api.core.get_chapters(manga), chapters)
    filters_chapters = sorted(filters_chapters, key=lambda x: float(x.number))

    if not download:
        return '\n'.join(
            map(lambda x: 'Capitulo {}'.format(x.number), filters_chapters)
        )

    pool = Pool(threads)

    directory = kwargs.pop('directory', os.path.expanduser('~'))
    manga_folder = os.path.join(directory, manga.name)

    generator = pool.imap_unordered(utils.download_chapter, filters_chapters)
    for chapter, data in generator:
        if convert_to == 'images':
            utils.convert_to_images('{}.jpg',
                                    chapter.number,
                                    manga_folder,
                                    data)
        else:
            utils.convert_to_pdf(f'Capitulo {chapter.number}.pdf',
                                 data,
                                 manga_folder)


def _contain(numbers, chapter):
    if isinstance(numbers, str):
        numbers = numbers.split(',')

    truth_table = []
    for number in numbers:
        try:
            value = [int(number)]
        except ValueError:
            _min, _max = map(int, number.split('to'))
            value = range(_min, _max + 1)

        truth_table.append(int(float(chapter.number)) in value)

    return any(truth_table)


def _filter_chapters(chapters, numbers):
    chapters = map(attrgetter('data'), chapters)
    chapters = chain.from_iterable(chapters)
    return filter(partial(_contain, numbers), chapters)
