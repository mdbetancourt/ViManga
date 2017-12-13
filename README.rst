=======
vimanga
=======


.. image:: https://img.shields.io/pypi/v/vimanga.svg
     :target: https://pypi.python.org/pypi/vimanga
     :alt: Pypi

.. image:: https://img.shields.io/travis/Akhail/ViManga.svg
     :target: https://travis-ci.org/Akhail/ViManga
     :alt: Travias

.. image:: https://img.shields.io/github/release/akhail/vimanga.svg
     :target: https://github.com/Akhail/ViManga/releases
     :alt: Releases

.. image:: https://pyup.io/repos/github/Akhail/ViManga/shield.svg
     :target: https://pyup.io/repos/github/Akhail/ViManga/
     :alt: Updates

.. image:: https://img.shields.io/github/license/akhail/vimanga.svg
     :target: https://github.com/Akhail/ViManga/blob/master/LICENSE
     :alt: License

.. image:: https://img.shields.io/pypi/pyversions/vimanga.svg
     :target: https://pypi.python.org/pypi/vimanga
     :alt: Versions

Aplicación que permite las descarga de manga en formato pdf y imagenes


* Free software: MIT license

Uso
====================

El metodo mas sencillo para usarlo es `vimanga find 'Black Haze'` de esta forma se puede buscar todos los mangas y listarlos.

Selección de capitulos
--------------------

Para seleccionar un capitulo se utiliza el siguiente parametro siguiendo con el ejemplo de arriba `vimanga find 'Black Haze' --chapters=1,` permite seleccionar un capitulo. Para seleccionar varios se puede pasar una lista de capitulos `vimanga find 'Black Haze' --chapters=1,5,10`.

Tambien permite la seleccion por rango para eso esta la palabra 'to' `vimanga find 'Black Haze' --chapters=1to100` que permite descargar todos los capitulos desde el 1 hasta el 100.

Descargar
--------------------

Para descargar se utiliza el comando --download `vimanga find 'Black Haze' --chapters=1to100 --download` esto descarga el primer manga que coincida con el texto de busqueda en el rango de capitulos 1 hasta el 100.

Conversiones
--------------------

ViManga soporta conversion de manga a pdf para eso se le debe pasar el parametro --convert-to con el valor pdf `vimanga find 'Black Haze' --chapters=1to100 --convert-to=pdf --download` 

Cambiar carpeta de descarga
--------------------

Para eso se usa el parametro --directory el valor por defecto es /home/{user}/mangas

Filtros
=====================

Para conseguir el manga se pueden usar los siguientes filtros que son utilizados de forma '--{nombre-filtro}'

Posibles filtros
---------------------

* page: Pagina actual.
* sort_dir: Direccion al ordenar `asc o desc`.
* score: Minima puntuacion del manga.
* search_by: Que se debe usar en la busqueda puede ser autor, titulo, artista.
* per_page: Numero de mangas a mostrar por Pagina.
* sorted_by: Que valor se debe usar para ordenar por defecto nombre.

Ejemplos de Uso
=====================

Se pueden usar comandos de la consola por ejemplo para ver 100 mangas con calificacion superior a 8
`vimanga find '' --puntuacion=8 --per-page=100 | less` o para contar cuantos mangas contienen 'sama' `vimanga find 'sama' --per-page=1000 | wc -l`