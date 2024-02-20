import re
import fitz
import os
import sys
from langdetect import detect

class Parser :
    def __init__(self) :
        pass

    """
    fonction de reconnaissance des adresses mails
    retourne un tuple avec liste contenant le prefixe de chaque adresse
    --> et une liste contenant les types
    """
    def recognize_adress(self,path) :
        adr1 = r'([\w+.+ +-]+)@' #format adresse mail classique
        adr2 = r'{?(\w+)(,\ \w+)*}?@' #format de regroupement
        pattern1 = re.compile(adr1)
        pattern2 = re.compile(adr2)
        result = [None,None]
        with fitz.open(path) as res :
            matches1 = pattern1.findall(res.load_page(0).get_text())
            matches2 = pattern2.findall(res.load_page(0).get_text())
            if matches1 :
                result[0] = matches1
            if matches2 :
                result[1] = matches2[0]
        return result

    """
    fonction permettant de former des noms
    input : une liste de prefixe d'adresse
    output : une liste de nom 
    """
    def make_name(self,t) :
        result = []
        sep = ' ' #separateur lors de la fusion des 2 parties du prefixe
        #verifie si il contient des adr1
        if t[0] :
            #on parcours chaque mot
            for i in range(len(t[0])) :
                result.append(sep.join(t[0][i].split(".")))
        #on passe aux adre2
        if t[1] :
            for val in t[1] :
                for jul in val.split(",") :
                    result.append(jul.strip()) #enleve les espaces inutiles
        return result


    """
    fonction qui permet de former des abreviations
    input : liste de string sous forme de nom + prenom 
    output : liste de tuple contenant nom + abr sous forme de string
    """
    def make_abr(self,li) :
        result = []
        for val in li :
            abr = ""
            for jul in val.split():
                abr += (jul[0])
            result.append((val,abr))
        return result

    """
    reconnait des chaines qui ont la forme d'un nom
    input : chemin du fichier
    output : liste des supposés noms
    """
    def recognize_name(self,chaine) :
        result = []
        reg = r'[A-Z]*\w*-*[A-Z]\w+ [A-Z]*.*[A-Z]* [A-Z]*\w*-*[A-Z]\w+' #forme des noms
        pattern = re.compile(reg)
        matches = pattern.findall(chaine)
        if matches :
            result = matches
        return result

    """
    reconnait des chaines qui ont la forme d'un nom
    input : chemin du fichier
    output : liste des supposés noms
    """
    def getAuthor(self,path) :
        auteurs = self.make_name(self.recognize_adress(path))
        if auteurs != [] :
            print("1")
            return auteurs
        else :
            with fitz.open(path) as pdf :
                meta = pdf.metadata
                auteurs2 = meta['author']
            if auteurs2 != "" :
                print("2")
                return auteurs2
            else :
                print("3")
                return self.recognize_name(self.getAuthorZone(path))

    """
    fonction qui retourne les auteurs
    input : le path
    output : liste d'auteurs
    """
    def recognize_author(self,path) :
        author = []
        potentiel = self.recognize_name(path)
        adr = self.make_abr(self.make_name(self.recognize_adress(path)))
        for val in potentiel :
            for jul in adr[0][0].split() :
                regex = rf'{jul}'
                pat = re.compile(regex)
                matches = pat.match(val.lower())
                if matches :
                    author.append(val)
        return author

    """
    fonction qui retourne la zone du texte pour la recherche des auteurs
    input : path
    output : block
    """
    def getAuthorZone(self,path) :
        i = 0
        top = self.get_size(path)[1] #je prends le block du titre
        bottom = self.find_abstract(path)[1] 
        bottompattern = re.compile(rf'{self.find_abstract(path)[0]}')
        result = ""
        boolean = False
        with fitz.open(path) as pdf :
            blocks = pdf.load_page(0).get_text('blocks')
            for block in blocks :
                if boolean == False :
                    matches = bottompattern.findall(block[4])
                    if matches :
                        boolean = True
                    else :
                        if i > top and i < bottom :
                            result += block[4]
                i += 1
        return result

    """
    fonction qui donne un format a une zone de recherche
    input : texte
    output : zone formatée
    """
    def to_formate(self,zone) :
        zone = zone.split("\n")
        return ''.join(zone)
            
    """
    fonction qui retourne la position du block d'intro et d'abstract
    input : chemin du fichier
    output : i le nombre de tour pour atteindre le block de l'intro et d'abstract dans une liste
    """
    def find_abs_intro_block(self,path) : 
        pat1 = re.compile(r'abstract')
        pat2 = re.compile(r'ntroduction') #longue histoire
        intro = 0            #pos de intro
        abs = 0              #pos de abs
        b1 = False              #signe si on trouve abstract
        b2 = False              #signe si on trouve intro
        result = [abs,intro]
        with fitz.open(path) as pdf : #je recupere les differents blocks du pdf
            blocks = pdf.load_page(0).get_text('dict')['blocks']
            for block in blocks : #je parcours chaque block
                if self.skipable(block) :
                    for line in block['lines'] : #je parcours chaque ligne de chaque block
                        for span in line['spans'] : #parcours de ligne et recuperation du texte
                            matches1 = pat1.findall(span['text'].lower())
                            matches2 = pat2.findall(span['text'].lower())
                            if matches1 :
                                if b1 == False :
                                    result[0] = abs
                                    b1 = True
                            if matches2 :
                                if b2 == False :
                                    result[1] = intro
                                    b2 = True
                intro += 1
                abs += 1
        return result

    """
    fonction qui retourne l'abstract
    input : path
    output : abstract et sa pos dans une liste
    """
    def find_abstract(self,path) :
        result = ""
        pos = 0
        abs = self.find_abs_intro_block(path)[0]
        intro = self.find_abs_intro_block(path)[1]
        if abs != 0 : #and abs < intro : #donc si l'abstract est delimimité par le mot abstract
            if re.compile(r'Abstract').findall(self.biggestBlock(path,abs,intro)[0]) == [] :
                #si l'abstract se trouve dans 2 blocks differents
                result = self.smallestBlock(path,abs,intro)[0] + self.biggestBlock(path,abs,intro)[0] 
                pos = self.biggestBlock(path,abs,intro)[1]-1
            else :
                result = self.biggestBlock(path,abs,intro)[0]
                pos = self.biggestBlock(path,abs,intro)[1]
        else :
            result = self.biggestBlock(path,intro-2,intro)[0]
            pos = self.biggestBlock(path,intro-2,intro)[1]
        return [result.strip(),pos] #.encode('utf-8') #enleve les espaces inutiles

    """
    fonction qui retourne le block de texte le plus grand
    input : path , i start , j limite
    output : le block en texte et le numero dudit block dans une liste
    """
    def biggestBlock(self,path,i,j) :
        result = ""
        tmp = 0
        data = 0
        with fitz.open(path) as pdf :
            blocks = pdf.load_page(0).get_text('blocks')
            for block in blocks :
                if tmp >= i-1 and tmp < j :
                    if len(result) < len(block[4]) :
                        data = tmp #stocke le numero du block de l'abstract
                        result = block[4]
                tmp += 1
        return [result,data]


    """
    fonction qui retourne le block de texte le plus petit
    input : path , i start , j limite
    output : le block en texte et le numero dudit block dans une liste
    """
    def smallestBlock(self,path,i,j) :
        result = ""
        tmp = 0
        data = 0
        with fitz.open(path) as pdf :
            blocks = pdf.load_page(0).get_text('blocks')
            for block in blocks :
                if tmp < self.biggestBlock(path,i,j)[1] :
                    data = tmp #stocke le numero du block de l'abstract
                    result = block[4]
                tmp += 1
        return [result,data]

    """
    fonction qui trouve le titre
    input : path
    output : titre
    """
    def find_title(self,path) :
        with fitz.open(path) as pdf :
            target = self.get_size(path)[0] #la taille max
            result = ""
            blocks = pdf.load_page(0).get_text('dict')['blocks']
            for block in blocks :
                if self.skipable(block) :
                    for line in block['lines'] :
                        for span in line['spans'] :
                            if span['size'] == target :
                                result += " " + str(span['text'])#.encode('utf-8'))
        return result.strip() #enleve les espaces inutiles

    """
    fonction qui skip un block
    input : block
    output : boolean
    """
    def skipable(self,block) :
        #verifie si c'est du texte
        if block['type'] == 0 :
            return True
        return False

    """
    fonction qui retourne la taille max de la police du texte
    input : path
    output : int size , numero pos du block dans une liste
    """
    def get_size(self,path) :
        with fitz.open(path) as pdf :
            result = 0
            pos = None
            i = 0
            blocks = pdf.load_page(0).get_text('dict')['blocks']
            for block in blocks :
                if self.skipable(block) == True : #skip si c'est pas du texte
                    for line in block['lines'] :
                        for span in line['spans'] :
                            size = span['size']
                            #si ce n'est pas un mot je le skip
                            if size > result and (is_in_language(span['text'],'en')) == True :
                                result = size
                                pos = i
                i += 1
        return [result,pos]

