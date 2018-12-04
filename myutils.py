"""
Funciones auxiliares varias para apoyarme en el
desarrollo del proyecto.
"""

import random
import matplotlib.pyplot as plt
from itertools import zip_longest

#########################################################
################### Manipulación de Frecuencias
#########################################################

def intersect_most_common(frecs, n = 100):
    """
    :param frecs: lista de 3 objetos Counter()
    :param n: entero
    :return set intersección de las palabras más comunes de los 3 contadores
    """
    sets = []
    for i in range(3):
        s = set()
        for k, v in frecs[i].most_common(n):
            s.add(k)
        sets.append(s)

    return sets[0] & sets[1] & sets[2]

def disjoin_frecs(frecs, min_frec = 0):
    """
    :param frecs: lista de 3 objetos Counter()
    :param min_frec: entero
    :return lista de sets de las palabras más frecuentes, que tienen mayor frecuencia a min_frec y que solo son frecuentes en uno de los géneros de películas
    """
    sets = []
    for i in range(3):
        s = set()
        for k in list(frecs[i].keys()):
            if frecs[i][k] > min_frec:
                s.add(k)
        sets.append(s)

    s = (sets[0] | sets[1] | sets[2]) - ((sets[0] & sets[1]) | (sets[0] & sets[2]) | (sets[1] & sets[2]))

    return [s & sets[0], s & sets[1], s & sets[2]]

def set2wordfrecs(s, frecs):
    """
    :param s: conjunto de palabras
    :param frecs: lista de objetos Counter
    :returns una lista de los elementos de s, ordenada y acompañada por sus frecuencias conjuntas en los contadores de frecs
    """
    res = []
    for elem in s:
        v = 0
        for frec in frecs:
            v += frec[elem]
        res.append((elem, v))

    return sorted(res, key = lambda tup: tup[1], reverse = True)

def comparar_generos(spa, eng, fre, frecs_spa, frecs_eng, frecs_fre):
    """
    :param spa: palabra en español
    :param eng: palabra en inglés
    :param fre: palabra en francés

    :param frecs_spa: Counter de palabras en español
    :param frecs_eng: en inglés
    :param frecs_fre: en francés

    Imprime de manera organizada las frecuencias de las palabras
    indicadas en cada lengua y género.

    :returns: Nada
    """
    generos = ["accion", "romance", "horror"]
    for i in range(3):
        s = frecs_spa[i][spa]
        e = frecs_eng[i][eng]
        f = frecs_fre[i][fre]

        print("Genero: {0}, Spa: {1}, Eng: {2}, Fre:{3}".format(generos[i], s, e, f))

#########################################################
################### Manipulación de Corpus
#########################################################

def split_list(l, chunk_size, overlap_size = 0):
    """
    :param l: lista a segmentar
    :param chunk_size: tamaño máximo de los segmentos
    :param overlap_size: overlape entre los segmentos

    :returns lista de listas segmentadas

    Ojo: chunk_size debe ser mayor a 0 y overlap_size
    debe ser menor a chunk_size
    """
    splitted = []
    imin = 0
    imax = min(chunk_size, len(l))

    while imin < len(l):
        splitted.append(l[imin:imax])
        imin += chunk_size - overlap_size
        imax = min(imin + chunk_size, len(l))

    return splitted

def filter_stopwords(l, stopwords):
    """
    :param l: lista de palabras
    :param stopwords: lista de palabras de paro

    :returns lista de palabras que no incluyan a las
    palabras de paro
    """
    if stopwords is None:
        return l

    res = []
    for word in l:
        if word not in stopwords:
            res.append(word)
    return res

def texts2lists(txts, stopwords):
    """
    :param txts: lista de strings
    :param stopwords: lista de palabras de paro
    
    :returns lista de listas de palabras, que no
    incluyan a las palabras de paro
    """
    lists = []
    for txt in txts:
        txt = txt.strip().split(" ")
        txt = filter_stopwords(txt, stopwords)
        lists.append(txt)
    return lists

def split_lists(lists, chunk_size, overlap_size = 0):
    """
    :param lists: lista de listas a segmentar
    :param chunk_size: ver "split_list()"
    :param overlap_size: ver "split_list()"

    :returns lista de listas segmentadas
    """
    splitted = []
    for l in lists:
        l = split_list(l, chunk_size, overlap_size)
        splitted += l
    return splitted

def lists2bow(docs, dictionary):
    """
    :param docs: lista de listas de palabras
    :param dictionary: Dictionary de Gensim que asocia
    un ID a cada palabra.

    :returns lista de vectores dispersos
    """
    return [dictionary.doc2bow(doc) for doc in docs]

def split_training_txts(txts, training_ratio = .7):
    """
    :param txts: lista de strings
    :training_ratio: porcentaje (del 0 al 1) de qué tan grande
    debería ser el training set con respecto al test set

    :returns training set y testing set separados y sus
    respectivas etiquetas
    """
    training_txts = []
    test_txts = []

    training_labels = []
    test_labels = []
    for genero, genero_txts in enumerate(txts):
        training_size = int(len(genero_txts)*training_ratio)
        training_ids = random.sample(range(len(genero_txts)), training_size)
        
        for i in range(len(genero_txts)):
            if i in training_ids:
                training_txts.append(genero_txts[i])
                training_labels.append(genero)
            else:
                test_txts.append(genero_txts[i])
                test_labels.append(genero)

    return training_txts, training_labels, test_txts, test_labels

def merge_lists(lists):
    """
    :param lists: tupla de listas
    :returns una lista que combine el contenido de las listas
    lists, intercalando un elemento de cada lista en cada paso
    """
    return [v for v in sum(zip_longest(*lists), ()) if v is not None]
    

def merge_multilingual(lists_esp, lists_eng, lists_fre):
    """
    Dadas las listas de textos en las 3 lenguas
    regresa una lista con un solo texto por cada película
    donde las palabras de las 3 lenguas se intercalan uno
    a uno.
    """
    lists_multi = []
    for i in range(len(lists_esp)):
        l = merge_lists((lists_esp[i], lists_eng[i], lists_fre[i]))
        lists_multi.append(l)

    return lists_multi

#########################################################
################### Visualización de Datos
#########################################################

def plot_data(datos, etiquetas = None, titulo = None, colores = 'red'):
    """
    Plotea el conjunto de datos añadiendo las etiquetas y los colores dispuestos
    
    :param datos: arreglo bidimensional.
    :param etiquetas: lista de strings. Del mismo tamaño que Z[0]
    :param titulo: titulo del plot
    :param colores: string o lista de strings con los colores de cada punto
    """

    plt.scatter(datos[:,0],datos[:,1], marker='o', c= colores)
    if etiquetas is not None:
        for label, x, y in zip(etiquetas, datos[:,0], datos[:,1]):
            plt.annotate(label, xy=(x,y), xytext=(-1,1), textcoords='offset points', ha='center', va='bottom')

    if titulo is not None:
        plt.title(titulo)

    plt.show()

def index2color(indices, colores):
    """
    Toma una lista de indices y devuelve una lista de colores
    asociados.

    :param indices: lista de números enteros
    :param colores: lista de strings que representen colores
    """
    c = []
    for i in indices:
        c.append(colores[i])

    return c
