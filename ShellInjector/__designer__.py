import os
import random
list_designer = []
designer1 = """\33[1m\33[96m
  __            ___    o
 (_ |_  _  |  |  | __  |  _  _ _|_ _  __
 __)| |(/_ |  | _|_| |_| (/_(_  |_(_) |\33[0m
"""

designer2 = """\33[1m\33[96m
 +-++-++-++-++-++-++-++-++-++-++-++-++-+
 |s||h||e||l||l||i||n||j||e||c||t||o||r|
 +-++-++-++-++-++-++-++-++-++-++-++-++-+\33[0m
"""

designer3 = """\33[1m\33[96m
 𝕊𝕙𝕖𝕝𝕝𝕀𝕟𝕛𝕖𝕔𝕥𝕠𝕣\33[0m
"""
list_designer.append(designer1)
list_designer.append(designer2)
list_designer.append(designer3)
def __choices__():
    os.system("clear")
    for __logo__ in random.choices(list_designer):
        print (__logo__)
#__choices__()