# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 14:16:36 2024

@author: laure
"""
import sys
import FileXML as xml
import FileTXT as txt

class Main :
     
    """
    Créer les fichiers "résumés" des articles contenu dans le repertoire source
    et les place dans le repertoire destination
    Input :     path_src : chemin du repertoire source
                path_dest : chemin du repertoire destination
                option : "-t" pour txt, "-x" pour xml
    """
    def main(self, path_src, path_dest, option="-t"):
        """
        if len(sys.argv) < 3 :
            SystemExit(-1)
        elif len(sys.argv) > 4 :
            SystemExit(-1)
        else :
        """
        path_src = sys.argv[1]
        path_dest = sys.argv[2]
        if option == '-t' :
            txtMain = txt.FileTXT()
            txtMain.write_file(path_src,path_dest)
        else :
            xmlMain = xml.FileXML()
            xmlMain.write_file(path_src,path_dest)

def main(s,d,o="-t") :
    main = Main()
    main.main(s,d,o)

if __name__ == "__main__" :
    if len(sys.argv) < 3 :
            SystemExit(-1)
    elif len(sys.argv) > 4 :
        SystemExit(-1)
    else :
        if len(sys.argv) == 4 :
            print("o")
            main(sys.argv[1],sys.argv[2],sys.argv[3])
        else :
            print('y')
            main(sys.argv[1],sys.argv[2])
            
    
    
    
        
        
        
            
            
            