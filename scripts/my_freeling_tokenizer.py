from freeling import freeling

freeling.util_init_locale("default")

class MyFreelingLemmatizer():
    def __init__(self, LANG, FREELINGDIR = "/usr/local"):
        self.LANG = LANG
        self.FREELINGDIR = FREELINGDIR
        self.DATA = FREELINGDIR+"/share/freeling/";
        DATA = self.DATA
        self.la=freeling.lang_ident(DATA+"common/lang_ident/ident.dat")

        self.op= freeling.maco_options(LANG)
        self.op.set_data_files( "", 
                       DATA + "common/punct.dat",
                       DATA + LANG + "/dicc.src",
                       DATA + LANG + "/afixos.dat",
                       "",
                       DATA + LANG + "/locucions.dat", 
                       DATA + LANG + "/np.dat",
                       DATA + LANG + "/quantities.dat",
                       DATA + LANG + "/probabilitats.dat")

        self.tk=freeling.tokenizer(DATA+LANG+"/tokenizer.dat")
        self.sp=freeling.splitter(DATA+LANG+"/splitter.dat")
        self.sid=self.sp.open_session()
        self.mf=freeling.maco(self.op)

        self.mf.set_active_options(False, True, True, True,
                              True, True, False, True,
                              True, True, True, True )

    def lemmatize(self, line, flush = True):
        """
        :param flush: boolean. Si es Falso, entonces guarda
        en el buffer de Freeling la entrada que vaya reci-
        biendo hasta encontrar un signo de terminación de
        enunciado. 
        """
        l = self.tk.tokenize(line)
        ls = self.sp.split(self.sid, l, flush)
        ls = self.mf.analyze(ls)
        
        # orig = ""
        lemmas = ""

        for s in ls :
           ws = s.get_words();

           for w in ws :
              # orig += w.get_form() + " "
              lemmas += w.get_lemma() + " "

        return lemmas

    def close_session(self):
        self.sp.close_session(self.sid)
    

    
