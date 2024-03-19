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
            xml.write("<article>\n\n")
            xml.write("\t<preamble> " + base_name + " </preamble>\n\n")
            xml.write("\t<titre> " + self.parser.findTitle() + " </titre>\n\n")
            xml.write("\t<auteurs>\n")
            
            for auteur in self.parser.getAuthors() :
                xml.write("\t\t<auteur>\n")
                xml.write("\t\t\t<name> "+auteur[0] +" </name>\n")
                xml.write("\t\t\t<mail> "+auteur[1] +"</mail>\n")
                xml.write("\t\t\t<affiliation> " +"</affiliation>\n")
                xml.write("\t\t</auteur>\n\n")
            xml.write("\t</auteurs>\n\n")
            
            xml.write("\t<abstract>\n" +self.parser.findAbstract()[0] + "\n\t</abstract>\n\n")
            xml.write("\t<introduction>\n" +self.parser.findIntro() + "\n\t</introduction>\n\n")
            xml.write("\t<corps>\n" +self.parser.findCorps() + "\n\t</corps>\n\n")
            xml.write("\t<discussion>\n" +self.parser.find_discussion_or_conclusion("d") + "\n\t</discussion>\n\n")
            xml.write("\t<conclusion>\n" +self.parser.find_discussion_or_conclusion() + "\n\t</conclusion>\n\n")
            xml.write("\t<biblio>\n"+ self.parser.findRefs() +"\n\t</biblio>\n\n")
            xml.write("</article>")

                
        
