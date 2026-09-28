#!/usr/bin/env python3
"""Reducer : additionne les montants de chaque clé.

Entrée : paires cle<TAB>montant, TRIÉES par clé
         (le tri est garanti par la phase shuffle and sort de Hadoop)
Sortie : cle<TAB>total
"""
import sys

cle_courante = None
total = 0.0

for ligne in sys.stdin:
    try:
        cle, montant = ligne.strip().split("\t")
        montant = float(montant)
    except ValueError:
        continue                              # ignorer les lignes invalides
    if cle == cle_courante:
        total += montant                      # même clé : on cumule
    else:
        if cle_courante is not None:          # nouvelle clé : on émet la précédente
            print(f"{cle_courante}\t{total:.2f}")
        cle_courante = cle
        total = montant

if cle_courante is not None:                  # ne pas oublier la dernière clé
    print(f"{cle_courante}\t{total:.2f}")
