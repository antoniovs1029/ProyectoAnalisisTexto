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
                

frecs_spa = obtener_frecuencias("../clean_dataset2/", "spa")
frecs_eng = obtener_frecuencias("../clean_dataset2/", "eng")
frecs_fre = obtener_frecuencias("../clean_dataset2/", "fre")

def comparar(spa, eng, fre):
    generos = ["accion", "romance", "horror"]
    for i in range(3):
        s = frecs_spa[i][spa]
        e = frecs_eng[i][eng]
        f = frecs_fre[i][fre]

        print("Genero: {0}, Spa: {1}, Eng: {2}, Fre:{3}".format(generos[i], s, e, f))
