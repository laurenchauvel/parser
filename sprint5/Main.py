# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 14:16:36 2024

"""
import sys
import FileXML as xml
import FileTXT as txt
import os

class Main :
     
    
    def main(self, path_src, path_dest, option="-t"):
        """
        Créer les fichiers "résumés" des articles contenu dans le repertoire source
        et les place dans le repertoire destination
        Input :     path_src : chemin du repertoire source
                    path_dest : chemin du repertoire destination
                    option : "-t" pour txt, "-x" pour xml
        """

        path_src = sys.argv[1]
        path_dest = sys.argv[2]
        fichiers_pdf = self.listFiles(path_src)
        if not fichiers_pdf:
            print("Aucun fichier PDF trouvé dans le répertoire.")
            exit()
        
        print("Liste des fichiers PDF :")
        for i in range(len(fichiers_pdf)):  #affiche la liste des fichiers à l'utilisateur
            print(f"{i+1}. {fichiers_pdf[i]}")
        input_numeros = input("\nEntrez les numéros des fichiers à sélectionner séparés par des espaces sinon * pour tous les fichiers: ")
        print("\nVoici la liste des fichiers générés :")
        selectFile = self.selectFiles(path_src, input_numeros)
        
        if option == '-t' : # traitement en txt
            
            for file in selectFile :    #parcours le tableau des fichiers selectionnees
                txtMain = txt.FileTXT(file)
                print(os.path.join(os.path.splitext(os.path.basename(file))[0] + '.txt'))
                txtMain.write_file(file, path_dest) #ecris les resultats dans le dossier de destination
        elif option == '-x' :# traitement en xml
            
            for file in selectFile :    #parcours le tableau des fichiers selectionnees
                xmlMain = xml.FileXML(file)
                print(os.path.join(os.path.splitext(os.path.basename(file))[0] + '.xml'))
                xmlMain.write_file(file, path_dest)  #ecris les resultats dans le dossier de destination
                
    def listFiles(self, path_src):
        """
        Liste des fichiers PDF
        Input :     self
                    path_src : chemin du répertoire contenant les fichiers
        Output :    fichiers_pdf: la liste des fichiers PDF
        """ 
        fichiers_pdf = [os.path.join(path_src, f) for f in os.listdir(path_src) if f.endswith('.pdf') and os.path.isfile(os.path.join(path_src, f))]
        return fichiers_pdf
            
            
    def selectFiles(self, path_src, input_numeros):
        """
        Sélectionne les Fichiers sélectionnés par l'utilisateur
        Input :     self
                    path_src : chemin du fichier pdf 
                    input_numeros : les valeurs entrées par l'utilisateur'
        Output :    fichiers_selectionnees: la liste des fichiers sélectionnées par l'utilisateur
        """ 
        
        fichiers_pdf = self.listFiles(path_src)       
        if input_numeros.strip() == '*':    #si l'entrée de l'utilisateur est un * on traite tous les fichiers
            fichiers_selectionnes = fichiers_pdf
        else:   #sinon on traite le ou les fichiers correspondants
            numeros = [int(num) for num in input_numeros.split()] #liste sous forme de tableau les numéros des fichiers
            
            fichiers_selectionnes = [] #liste les fichiers entrées par l'utilisateur
            for num in numeros:
                if 1 <= num <= len(fichiers_pdf):
                    fichier_selectionne = fichiers_pdf[num - 1]
                    fichiers_selectionnes.append(fichier_selectionne)
                else:
                    print("Numéro invalide :", num)
        return fichiers_selectionnes #retourne la liste des fichiers selectionnees
        
def usage():
   print("Usage: python Main.py chemin_du_repertoire_source chemin_du_repertoire_destination [-t | -x]")
   print("Options:")
   print("  -t : Générer des fichiers texte")
   print("  -x : Générer des fichiers XML")
   sys.exit(1)

def main(s,d,o="-t") :
    main = Main()
    main.main(s,d,o)

if __name__ == "__main__" :
    
    if len(sys.argv) < 3 :
        usage()
    elif len(sys.argv) > 4 :
        usage()
    else :
        if len(sys.argv) == 4 :
            main(sys.argv[1],sys.argv[2],sys.argv[3])
        else :
            main(sys.argv[1],sys.argv[2])
            
       
    
    
        
        
        
            
            
            