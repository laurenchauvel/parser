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
        self.reference = ""
        self.parser = prs.Parser(path)
        
    
    def find_abstractTXT(self) :
        """
            Supprime Abstract s'il revient deux fois
            Input :     self
                        path : chemin du fichier pdf 
                        
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
                        path : chemin du fichier pdf 
                        
            Output :    self.authors: les auteurs 
        """  
        auteurs = self.parser.getAuthors()
        val=""
        if isinstance(auteurs, list) and auteurs:
            for auteur in auteurs:
                val += auteur[0]+","+auteur[1]+"\n"
            self.authors = val
            return self.authors
        else :
            self.authors = auteurs
            return self.authors
     
    def find_titleTXT(self) :
        """
            Trouve le titre 
            Input :     self
                        path : chemin du fichier pdf 
                        
            Output :    self.title: le titre
        """  
        self.title = self.parser.findTitle()
        return self.title
      
    def find_RefsTXT(self):
        """
            Trouve les références bibliographie
            Input :     self
                        
                        
            Output :    self.referennce: les references
        """  
        self.reference = self.parser.findRefs()
        return self.reference
    
    def write_file(fileTXT, src, dst):
        """
            Ecris le fichier TXT 
            Input :     self
                        path : chemin du fichier pdf 
        """  
    
        if not os.path.exists(dst):
            os.makedirs(dst)
        base_name = os.path.splitext(os.path.basename(src))[0]

        # Chemin du fichier de destination
        dfile = os.path.join(dst, base_name + '.txt')
        
        # Extraction des informations et écriture dans le fichier de destination
        with open(src, 'r'), open(dfile, 'w') as d:
            d.write("Nom fichier source : ")
            d.write(base_name + ".pdf")
            d.write("\n_____________________________\n")
            d.write("Titres : ")
            d.write(fileTXT.find_titleTXT())
            d.write("\n_____________________________\n")
            d.write("Auteurs : ")
            d.write(str(fileTXT.getAuthorTXT()))
            d.write("\n")
            d.write("\n_____________________________\n")
            d.write("Abstract : ")
            d.write(str(fileTXT.find_abstractTXT()[0]))
            d.write("\n_____________________________\n")
            d.write("Bibliographie : ")
            d.write(fileTXT.find_RefsTXT())
                    