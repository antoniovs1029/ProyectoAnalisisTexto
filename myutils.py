import random
import matplotlib.pyplot as plt
from itertools import zip_longest

#########################################################
################### Manipulación de Frecuencias
#########################################################

def intersect_most_common(frecs, n = 100):
    sets = []
    for i in range(3):
        s = set()
        for k, v in frecs[i].most_common(n):
            s.add(k)
        sets.append(s)

    return sets[0] & sets[1] & sets[2]

def disjoin_frecs(frecs, min_frec = 0):
    sets = []
    for i in range(3):
        s = set()
        for k in list(frecs[i].keys()):
            if frecs[i][k] > min_frec:
                s.add(k)
        sets.append(s)

    s = (sets[0] | sets[1] | sets[2]) - ((sets[0] & sets[1]) | (sets[0] & sets[2]) | (sets[1] & sets[2]))

    return s

def set2wordfrecs(s, frecs):
    res = []
    for elem in s:
        v = 0
        for frec in frecs:
            v += frec[elem]
        res.append((elem, v))

    return sorted(res, key = lambda tup: tup[1], reverse = True)

#########################################################
################### Manipulación de Corpus
#########################################################

def split_list(l, chunk_size, overlap_size = 0):
    """
    chunk_size debe ser mayor a 0

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
    if stopwords is None:
        return l

    res = []
    for word in l:
        if word not in stopwords:
            res.append(word)
    return res

def texts2lists(txts, stopwords):
    lists = []
    for txt in txts:
        txt = txt.strip().split(" ")
        txt = filter_stopwords(txt, stopwords)
        lists.append(txt)
    return lists

def split_lists(lists, chunk_size, overlap_size = 0):
    splitted = []
    for l in lists:
        l = split_list(l, chunk_size, overlap_size)
        splitted += l
    return splitted

def lists2bow(docs, dictionary):
    return [dictionary.doc2bow(doc) for doc in docs]

def split_training_txts(txts, training_ratio = .7):
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
    return [v for v in sum(zip_longest(*lists), ()) if v is not None]
    

def merge_multilingual(lists_esp, lists_eng, lists_fre):
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
