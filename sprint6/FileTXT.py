#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 14:53:52 2024

@author: lalatiana
"""

import os
import prototype as prs

class FileTXT:
    def __init__(self,path):
        self.parser = prs.Parser(path)
        self.parser.remplir_dico()
        self.title = self.parser.extract_title()
        self.references = self.parser.extract_references()
        self.introduction = self.parser.extract_intro()
        self.discussion = self.parser.extract_discussion()
        self.conclusion = self.parser.extract_conclusion()
        self.authors = ""
        self.abstract = ""
        
    """
    Supprime Abstract s'il revient deux fois
    Input : self
    Output : self.abstract : le résumé 
    """            
    def find_abstractTXT(self) :
        resultat = self.parser.extract_abstract()
        abstract = resultat.replace("Abstract", "")  
        self.abstract = abstract.strip()
        return self.abstract
    

    """
    Traite les valeurs d'un tableau de auteurs 
    Input : self
    Output : self.authors: les auteurs 
    """  
    def getAuthorTXT(self):
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
    """
    Trouve le titre 
    Input : self
    Output : self.title: le titre
    """  
    def find_titleTXT(self) :
        self.title = self.parser.extract_title()
        return self.title
    
    """
    Ecris le fichier TXT 
    Input : self , src : chemin du fichier pdf , dst : chemin de la destination
    """  
    def write_file(self, src, dst):
        if not os.path.exists(dst):
            os.makedirs(dst)
        base_name = os.path.splitext(os.path.basename(src))[0]
        # Chemin du fichier de destination
        dfile = os.path.join(dst, base_name + '.txt')
        content = self.parser.extract_affiliation()
        if content is None:
            content = "" 
        # Extraction des informations et écriture dans le fichier de destination
        with open(src, 'r'), open(dfile, 'w') as d:
            d.write("Nom fichier source : ")
            d.write(base_name + ".pdf")
            d.write("\n_____________________________\n")
            d.write("Titres : ")
            d.write(self.title)
            d.write("\n_____________________________\n")
            d.write("Affiliation : ")
            c=""
            if isinstance(content, list) and content:
                for cont in content:
                        c+=str(cont)+" "
            d.write(c)
            d.write("\n_____________________________\n")
            d.write("Auteurs : ")
            d.write(str(self.getAuthorTXT()))
            d.write("\n")
            d.write("\n_____________________________\n")
            d.write("Abstract : ")
            d.write(str(self.find_abstractTXT()))
            d.write("\n_____________________________\n")
            d.write("Biblio : ")
            d.write(self.references)
            prs.closePdf(self.parser.pdf)
            
                    