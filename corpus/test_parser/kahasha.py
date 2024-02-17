import re
import fitz
import os
import pathlib
from langdetect import detect

"""
fonction de reconnaissance des adresses mails
retourne un tuple avec liste contenant le prefixe de chaque adresse
--> et une liste contenant les types
"""
def recognize_adress(path) :
    adr1 = r'([\w+.+ +-]+)@' #format adresse mail classique
    adr2 = r'\(?{?(\w+)(,\ \w+)*}?\)?@' #format de regroupement
    pattern1 = re.compile(adr1)
    pattern2 = re.compile(adr2)
    result = [None,None]
    with fitz.open(path) as res :
        matches1 = pattern1.findall(res.load_page(0).get_text())
        matches2 = pattern2.findall(res.load_page(0).get_text())
        if (matches1) :
            result[0] = matches1
        if (matches2) :
            result[1] = matches2[0]
    return result

"""
fonction permettant de former des noms
input : une liste de prefixe d'adresse
output : une liste de nom 
"""
def make_name(t) :
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
def make_abr(li) :
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
def recognize_name(path) :
    result = []
    reg = r'[A-Z]*\w*-*[A-Z]\w+ [A-Z]*.*[A-Z]* [A-Z]*\w*-*[A-Z]\w+' #forme des noms
    pattern = re.compile(reg)
    with fitz.open(path) as fic :
        matches = pattern.findall(fic.load_page(0).get_text())
        if matches :
            result = matches
    return result

"""
fonction qui retourne les auteurs
input : le path
output : liste d'auteurs
"""
def recognize_author(path) :
    author = []
    with fitz.open(path) as pdf :
        potentiel = recognize_name(path)
        adr = make_abr(make_name(recognize_adress(path)))
        for val in potentiel :
            for jul in adr[0][0].split() :
                regex = rf'{jul}'
                pat = re.compile(regex)
                matches = pat.match(val.lower())
                if matches :
                    author.append(val)
    return author

"""
fonction qui print les auteurs d'un corpus
input : path du dossier
output : None
"""
def summarize_corpus(path) :
    dos = pathlib.Path(path)
    with dos :
        for element in dos.iterdir() :
            if str(element) != "/mnt/c/Users/KAHASHA/Documents/ubs/licence3/s2/parser/corpus/pdf/-Y" :
                print(element)
                print(recognize_author(element))
    return None

"""
fonction qui retourne les differents blocks
input : chemin du fichier
output : info sur le block
"""
def getBlocks(path) :
    with fitz.open(path) as pdf :
        page = pdf.load_page(0)
        #blocks = page.get_text('dict')['blocks']
        blocks = page.get_text('blocks')
        reg  = r'Introduction'
        pat = re.compile(reg)
        i = 0
        #print(len(blocks))
        print()
        #print(blocks)
        i = 0
        for block in blocks :
            #print(block[4])
            #if  skipable(block) :
                print(block[4],"\n_______________\n")
                """
                for line in block['lines'] :
                    for span in line['spans'] :
                        i += 1
                        print(span['size'])
                        print(span['font'])
                        print(span['text'])
                        print(i)
                        print()
                        matches = pat.findall(span['text'])
                
                        
                        print(matches)
                        if matches :
                            return i
                            print("exist")
                            break
                        
                        print("xxx")
                        print()
                        
                        print(len(block['lines']))
                        print()
                        print(block['lines']['spans'])
                        print()
                        """
                        #print(block)
                
        
