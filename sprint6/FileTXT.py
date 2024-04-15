#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 14:53:52 2024

@author: lalatiana
"""

import os
import Parser as prs

class FileTXT:
    def __init__(self,path):
        self.title = ""
        self.authors = ""
        self.abstract = ""
        self.parser = prs.Parser(path)
        
    
    def find_abstractTXT(self) :
        """
            Supprime Abstract s'il revient deux fois
            Input :     self
            Output :    self.abstract : le résumé 
        """            
        resultat, pos = self.parser.findAbstract()
        abstract = resultat.replace("Abstract", "")  
        self.abstract = [abstract.strip(), pos]
        return self.abstract
    
    def getAuthorTXT(self):
        """
            Traite les valeurs d'un tableau de auteurs 
            Input :     self
            Output :    self.authors: les auteurs 
        """  
        auteurs = self.parser.getAuthors()
        val=""
        if isinstance(auteurs, list) and auteurs:
            for auteur in auteurs:
                val+=str(auteur)+" "
            self.authors = val
            return self.authors
        else :
            self.authors = auteurs
            return self.authors
     
    def find_titleTXT(self) :
        """
            Trouve le titre 
            Input :     self
            Output :    self.title: le titre
        """  
        self.title = self.parser.findTitle()
        return self.title
    
      
    def write_file(fileTXT, src, dst):
        """
            Ecris le fichier TXT 
            Input :     self
                        src : chemin du fichier pdf 
                        dst : chemin de la destination
        """  
    
        if not os.path.exists(dst):
            os.makedirs(dst)
        base_name = os.path.splitext(os.path.basename(src))[0]

        # Chemin du fichier de destination
        dfile = os.path.join(dst, base_name + '.txt')
        content = fileTXT.parser.Affiliation()
        if content is None:
            content = "" 
        # Extraction des informations et écriture dans le fichier de destination
        with open(src, 'r'), open(dfile, 'w') as d:
            d.write("Nom fichier source : ")
            d.write(base_name + ".pdf")
            d.write("\n_____________________________\n")
            d.write("Titres : ")
            d.write(str(fileTXT.find_titleTXT()))
            d.write("\n_____________________________\n")
            d.write("Affiliation : ")
            c=""
            if isinstance(content, list) and content:
                for cont in content:
                        c+=str(cont)+" "
            d.write(c)
            d.write("\n_____________________________\n")
            d.write("Auteurs : ")
            d.write(str(fileTXT.getAuthorTXT()))
            d.write("\n")
            d.write("\n_____________________________\n")
            d.write("Abstract : ")
            d.write(str(fileTXT.find_abstractTXT()[0]))
            d.write("\n_____________________________\n")
            d.write("Biblio : ")
            d.write(fileTXT.parser.findRefs())
            
                    