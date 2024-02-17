import re
import fitz
import os
import pathlib

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
"""
def getBlocks(path) :
    with fitz.open(path) as pdf :
        page = pdf.load_page(0)
        blocks = page.get_text('blocks')
        i = 0
        #print(type(blocks))
        for block in blocks :
            i += 1
            print(block[4].encode('utf-8'))
            print("#########################",end='\n')
            """
            if i == 2 :
                break
            """



"""
fonction pour reconnaitre un nom dans le texte
input : path du fichier
output : boolean
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
    getBlocks(path4)


if __name__ == "__main__" :
    main()