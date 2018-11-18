import os, codecs
from pythonopensubtitles.opensubtitles import OpenSubtitles

def descargar_sub(movieid, path, ost = None):
    if ost is None:
        ost = OpenSubtitles()
        token = ost.login('doctest', 'doctest')

    langs = ['eng', 'spa', 'fre']

    directory = os.path.join(path, movieid)
    if not os.path.isdir(directory):
        os.makedirs(directory)

    for lang in langs:
        found = ost.search_subtitles([{'sublanguageid': lang, 'imdbid': movieid}])

        if found and len(found) > 0:
            subid = found[0].get('IDSubtitleFile')
            sub = ost.download_subtitles([ subid ], output_directory=directory, extension= lang + '.srt')

def descargar_subs_de_lista(listfile, outputpath, min_line = 0, max_line = 10):
    ost = OpenSubtitles()
    token = ost.login('doctest', 'doctest')

    with codecs.open(listfile, "r") as lf:
        for i, line in enumerate(lf):
            if i < min_line: continue
            if i >= max_line: break

            movieid = line.split(" ")[0]
            print("Descargando #{0} - {1}".format(i, movieid))
            descargar_sub(movieid, outputpath, ost = ost)

descargar_subs_de_lista('imdbids_horror.txt', "./dataset/2/", min_line = 20, max_line = 50)

############ PLAN DE DESCARGA ###############
# Sigue horror del 35 al 50
# Luego todos del 50 al 100
# Luego todos del 100 al 300 si me da tiempo... quizas considerar hacerlo solo para ingles en este punto y ya asi solo hacer clasificador de ingles