"""
fonction pour donner les titres d'un corpus
input : path du dossier
output : les titres
"""
def summarize(parser,src,dst) :
    if not os.path.exists(dst):
        os.makedirs(dst)
    for fichier in os.listdir(src) :
        sfile = os.path.join(src,fichier)
        #Obtient le nom du fichier sans l'extension
        base_name = os.path.splitext(fichier)[0]
        dfile = os.path.join(dst, base_name)
        with open(dfile,'w') as d :
            d.write("Nom fichier source : ")
            d.write(base_name+".pdf")
            d.write("\n_____________________________\n")
            d.write("Titres : ")
            d.write(parser.find_title(sfile))
            d.write("\n_____________________________\n")
            d.write("Auteurs : ")
            d.write(str(parser.getAuthor(sfile)))
            d.write("\n_____________________________\n")
            d.write("Abstract : ")
            d.write(str(parser.find_abstract(sfile)[0].strip()))
        


"""
fonction qui dit si une chaine appartient bien à une langue
#source : microsoft copilot
input : text , prefixe dans la langue
output : boolean
"""
def is_in_language(text, language):
    try:
        detected_language = detect(text)
        return detected_language == language
    except:
        return False


def main(path1,path2) :
    parser = Parser()
    """
    path1  = "/mnt/c/Users/KAHASHA/Documents/ubs/licence3/s2/parser/corpus/pdf/"
    path2 = "/mnt/c/Users/KAHASHA/Documents/ubs/licence3/s2/parser/parserV1/resultats/"
    """
    summarize(parser,path1,path2)

if __name__ == "__main__" :
    if len(sys.argv) == 3 :
        main(sys.argv[1],sys.argv[2])