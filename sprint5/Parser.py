import re
import fitz
import os
import sys
from langdetect import detect

class Parser :

    def __init__(self,path) :
        self.path = path
        self.pages = getPages(path)[0]
        self.pdf = getPages(path)[1]
    
#------------------------------------------------------------------------------

#EXTRACTION DU TITRE
    
#------------------------------------------------------------------------------   
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
    fonction qui trouve le titre
    input : path
    output : titre
    """
    def findTitle(self) :
        target = self.getTitleSize()[0] #la taille max
        result = ""
        blocks = self.pages[0].get_text('dict')['blocks']
        for block in blocks :
            if self.skipable(block) :
                for line in block['lines'] :
                    for span in line['spans'] :
                        if span['size'] == target :
                            result += " " + str(span['text'])#.encode('utf-8'))
        return result.strip() #enleve les espaces inutiles
    

    """
    fonction qui retourne la taille max de la police du texte
    input : path
    output : int size , numero pos du block dans une liste
    """
    def getTitleSize(self) :
        result = 0
        pos = None
        i = 0
        blocks = self.pages[0].get_text('dict')['blocks']
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
    
    
#------------------------------------------------------------------------------

#EXTRACTION DE L'ABSTRACT
    
#------------------------------------------------------------------------------
 
    """
    fonction qui retourne la position du block d'intro et d'abstract
    input : chemin du fichier
    output : i le nombre de tour pour atteindre le block de l'intro et d'abstract dans une liste
    """
    def findAbsBlock(self) : 
        pat1 = re.compile(r'abstract')
        abs = 0              #pos de abs
        b1 = False              #signe si on trouve abstract
        result = [abs]
        blocks = self.pages[0].get_text('dict')['blocks']
        for block in blocks : #je parcours chaque block
            if self.skipable(block) :
                for line in block['lines'] : #je parcours chaque ligne de chaque block
                    for span in line['spans'] : #parcours de ligne et recuperation du texte
                        matches1 = pat1.findall(span['text'].lower())
                        if matches1 :
                            if b1 == False :
                                result[0] = abs
                                b1 = True
            abs += 1
        return result
    
    """
    fonction qui retourne la position du block d'intro et d'abstract
    input : chemin du fichier
    output : i le nombre de tour pour atteindre le block de l'intro et d'abstract dans une liste
    """
    def findIntroBlock(self) : 
        pat2 = re.compile(r'ntroduction') #longue histoire
        intro = 0            #pos de intro
        b2 = False              #signe si on trouve intro
        result = [intro,0,None]
        blocks = self.pages[0].get_text('dict')['blocks']
        for block in blocks : #je parcours chaque block
            if self.skipable(block) :
                for line in block['lines'] : #je parcours chaque ligne de chaque block
                    for span in line['spans'] : #parcours de ligne et recuperation du texte
                        matches2 = pat2.findall(span['text'].lower())
                        #print(type(span['font']))
                        if matches2 :
                            if b2 == False :
                                result[0] = intro
                                result[1] = span['size']
                                result[2] = span['font']
                                #print(result[2])
                                b2 = True
            intro += 1
        return result

    """
    fonction qui retourne l'abstract
    input : path
    output : abstract et sa pos dans une liste
    """
    def findAbstract(self) :
        result = ""
        pos = 0
        abs = self.findAbsBlock()[0]
        intro = self.findIntroBlock()[0]
        if abs != 0 : #and abs < intro : #donc si l'abstract est delimimité par le mot abstract
            if re.compile(r'Abstract').findall(self.biggestBlock(abs,intro)[0]) == [] :
                #si l'abstract se trouve dans 2 blocks differents
                result = self.smallestBlock(abs,intro)[0] + self.biggestBlock(abs,intro)[0] 
                pos = self.biggestBlock(abs,intro)[1]-1
            else :
                result = self.biggestBlock(abs,intro)[0]
                pos = self.biggestBlock(abs,intro)[1]
        else :
            result = self.biggestBlock(intro-2,intro)[0]
            pos = self.biggestBlock(intro-2,intro)[1]
        return [result.strip(),pos] #.encode('utf-8') #enleve les espaces inutiles

    """
    fonction qui retourne le block de texte le plus grand
    input : path , i start , j limite
    output : le block en texte et le numero dudit block dans une liste
    """
    def biggestBlock(self,i,j) :
        result = ""
        tmp = 0
        data = 0
        blocks = self.pages[0].get_text('blocks')
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
    def smallestBlock(self,i,j) :
        result = ""
        tmp = 0
        data = 0
        blocks = self.pages[0].get_text('blocks')
        for block in blocks :
            if tmp < self.biggestBlock(i,j)[1] :
                data = tmp #stocke le numero du block de l'abstract
                result = block[4]
            tmp += 1
        return [result,data]


#------------------------------------------------------------------------------

#EXTRACTION DE L'INTRODUCTION
    
#------------------------------------------------------------------------------

    """
    fonction qui retourne l'intro
    input : path
    output : intro en string
    """
    def findIntro(self) :
        result = ""
        b = True
        pattern = re.compile(r'ntroduction')
        font = self.findIntroBlock()[2]
        size = self.findIntroBlock()[1]
        for page in self.pages :
            blocks = page.get_text('dict')['blocks']
            for block in blocks :
                if self.skipable(block) :
                    for line in block['lines'] :                           
                        for span in line['spans'] :
                            if font == span['font'] and size == span['size'] :
                                matches = pattern.findall(span['text'].lower())
                                if matches :
                                    b = False
                                else :
                                    b = True
                            if b == False :
                                result += " " + span['text']
            result = result.replace("&","&amp;").replace("<", "&lt;").replace(">", "&gt;")
            return result


#------------------------------------------------------------------------------

#EXTRACTION DES REFERENCES BIBLIOGRAPHIQUES
    
#------------------------------------------------------------------------------

    """
    fonction qui retourne le block des refs
    input : path
    output : numero du block et de page
    """
    def getRefsBlockNumber(self) :
        j = 0
        size = 0
        result = [0,0,0]
        pattern = re.compile(r'eference') #souvent le r est sur une autre ligne 
        for page in self.pages :
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
    def findRefs(self) :
        result = ""
        npage = self.getRefsBlockNumber()[0]
        nblock = self.getRefsBlockNumber()[1]
        nsize = self.getRefsBlockNumber()[2]
        boolean = False
        for i in range(npage,len(self.pages)) :
            current = self.pages[i]
            blocks = current.get_text('dict')['blocks']
            j = 0
            for block in blocks :
                if self.skipable(block) :
                    if j >= nblock :
                        for line in block['lines'] :
                            for span in line['spans'] :
                                if nsize == span['size'] :
                                    boolean = True
                                if boolean == True :
                                    result += " " + span['text'] 
                j +=1
        result = result.replace("&","&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return result
   

#------------------------------------------------------------------------------

#EXTRACTION DE LA CONCLUSION ET DE LA DISCUSSION
    
#------------------------------------------------------------------------------

    """
    fonction qui retourne la conclusion
    input : path et un paramtre qui dit si on veut la conclusion ou la discussion
    output : conclusion en string
    """
    def find_discussion_or_conclusion(self,r="c") :
        result = ""
        b = True
        if r == 'd' : #pour une discussion
            pat1 = re.compile(r'onclusion')
            pattern = re.compile(r'iscussion')
        else : #pour une conclusion
            pat1 = re.compile(r'iscussion')
            pattern = re.compile(r'onclusion')
        font = self.findIntroBlock()[2]
        size = self.findIntroBlock()[1]
        for page in self.pages :
            blocks = page.get_text('dict')['blocks']
            for block in blocks :
                if self.skipable(block) :
                    for line in block['lines'] :                           
                        for span in line['spans'] :
                            if font == span['font'] and size == span['size'] :
                                matches = pattern.findall(span['text'].lower())
                                if matches :
                                    b = False
                                if (pat1.findall(span['text'].lower())) :
                                    b = True
                                else :
                                    pat1 = re.compile(r'eference')
                                    if (pat1.findall(span['text'].lower())) :
                                        b = True
                            if b == False :
                                result += " " + span['text']
            result = result.replace("&","&amp;").replace("<", "&lt;").replace(">", "&gt;")
            return result

#------------------------------------------------------------------------------

#EXTRACTION DU DEVELOPPEMENT
    
#------------------------------------------------------------------------------

    """
    fonction qui retourne le corps du pdf
    input : path
    output : corps en string
    """
    def findCorps(self) :
        result = ""
        primo = False #si on trouve l'intro
        secundo = False #si on trouve le block qui suit l'intro
        trois = False #signale si on trouve la fin
        font = self.findIntroBlock()[2]
        size = self.findIntroBlock()[1]
        pat1 = re.compile(r'ntroduction')
        print(self.nearestPart()[0])
        pat2 = re.compile(rf'{self.nearestPart()[0]}')
        for page in self.pages :
            blocks = page.get_text('dict')['blocks']
            for block in blocks :
                if self.skipable(block) :
                    for line in block['lines'] :
                        for span in line['spans'] :
                            if primo == False :
                                if span['font'] == font and span['size'] == size :
                                    if pat1.findall(span['text'].lower()) :
                                        primo = True
                            else :
                                if span['font'] == font and span['size'] == size :
                                    secundo = True
                                    matches = pat2.findall(span['text'].lower())
                                    if matches :
                                        trois = True
                            if secundo == True and trois == False :
                                result += " " + span['text']
        result = result.replace("&","&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return result

    """
    fonction qui retourne le block le plus proche entre la conclusion et la discussion
    input : path ,p1 et p2 des pattern de regex
    output : block en string
    """
    def nearestPart(self) :
        p1 = re.compile(r'onclusion')
        p2 = re.compile(r'iscussion')
        font = self.findIntroBlock()[2]
        size = self.findIntroBlock()[1]
        for page in self.pages :
            blocks = page.get_text('dict')['blocks']
            for block in blocks :
                if self.skipable(block) :
                    for line in block['lines'] :
                        for span in line['spans'] :
                            if span['font'] == font :
                                matches1 = p1.findall(span['text'].lower())
                                matches2 = p2.findall(span['text'].lower())
                                if span['size'] == size :  
                                    if matches1 :
                                        return matches1
                                    if matches2 :
                                        return matches2
                                else :
                                    if matches1 :
                                        return matches1
                                    if matches2 :
                                        return matches2
        return None
       
        
#------------------------------------------------------------------------------

#EXTRACTION DES ADRESSES MAILS DES AUTEURS
    
#------------------------------------------------------------------------------

    """
    fonction de reconnaissance des adresses mails
    retourne un tuple avec liste contenant le prefixe de chaque adresse
    --> et une liste contenant les types
    """
    def recognize_adress__(self,chaine) :
        adr1 = r'([\w+.+-]+)@([\w+.+-]+)' #format adresse mail classique
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
            matches1[0][1].replace('\n','')
            result[0] = matches1
        if matches2 :
            result[1] = matches2[0]
        if matches3 :
            #print(matches3)
            result[2] = matches3[0]
        return result

    """
    fonction qui retourne la zone du texte pour la recherche des auteurs
    input : path
    output : block
    """
    def getAuthorZone(self) :
        i = 0
        top = self.getTitleSize()[1] #je prends le block du titre
        bottom = self.findAbstract()[1] 
        bottompattern = re.compile(rf'{self.findAbstract()[0]}')
        result = ""
        boolean = False
        blocks = self.pages[0].get_text('blocks')
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
   
#------------------------------------------------------------------------------

#EXTRACTION DES NOMS D'AUTEURS
    
#------------------------------------------------------------------------------

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
                t[0][i][1] #= t[0][i][1].replace('\n','')
                #print(t[0][i][1])
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
            #print(jul[0])
            abr += (jul[0])
            #print(abr)
        return (nom,abr)

   
    """
    reconnait des chaines qui ont la forme d'un nom
    input : chemin du fichier
    output : liste des supposés noms
    """
    def getAuthors(self) :
        auteurs = []
        auteursliste = self.make_abr(self.make_name(self.recognize_adress__(self.getAuthorZone())))
        if auteursliste != [] :
            for val in auteursliste :
                auteurs.append((val[0],val[1])) 
        return auteurs
    
    """
    fonction de reconnaissance
    input : zone de texte
    output : liste
    """
    def takeGoodString(self,zone,motif) :
        tabMotif = motif.split()
        result = []
        tabZone = zone.split()
        for val,jul in zip(tabZone[:len(tabZone)-1],tabZone[1:]) :
            for m in tabMotif :
                if m in val.lower() or jul.lower() :
                    result.appenf(' '.join([val,jul]))
        return result
    
#------------------------------------------------------------------------------

#fin du processus
    
#------------------------------------------------------------------------------
    """
    """
    def closeFile(self) :
        self.pdf.close


 
   

   
#------------------------------------------------------------------------------

#FONCTIONS UTILES DANS TOUTE LA CLASSE
    
#------------------------------------------------------------------------------   

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

"""
fonction qui reconnait des noms dans du texte
input : texte
output : auteurs en str
"""
def takeAuthors(texte) :
    nlpfr = spacy.load('fr_core_news_sm')
    tmp = nlpfr(texte)
    for val in tmp.ents :
        if val.label_ == 'PER' :
            print(val.text)

"""
fonction de reconnaissance
input : zone de texte
output : liste
"""
def takeGoodString(zone,motif) :
    tabMotif = motif.split()
    print(tabMotif)
    result = []
    tabZone = zone.split()
    for val,jul in zip(tabZone[:len(tabZone)-1],tabZone[1:]) :
        for m in tabMotif :
            """
            print(val," -- ",jul)
            print(val.lower(),"yyyy")
            print(len(val))
            print(m.lower(),"xxxx")
            """
            if m.lower() in val.lower() or m in jul.lower() :
                """
                if m.lower() in jul.lower() :
                    print(True)
                """
                result.append(' '.join([val,jul]))
    return result

"""
fonction qui normalise les noms
"""

"""
input : path du fichier
output : retourne une liste de page
"""
def getPages(path) :
    res = []
    pdf = fitz.open(path)
    for i in range(len(pdf)) :
        res.append(pdf.load_page(i))
    return res,pdf


def main(path) :
    parser = Parser(path)
    #print(parser.findCorps())
    print(parser.find_discussion_or_conclusion("d"))

    #print("ta maman")
    """
    zone = "je suis Nailman Mugisho dans ta maman"
    motif = "Nailman"
    result = takeGoodString(zone,motif)
    print(result)
    res = (getPages(path))
    print(type(res[0]))
    parser = Parser(path)
    print(parser.findTitle())
    """


if __name__ == "__main__" :
    main(sys.argv[1])