"""
fonction qui retourne la position du block d'intro
input : chemin du fichier
output : i le nombre de tour pour atteindre le block de l'intro
"""
def find_intro(path) :
    regex1 = r'Abstract'
    regex2 = r'INTRODUCTION'
    pat1 = re.compile(regex1)
    pat2 = re.compile(regex2)
    j = 0
    intro = ""
    result = [None,None]
    with fitz.open(path) as pdf : #je recupere les differents blocks du pdf
        blocks = pdf.load_page(0).get_text('dict')['blocks']
        #print(pdf.load_page(0).get_text('blocks')[4][6])
        #print(blocks[6][4])
        #print(pdf.load_page(0).get_text())
        for block in blocks : #je parcours chaque block
            #print(pdf.load_page(0).get_text('blocks')[6][4].encode('utf-8'))
            j += 1
            for line in block['lines'] : #je parcours chaque ligne de chaque block
                #print(type(line))
                for span in line['spans'] : #parcours de ligne et recuperation du texte
                    matches1 = pat1.findall(span['text'])
                    matches2 = pat2.findall(span['text'])
                    if matches1 :
                        print(matches1)
                        result[1] = j
                    if matches2 :
                        print(matches2)
                        result[1] = j
        #on conserve le texte de l'intro
        result[0] = pdf.load_page(0).get_text('blocks')[j-1][4].encode('utf-8')
    return result

"""
fonction qui trouve le titre
input : path
output : titre
"""
def find_title(path) :
    with fitz.open(path) as pdf :
        target = get_size(path)
        result = ""
        blocks = pdf.load_page(0).get_text('dict')['blocks']
        for block in blocks :
            if skipable(block) :
                for line in block['lines'] :
                    for span in line['spans'] :
                        if span['size'] == target :
                            result += str(span['text'])#.encode('utf-8'))
    return result

"""
fonction qui trouve le block du titre
"""

"""
fonction qui skip un block
input : block
output : boolean
"""
def skipable(block) :
    #verifie si c'est du texte
    if block['type'] == 0 :
        return True
    return False

"""
fonction qui retourne la taille max de la police du texte
input : path
output : int size
"""
def get_size(path) :
    with fitz.open(path) as pdf :
        result = 0
        blocks = pdf.load_page(0).get_text('dict')['blocks']
        for block in blocks :
            if skipable(block) == True : #skip si c'est pas du texte
                for line in block['lines'] :
                    for span in line['spans'] :
                        size = span['size']
                        #si ce n'est pas un mot je le skip
                        if size > result and (is_in_language(span['text'],'en')) == True :
                            result = size
    return result

"""
fonction qui trouve l'abstract
input : path
output : abstract
"""
def find_absract(path) :
    with fitz.open(path) as pdf :
        #l'abstract est donc le block juste avant l'entrée
        return pdf.load_page(0).get_text('blocks')[find_intro(path)[1]][4].encode('utf-8')

"""
fonction pour donner les titres d'un corpus
input : path du dossier
output : les titres
"""
def corpus_title(path) :
    for fichier in os.listdir(path) :
        f = os.path.join(path,fichier)
        if os.path.isfile(f) :
            print(find_title(f))


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
text = "Googletrans est une bibliothèque python gratuite et illimitée qui a implémenté l'API Google Translate"
print(is_in_language(text, 'fr'))  # Retourne True si le texte est en français
"""

        



def main() :
    """
    path1 = "/mnt/c/Users/KAHASHA/Documents/ubs/licence3/s2/parser/corpus/pdf/Das_Martins.pdf"
    print((recognize_adress(path1)[1]))
    print(make_abr(make_name(recognize_adress(path1))))
    print(recognize_author(path1))
    print("========================================================================================")
    path2 = "/mnt/c/Users/KAHASHA/Documents/ubs/licence3/s2/parser/corpus/pdf/Gonzalez_2018_Wisebe.pdf"
    #print(recognize_name(path2))
    print(make_abr(make_name(recognize_adress(path2))))
    print(recognize_author(path2))
    print("========================================================================================")
    path3 = "/mnt/c/Users/KAHASHA/Documents/ubs/licence3/s2/parser/corpus/pdf/kessler94715.pdf"
    print(make_abr(make_name(recognize_adress(path3))))
    print(recognize_author(path3))
    print("========================================================================================")
    """
    path4  = "/mnt/c/Users/KAHASHA/Documents/ubs/licence3/s2/parser/corpus/pdf/mikheev J02-3002.pdf"
    #print(getBlocks(path4))
    print(find_title(path4))
    #corpus_title("/mnt/c/Users/KAHASHA/Documents/ubs/licence3/s2/parser/corpus/pdf/")


if __name__ == "__main__" :
    main()