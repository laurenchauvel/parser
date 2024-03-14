# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 13:20:51 2024

@author: lauren
"""
import os
import prototype as proto

class FileXML :

    def __init__(self):
        self.title = ""
        self.authors = ""
        self.abtsract = ""
        self.references = ""
        self.parser = proto.Parser()
        
         
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
        for fichier in os.listdir(src) :
            sfile = os.path.join(src,fichier)
            #Obtient le nom du fichier sans l'extension
            base_name = os.path.splitext(fichier)[0]
            dfile = os.path.join(dest, base_name)
            with open(dfile,'w') as xml :
                xml.write("<article>\n")
                #xml.write("\t<preamble> " + os.path.splitext(sfile) + " </preamble>\n")
                xml.write("\t<titre>\n" + self.parser.findTitle(sfile) + " </titre>\n")
                xml.write("\t<auteurs>\n")
                """
                for auteur in self.parser.getAuthors(src) :
                    xml.write("\t\t<auteur>\n")
                    xml.write("\t\t\t<name>\n"+ +" </name>\n")
                    xml.write("\t\t\t<mail>\n"+ +"</mail>\n")
                    xml.write("\t\t\t<affiliation>\n"+ +"</affiliation>\n")
                    xml.write("\t\t</auteur>\n")
                """
                xml.write("\t</auteurs>\n")
                xml.write("\t<abstract>\n" +self.parser.findAbstract(sfile)[0] + " </abstract>\n")
                xml.write("\t<introduction>\n" +self.parser.findIntro(sfile) + " </introduction>\n")
                xml.write("\t<corps>\n" +self.parser.findCorps(sfile) + " </corps>\n")
                xml.write("\t<conclusion>\n" +self.parser.find_discussion_or_conclusion(sfile) + " </conclusion>\n")
                xml.write("\t<discussion>\n" +self.parser.find_discussion_or_conclusion(sfile, "d") + " </discussion>\n")
                xml.write("\t<biblio>\n"+ self.parser.findRefs(sfile) +" </biblio>\n")
                xml.write("</article>")

                
        
