import re, os
from dir_tools import get_immediate_subdirectories, get_immediate_files
from my_freeling_tokenizer import MyFreelingLemmatizer

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


def clean_file(inpath, outpath, lemmatizer, stopwords):
    directory = os.path.dirname(outpath)
    if directory and not os.path.isdir(directory):
        os.makedirs(directory)

    r = re.compile("[^\W\d]+") # para capturar solo palabras compuestas por letras (respeta acentos pero no apóstrofes, e ignora signos de puntuación y números)
    with open(inpath, "r") as inputf, open(outpath, "w") as outputf:
        for line in inputf:
            line = lemmatizer.lemmatize(line)
            line = line.strip().lower().replace("\t", " ").replace("_", " ")
            words = r.findall(line)
            words = filter_stopwords(words, stopwords)

            if words:
                outputf.write(" ".join(words) + " ")

def clean_files(inpath, outpath, lang, stw_path):
    freeling_langs = {"spa":"es", "fre": "fr", "eng":"en"}
    lemmatizer = MyFreelingLemmatizer(freeling_langs[lang])
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

    lemmatizer.close_session()


print("Español")
stw_spa_path = "wordlists/stopwords_spanish.txt"
clean_files("original_dataset/", "../clean_dataset/", "spa", stw_spa_path)

print("Inglés")
stw_spa_path = "wordlists/stopwords_english.txt"
clean_files("original_dataset/", "../clean_dataset/", "eng", stw_spa_path)

print("Francés")
stw_spa_path = "wordlists/stopwords_french.txt"
clean_files("original_dataset/", "../clean_dataset/", "fre", stw_spa_path)
