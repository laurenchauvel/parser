#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 22:52:14 2024

@author: lalatiana
"""

import fitz  # PyMuPDF
import os
import shutil
def extract_abstract(pdf_path):
    
    doc = fitz.open(pdf_path)
    abstract = ""
    recording = False

    for page in doc:  
        text = page.get_text()
        if not recording:
            #Vérifie si le texte contient Abstract
            if "Abstract—" in text or "Abstract" in text:
                recording = True
                start_index = text.find("Abstract—") if "Abstract—" in text else text.find("Abstract")
                text = text[start_index:]  

        if recording:
            # Vérifie si le texte contient Introduction ou INTRODUCTION et s'arrete là
            if "Introduction" in text or "INTRODUCTION" in text:  
                end_index = text.find("Introduction") if "Introduction" in text else text.find("INTRODUCTION")
                abstract += text[:end_index].strip()
                break  # si la fin est trouvé
            else:
                abstract += text
    
    return abstract


def process_pdfs(input_dir):
    output_dir = os.path.join('../parserV1', "abstracts")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)  # Supprime le dossier existant
    os.makedirs(output_dir)  # Crée un nouveau dossier

    for filename in os.listdir(input_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            abstract = extract_abstract(pdf_path)
            output_filename = os.path.join(output_dir, filename.replace('.pdf', '.txt'))
            with open(output_filename, 'w') as f:
                f.write(abstract)

process_pdfs('../corpus/pdf')