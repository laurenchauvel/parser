#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 14:53:52 2024

@author: lalatiana
"""

import os
import prototype as proto

class FileTXT:
    def __init__(self):
        self.title = ""
        self.authors = ""
        self.abstract = ""
        self.parser = proto.Parser()
        
    """
        Fonction qui Supprime Abstract s'il revient deux fois
    """    
    def find_abstractTXT(self,path) :        
        resultat, pos = self.parser.findAbstract(path)
        self.abstract = resultat.replace("Abstract", "")    
        return [self.abstract.strip(), pos]
    
    """
        Fonction qui traite les valeurs d'un tableau de auteurs 
    """  
    def getAuthorTXT(self,path):
        auteurs = self.parser.getAuthor(path)
        val=""
        if isinstance(auteurs, list) and auteurs:
            for auteur in auteurs:
                val+=auteur+" "
            self.authors = val
            return self.authors
        else :
            self.authors = auteurs
            return self.authors
     
     
    """
        Fonction qui trouve le titre 
    """  
    def find_titleTXT(self,path) :
        self.title = self.parser.findTitle(path)
        return self.title
    
    """
        Ecris le fichier TXT  
    """    
    def write_file(fileTXT, src, dst):
    
            if not os.path.exists(dst):
                os.makedirs(dst)
            for fichier in os.listdir(src) :
                sfile = os.path.join(src,fichier)
                #Obtient le nom du fichier sans l'extension
                base_name = os.path.splitext(fichier)[0]
                dfile = os.path.join(dst, base_name + '.txt')
                with open(dfile,'w') as d :
                    d.write("Nom fichier source : ")
                    d.write(base_name+".pdf")
                    d.write("\n_____________________________\n")
                    d.write("Titres : ")
                    d.write(fileTXT.find_titleTXT(sfile))
                    d.write("\n_____________________________\n")
                    d.write("Auteurs : ")
                    #d.write(str(fileTXT.getAuthorTXT(sfile)))
                    d.write("\n")
                    d.write("\n_____________________________\n")
                    d.write("Abstract : ")
                    d.write(str(fileTXT.find_abstractTXT(sfile)[0]))
                    d.write("\n_____________________________\n")
                    d.write("Biblio : ")
                    d.write(fileTXT.parser.findRefs(sfile))
                    
if __name__ == "__main__" :
    fileTXT = FileTXT()
    src = "../corpus/pdf/"
    dst = "../sprint3/resultatsTXT"
    fileTXT.write_file(src,dst)
    print("réussi")