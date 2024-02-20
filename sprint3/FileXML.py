# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 13:20:51 2024

@author: lauren
"""
import os

class FileXML :

    def __init__(self):
        self.title
        self.authors
        self.abtsract
        self.references
        
         
    """
    Ecris le fichier XML
    Input :     self
                src : chemin du fichier pdf
                dest : chemin du fichier xml de sortie
    Output :    xml_file : le fichier XML
    """    
    def write_file(self, src, dest):
        
        with open(dest, "w") as xml:

            xml.write("<article>\n")
            xml.write("\t<preamble> ", os.path.splitext(src) ," </preamble>\n")
            xml.write("\t<titre> ", ," </titre>\n")
            xml.write("\t<auteurs>\n")
            
            for auteur in parser.getAuthors(src) :
                xml.write("\t\t<auteur>")
                xml.write("\t\t\t<name> ", ," </name>\n")
                xml.write("\t\t\t<mail> ", , "</mail>\n")
                xml.write("\t\t</auteur>\n")
                
            xml.write("\t</auteurs>\n")
            xml.write("\t<abstract> ", ," </abstract>\n")
            xml.write("\t<biblio> ", ," </biblio>\n")
            xml.write("</article>")
            

                
        
