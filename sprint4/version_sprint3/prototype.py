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
        adr1 = r'([\w+.+ +-]+)@([\w+.+-]+)' #format adresse mail classique
        adr2 = r'{(\w+)(,\ \w+)*}@([\w+.+-]+)' #format de regroupement
        pattern1 = re.compile(adr1)
        pattern2 = re.compile(adr2)
        result = [None,None]
        with fitz.open(path) as res :
            matches1 = pattern1.findall(res.load_page(0).get_text())
            matches2 = pattern2.findall(res.load_page(0).get_text())
            if matches1 :
                print(matches1)
                result[0] = matches1
            if matches2 :
                result[1] = matches2[0]
        return result
    
    """
    fonction de reconnaissance des adresses mails
    retourne un tuple avec liste contenant le prefixe de chaque adresse
    --> et une liste contenant les types
    """
    def recognize_adress__(self,chaine) :
        adr1 = r'([\w+.+ +-]+)@([\w+.+-]+)' #format adresse mail classique
        adr2 = r'[{\(](\w+)(,\ \w+)*[}\)]@([\w+.+-]+)' #format de regroupement
        adr3 = r'\(([\w.-]+(?:,[\w.-]+)*)\)@([\w.-]+\.[\w.-]+)'
        pattern1 = re.compile(adr1)
        pattern2 = re.compile(adr2)
        pattern3 = re.compile(adr3)
        result = [None,None,None]
        matches1 = pattern1.findall(chaine)
        matches2 = pattern2.findall(chaine)
        matches3 = pattern3.findall(chaine)
        if matches1 :
            result[0] = matches1
        if matches2 :
            result[1] = matches2[0]
        if matches3 :
            print(matches3)
            result[2] = matches3[0]
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
                result.append((sep.join(t[0][i][0].split(".")),t[0][i][0]+'@'+t[0][i][1]))
        #on passe aux adr2 et 3
        if t[1] or t[2] :
            if t[1] :
                for j in range(len(t[1])-1):
                    if t[1][j][0] != ',' :
                        for jul in t[1][j].split() : #.split(",") :
                            result.append(jul.strip()) #enleve les espaces inutiles
                    else :
                        for jul in t[1][j].split(',')[1:] : #.split(",") :
                            result.append(jul.strip()) #enleve les espaces inutiles
                for i in range(len(result)) :
                    result[i] = ((sep.join(result[i].split(".")),result[i]+'@'+t[1][len(t[1])-1]))
            if t[2] :
                print("RRRRRRRRRRRRRRRRRR")
                for j in range(len(t[2])-1):
                    if t[2][j][0] != ',' :
                        for jul in t[2][j].split() : #.split(",") :
                            result.append(jul.strip()) #enleve les espaces inutiles
                    else :
                        for jul in t[2][j].split(',')[1:] : #.split(",") :
                            result.append(jul.strip()) #enleve les espaces inutiles
                for i in range(len(result)) :
                    result[i] = ((sep.join(result[i].split(".")),result[i]+'@'+t[2][len(t[1])-1]))
        return result


    """
    fonction qui permet de former des abreviations
    input : tuple de string sous forme de nom + prenom + adresse
    output :  tuple contenant nom + adresse + abr sous forme de string
    """
    def make_abr(self,tu) :
        result = []
        for val in tu :
            i = 0
            for j in range(len(val)) :
                if i < 1 :
                    abr = self.make_abr_name(val[j])[1]
                    result.append((val[0],val[1],abr))
                i += 1
        return result
    
    """
    fonction qui permet de former des abreviations
    input : string
    output :  tuple avec nom et abr
    """
    def make_abr_name(self,nom) :
        abr = ""
        for jul in nom.split(" "):
            print(jul[0])
            abr += (jul[0])
            print(abr)
        return (nom,abr)

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
        auteurs = []
        with fitz.open(path) as pdf :
            meta = pdf.metadata
            if meta['author'] :
                auteursliste = self.make_abr(self.make_name(self.recognize_adress__(self.getAuthorZone(path))))
                auteurstmp = meta['author'].split(';')
                if auteursliste :
                    i = 0
                    for val in auteursliste :
                        matches1 = re.compile(rf'{val[0].split()[0]}').findall(meta['author'].lower())
                        matches2 = re.compile(rf'{val[0].split()[1]}').findall(meta['author'].lower())
                        if matches1 :
                            if matches2 :
                                auteurs.append((" ".join(matches1+matches2),val[1]))
                            else :
                                auteurs.append((" ".join(matches1),val[1]))
                        elif matches2 :
                            auteurs.append((matches2,val[1]))
                        else :
                            for j in range(len(auteurstmp)) :
                                print(val[2])
                                print(auteurstmp[j])
                                if re.compile(rf'{val[2]}').findall(self.make_abr_name(auteurstmp[j])) :
                                    print(auteurstmp[j])
                                    auteurs.append((auteurstmp[j],val[1]))
                        i += 1
            else :
                auteursliste = self.make_abr(self.make_name(self.recognize_adress__(self.getAuthorZone(path))))
                if auteursliste != [] :
                    for val in auteursliste :
                        print("2")
                        auteurs.append((val[0],val[1]))
                else :
                    auteursliste = self.recognize_name(self.getAuthorZone(path))
                    if auteursliste != [] :
                        print("3")
                        auteurs = ", ".join(auteursliste)
                    else :
                        print('4')         
        return auteurs

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
    """
    def to_formalize(self,texte) :
        pass
    
    """
    fonction qui retourne le block des refs
    input : path
    output : numero du block et de page
    """
    def getRefsBlockNumber(self,path) :
        j = 0
        size = 0
        result = [0,0,0]
        pattern = re.compile(r'reference')
        with fitz.open(path) as pdf :
            for page in pdf :
                blocks = page.get_text('dict')['blocks']
                i = 0
                for block in blocks :
                    if self.skipable(block) :
                        for line in block['lines'] :
                            for span in line['spans'] :
                                matches = pattern.findall(span['text'].lower())
                                if matches :
                                    if size < span['size'] :
                                        size = span['size']
                                        result[0] = j
                                        result[1] = i
                                        result[2] = size
                    i += 1
                j += 1
        return result
    
    """
    fonction qui retourne les references
    input : path
    output = refs
    """
    def find_refs(self,path) :
        result = ""
        with fitz.open(path) as pdf :
            npage = self.getRefsBlockNumber(path)[0]
            nblock = self.getRefsBlockNumber(path)[1]
            nsize = self.getRefsBlockNumber(path)[2]
            boolean = False
            print(pdf.page_count)
            for i in range(npage,pdf.page_count) :
                current = pdf.load_page(i)
                blocks = current.get_text('dict')['blocks']
                i = 0
                for block in blocks :
                    if self.skipable(block) :
                        if i >= nblock :
                            for line in block['lines'] :
                                for span in line['spans'] :
                                    if nsize == span['size'] :
                                        boolean = True
                                    if boolean == True :
                                        result += " " + span['text'] 
                    i +=1
        return result
                    
               
            
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
    summarize(parser,path1,path2)

if __name__ == "__main__" :
    parser = Parser()
    print(parser.getAuthorZone(sys.argv[1]))
    print()
    print(parser.getAuthor(sys.argv[1]))
    
    
    """
    if len(sys.argv) == 3 :
        main(sys.argv[1],sys.argv[2])
    else :
        main(sys.argv[1])
    """