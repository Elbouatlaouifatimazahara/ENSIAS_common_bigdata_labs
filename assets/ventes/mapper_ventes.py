#!/usr/bin/env python3
"""Mapper : total des ventes par magasin.

Chaque ligne de purchases.txt contient 6 champs séparés par des tabulations :
    date   heure   magasin   catégorie   montant   paiement
    [0]    [1]     [2]       [3]         [4]       [5]

Le mapper doit émettre une paire clé-valeur par ligne :  magasin<TAB>montant
"""
import sys

for ligne in sys.stdin:
    champs = ligne.strip().split("\t")
    if len(champs) != 6:          # ignorer les lignes mal formées
        continue

    # À VOUS DE JOUER : complétez les deux lignes ci-dessous
    cle = None      # TODO : le magasin
    valeur = None   # TODO : le montant de l'achat

    print(f"{cle}\t{valeur}")
