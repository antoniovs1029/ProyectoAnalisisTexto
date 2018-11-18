import re, requests, codecs
from bs4 import BeautifulSoup
import imdb
from pythonopensubtitles.opensubtitles import OpenSubtitles

def printmovielist(query, outfile, num = 300, check_if_subtitles = True):
    results = 0
    start_index = 1
    
    imdb_api = imdb.IMDb()

    if check_if_subtitles:
        ost = OpenSubtitles()
        token = ost.login('doctest', 'doctest')
        print(token)
    
    with codecs.open(outfile, "w", encoding="utf-8") as out:
        while results < num:
            page = requests.get(query + "&start={0}".format(start_index))
            soup = BeautifulSoup(page.content, "html.parser")
            titles = soup.find_all('span', class_="lister-item-header")
            idregex = re.compile("tt([0-9]*)")

            print("Revisando resultados del {0} al {1}:", start_index, start_index + 49)
            for title in titles:
                movielink = title.find('a')
                movieid = idregex.search(movielink['href']).group(1)
                movietitle = title.text.replace("\n", " ").strip()

                # Se ignoran los resultados que no sean peliculas:
                movie = imdb_api.get_movie(movieid)
                if movie is None or movie['kind'] != 'movie':
                    continue

                usable = True

                # Se ignoran los resultados para los que no haya subtitulos en los lenguajes de nuestro interes:
                if check_if_subtitles:
                    languages = ['eng', 'spa', 'fre']

                    for lang in languages:
                        found = ost.search_subtitles([{'sublanguageid': lang, 'imdbid': movieid}])
                        if not found or len(found) < 1:
                            usable = False
                
                if usable:
                    print(movieid, movietitle)
                    out.write("{0} {1}\n".format(movieid, movietitle))
                    results += 1

                    if results == num:
                        return

            start_index += 50

#query_romance_comedia = "https://www.imdb.com/search/title?genres=comedy,romance&sort=num_votes,desc&explore=title_type,genres&view=simple"
#printmovielist(query_romance_comedia, "imdbids_romance-comedia.txt", check_if_subtitles = False)

#query_accion = "https://www.imdb.com/search/title?genres=action&sort=num_votes,desc&explore=title_type,genres&view=simple"
#printmovielist(query_accion, "imdbids_accion.txt", check_if_subtitles = False)

query_horror = "https://www.imdb.com/search/title?genres=horror&view=simple&sort=num_votes,desc&explore=title_type,genres"
printmovielist(query_horror, "imdbids_horror.txt", check_if_subtitles = False)
