# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 13:20:51 2024

@author: lauren
"""
import os
import prototype as par

class FileXML :

    def __init__(self, path):
        self.parser = par.Parser(path)
        self.parser.remplir_dico()
        self.title = self.parser.extract_title()
        self.references = self.parser.extract_references()
        self.introduction = self.parser.extract_intro()
        self.discussion = self.parser.extract_discussion()
        self.conclusion = self.parser.extract_conclusion()
        self.abstract = self.parser.extract_abstract()
        self.authors = self.parser.extract_authors()
        
         
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
        dfile = os.path.join(dest, base_name+ ".xml")
        content = self.parser.extract_affiliation()
        if content is None:
            content = "" 
        with open(dfile,'w') as xml :
            xml.write("<article>\n")
            xml.write("\t<preamble>" + base_name+ ".pdf" + "</preamble>\n")
            xml.write("\t<titre>" + self.title + " </titre>\n")
            
            xml.write("\t<auteurs>\n")
            
            if self.authors==[] or self.authors == ['']:
                xml.write("\t\t<auteur>\n")
                xml.write("\t\t\t<name> </name>\n")
                xml.write("\t\t\t<mail> </mail>\n")
                xml.write("\t\t\t<affiliation> </affiliation>\n")
                xml.write("\t\t</auteur>\n")
            else :
                for auteur in self.authors :
                    xml.write("\t\t<auteur>\n")
                    xml.write("\t\t\t<name>"+auteur[0] +"</name>\n")
                    xml.write("\t\t\t<mail>"+auteur[1] +"</mail>\n")
                    c=""
                    if isinstance(content, list) and content:
                        for cont in content:
                            c+=str(cont)+" "
                    xml.write("\t\t\t<affiliation>" + c +"</affiliation>\n")
                    xml.write("\t\t</auteur>\n")
            
            xml.write("\t</auteurs>\n")
            xml.write("\t<abstract>\n" +self.abstract + "</abstract>\n")
            xml.write("\t<introduction>\n" +self.introduction + "</introduction>\n")
            xml.write("\t<discussion>\n" +self.discussion +"</discussion>\n")
            xml.write("\t<conclusion>\n" +self.conclusion + "</conclusion>\n")
            xml.write("\t<biblio>\n"+ self.references +"</biblio>\n")
            xml.write("</article>")

            par.closePdf(self.parser.pdf)

                
        
