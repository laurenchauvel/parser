import os
import fitz
import re
from langdetect import detect

#------------------------------------------------------------------------------
#Fonction qui transforme tous les fichiers PDF d'un repertoire en fichiers .txt
#Puis extrait les 4 premières lignes du fichier .txt
#input : directory
#------------------------------------------------------------------------------
def pdf_to_text_directory(directory):
    title = ""
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            
            #on conertit les pdf en .txt
            pdf_path = os.path.join(directory, filename)
            txt_path = os.path.join(directory+"/results", os.path.splitext(filename)[0] + '.txt')
            #pdf_to_text(pdf_path, txt_path)
            
            
            title = find_title(pdf_path)
            
            print("\n", filename, "\nTitre : ", title)
   
            
#------------------------------------------------------------------------------
#Fonction qui trouve le titre
#input : path
#output : titre
#------------------------------------------------------------------------------
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
                            result += " "+str(span['text'])#.encode('utf-8'))
    return result


#------------------------------------------------------------------------------
#Fonction qui skip un block
#input : block
#output : boolean
#------------------------------------------------------------------------------
def skipable(block) :
    #verifie si c'est du texte
    if block['type'] == 0 :
        return True
    return False


#------------------------------------------------------------------------------
#Fonction qui retourne la taille max de la police du texte
#input : path
#output : int size
#------------------------------------------------------------------------------
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

#------------------------------------------------------------------------------
#Fonction qui dit si une chaine appartient bien à une langue
#source : microsoft copilot
#input : text , prefixe dans la langue
#output : boolean
#------------------------------------------------------------------------------
def is_in_language(text, language):
    try:
        detected_language = detect(text)
        return detected_language == language
    except:
        return False

"""            
#------------------------------------------------------------------------------
#Fonction qui transforme un fichier pdf en txt
#------------------------------------------------------------------------------
def pdf_to_text(pdf_path, txt_path):
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)
            
#------------------------------------------------------------------------------
#Foncction qui permet de trouver le titre du doc
#(non aboutie)
#------------------------------------------------------------------------------          
def search_title(pdf_path, txt_path):
    title = get_pdf_title(pdf_path) #regarde si le titre est dans les metadatas
    police_max=0
    pos=0


    #si le titre n'est pas renseigné dans les metadonnees ou qu'il commence par un caractere special
    if(title==None or re.match(r'^\W', title)):
        first_lines = extract_first_lines(txt_path)
        
        info=police_max(pdf_path)
        police_max=info[0]
        pos=info[1]
       # for line in first_lines:
            
            
            #title_tab = analyse_line(line)
            #title = " ".join(title_tab)
            
    return title



#------------------------------------------------------------------------------
#Fonction qui extrait les premières lignes d'un fichier .txt
#------------------------------------------------------------------------------
def extract_first_lines(txt_path, num_lines=4):
    first_lines = []
    with open(txt_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            first_lines.append(line.strip())
            if i >= num_lines - 1:
                break
    return first_lines

#------------------------------------------------------------------------------
#Chercrhe le titre dans les metadata
#------------------------------------------------------------------------------      
def get_pdf_title(pdf_path):
    try:
        # Ouvrir le document PDF
        doc = fitz.open(pdf_path)

        # Extraire le titre
        title = doc.metadata.get('title', 'No Title')

        # Fermer le document
        doc.close()

        return title
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'extraction du titre : {e}")
        return None

#------------------------------------------------------------------------------
#Renvoie la taille de police max et la position de la ligne dan le texte
#------------------------------------------------------------------------------
def police_max(pdf_path, num_lines=4):
    largest_font_size = 0
    first_line_position = None
    with fitz.open(pdf_path) as doc:
        for page in doc:
            # Obtenez les informations de texte sous forme de dictionnaire
            text_instances = page.get_text("dict")

            # Trier les instances de texte par ordre de position verticale puis horizontale
            text_instances.sort(key=lambda x: (x["top"], x["x0"]))

            # Parcourir les quatre premières lignes de chaque page
            for inst in text_instances:
                if inst["top"] > text_instances[0]["top"] + 4 * inst["height"]:
                    break  # Sortir de la boucle si on a dépassé les quatre premières lignes
                if inst["size"] > largest_font_size:
                    largest_font_size = inst["size"]
                    first_line_position = inst["top"]

    return largest_font_size, first_line_position
"""



pdf_directory = "C:/Users/laure/OneDrive/Desktop/parser/corpus/pdf" 
pdf_to_text_directory(pdf_directory)






