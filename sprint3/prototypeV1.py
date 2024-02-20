#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:15:51 2024

@author: lalatiana
"""

import re
from pdfminer.high_level import extract_text

def extract_general_info(pdf_path):
    text = extract_text(pdf_path)

    # Extraction du titre et sauvegarde de la position de fin
    title_match = re.search(r"^(.*?)\n(?:\n)", text, re.S)
    if title_match:
        title = title_match.group(1).strip()
        search_start = title_match.end()
    else:
        title = "Titre introuvable"
        search_start = 0

    # Commence l'extraction des auteurs à partir de la fin du titre
    authors_match = re.search(r"^(.*?)\n(?:\n|Abstract)", text[search_start:], re.S)
    if authors_match:
        authors = authors_match.group(1).strip()
        # Ajustement pour ne pas inclure "Abstract" dans les noms des auteurs
        authors = re.sub(r"\nAbstract.*", "", authors, flags=re.S).strip()
        search_start += authors_match.end()  # Met à jour le point de départ pour la recherche suivante
    else:
        authors = "Auteurs introuvables"

    # Commence l'extraction du résumé à partir de la fin des auteurs
    abstract_match = re.search(r"Abstract(.*?)\nI\. INTRODUCTION", text[search_start:], re.S)
    abstract = abstract_match.group(1).strip() if abstract_match else "Résumé introuvable"


    return title, authors, abstract


# Utilisation de la fonction
pdf_path = "../corpus/pdf2txt/Torres.pdf"  
title, authors, abstract = extract_general_info(pdf_path)
print(f"Titre: {title}\nAuteurs: {authors}\nRésumé: {abstract}")