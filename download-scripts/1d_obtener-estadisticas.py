import os
from collections import Counter
from dir_tools import get_immediate_files

def contar_palabras_archivo(path, contador):
    with open(path, "r") as inputf:
        for line in inputf:
            for word in line.split(" "):
                contador[word] += 1

def obtener_frecuencias(path, lang):
    contadores = []
    for label in ["0/", "1/", "2/"]:
        contador = Counter()
        directory = os.path.join(path, label)
        for subtitlefile in get_immediate_files(directory):
            if subtitlefile.endswith(lang + "." + "txt"):
                subpath = os.path.join(directory, subtitlefile)
                contar_palabras_archivo(subpath, contador)

        contadores.append(contador)

    return contadores                
                

frecs_spa = obtener_frecuencias("../clean_dataset/", "spa")
frecs_eng = obtener_frecuencias("../clean_dataset/", "eng")
frecs_fre = obtener_frecuencias("../clean_dataset/", "fre")

def comparar(spa, eng, fre):
    generos = ["accion", "romance", "horror"]
    for i in range(3):
        s = frecs_spa[i][spa]
        e = frecs_eng[i][eng]
        f = frecs_fre[i][fre]

        print("Genero: {0}, Spa: {1}, Eng: {2}, Fre:{3}".format(generos[i], s, e, f))

def intersect_most_common(frecs, n = 100):
    sets = []
    for i in range(3):
        s = set()
        for k, v in frecs[i].most_common(n):
            s.add(k)
        sets.append(s)

    s = sets[0] & sets[1] & sets[2]
    res = []
    for elem in s:
        v = frecs[0][elem] + frecs[1][elem] + frecs[2][elem]
        res.append((elem, v))

    return sorted(res, key = lambda tup: tup[1], reverse = True)

def disjoin_frecs(frecs, min_frec = 0):
    sets = []
    for i in range(3):
        s = set()
        for k in list(frecs[i].keys()):
            if frecs[i][k] > min_frec:
                s.add(k)
        sets.append(s)

    s = (sets[0] | sets[1] | sets[2]) - ((sets[0] & sets[1]) | (sets[0] & sets[2]) | (sets[1] & sets[2]))
    res = []
    for elem in s:
        v = frecs[0][elem] + frecs[1][elem] + frecs[2][elem]
        res.append((elem, v))

    return sorted(res, key = lambda tup: tup[1], reverse = True)

