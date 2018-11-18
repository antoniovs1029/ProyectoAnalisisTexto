import re, os
from dir_tools import get_immediate_subdirectories, get_immediate_files

def load_stopwords(path):
    stopwords = []
    with open(path, "r") as stwf:
        for line in stwf:
            stopwords.append(line.rstrip())
    return stopwords

def filter_stopwords(wordlist, stopwords):
    filtered = []
    for word in wordlist:
        if word not in stopwords and len(word) > 1:
            filtered.append(word)

    return filtered

def load_lemmadict(path):
    lemmadict = dict()
    with open(path, "r") as inputf:
        for line in inputf:
            line = line.split("\t")
            lemmadict[line[1]] = line[0]

    return lemmadict

class MyLemmatizer():
    def __init__(self, path):
        self.lemmadict = load_lemmadict(path)

    def lemmatize_word(self, word):
        return self.lemmadict.get(word, word)

    def lemmatize(self, wordlist):
        lemlist = []
        for word in wordlist:
            lemlist.append(self.lemmatize_word(word))
        return lemlist

def clean_file(inpath, outpath, lemmatizer, stopwords):
    directory = os.path.dirname(outpath)
    if not os.path.isdir(directory):
        os.makedirs(directory)

    r = re.compile("[^\W\d]+") # para capturar solo palabras compuestas por letras (respeta acentos pero no apóstrofes, e ignora signos de puntuación y números)
    with open(inpath, "r") as inputf, open(outpath, "w") as outputf:
        for line in inputf:
            line = line.strip().lower().replace("\t", " ")
            words = r.findall(line)
            words = filter_stopwords(words, stopwords)
            lemmas = lemmatizer.lemmatize(words)

            if lemmas:
                outputf.write(" ".join(lemmas) + " ")

def clean_files(inpath, outpath, lang, lemm_path, stw_path):
    lemmatizer = MyLemmatizer(lemm_path)
    stopwords = load_stopwords(stw_path)

    for label in ["0/", "1/", "2/"]:
        directory = os.path.join(inpath, label)
        for movieid in get_immediate_subdirectories(directory):
            subdir = os.path.join(directory, movieid + "/")
            for subtitlefile in get_immediate_files(subdir):
                if subtitlefile.endswith('.' + lang + '.srt'):
                    inputfile = os.path.join(inpath, label, movieid, subtitlefile)
                    outputfile = os.path.join(outpath, label, movieid + "." + lang + ".txt")
                    print(inputfile)
                    if not os.path.isfile(outputfile):
                        clean_file(inputfile, outputfile, lemmatizer, stopwords)

print("Español")
stw_spa_path = "wordlists/stopwords_spanish.txt"
lemm_spa_path = "wordlists/lemmatization-es.txt"
clean_files("dataset20/", "clean_dataset/", "spa", lemm_spa_path, stw_spa_path)

print("Inglés")
stw_spa_path = "wordlists/stopwords_english.txt"
lemm_spa_path = "wordlists/lemmatization-en.txt"
clean_files("dataset20/", "clean_dataset/", "eng", lemm_spa_path, stw_spa_path)

print("Francés")
stw_spa_path = "wordlists/stopwords_french.txt"
lemm_spa_path = "wordlists/lemmatization-fr.txt"
clean_files("dataset20/", "clean_dataset/", "fre", lemm_spa_path, stw_spa_path)
