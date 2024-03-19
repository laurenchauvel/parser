# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 13:20:51 2024

@author: lauren
"""
import os
import Parser as par

class FileXML :

    def __init__(self, path):
        self.title = ""
        self.authors = ""
        self.abtsract = ""
        self.references = ""
        self.parser = par.Parser(path)
        
         
    """
    Ecris le fichier XML
    Input :     self
                src : chemin du fichier pdf
                dest : chemin du fichier xml de sortie
    Output :    xml_file : le fichier XML
    """    
    def write_file(self, src, dest):
    
        if not os.path.exists(dest):
            os.makedirs(dest)
        
        #Obtient le nom du fichier sans l'extension
        base_name = os.path.splitext(os.path.basename(src))[0]
        dfile = os.path.join(dest, base_name)
        
        with open(dfile,'w') as xml :
            xml.write("<article>\n")
            xml.write("\t<preamble> " + base_name + " </preamble>\n")
            xml.write("\t<titre>\n" + self.parser.findTitle() + " </titre>\n")
            xml.write("\t<auteurs>\n")
            
            for auteur in self.parser.getAuthors() :
                xml.write("\t\t<auteur>\n")
                xml.write("\t\t\t<name>\n"+auteur[0] +" </name>\n")
                xml.write("\t\t\t<mail>\n"+auteur[1] +"</mail>\n")
                xml.write("\t\t\t<affiliation>\n" +"</affiliation>\n")
                xml.write("\t\t</auteur>\n")
            
            xml.write("\t</auteurs>\n")
            xml.write("\t<abstract>\n" +self.parser.findAbstract()[0] + " </abstract>\n")
            xml.write("\t<introduction>\n" +self.parser.findIntro() + " </introduction>\n")
            xml.write("\t<corps>\n" +self.parser.findCorps() + " </corps>\n")
            xml.write("\t<conclusion>\n" +self.parser.find_discussion_or_conclusion() + " </conclusion>\n")
            xml.write("\t<discussion>\n" +self.parser.find_discussion_or_conclusion("d") + " </discussion>\n")
            xml.write("\t<biblio>\n"+ self.parser.findRefs() +" </biblio>\n")
            xml.write("</article>")

                
        
