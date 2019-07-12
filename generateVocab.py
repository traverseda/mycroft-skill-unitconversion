"""Generates vocabulary from pint definition
"""

import pint
ureg = pint.UnitRegistry()

with open("vocab/en-us/unit.entity","w+") as voc:
    for key,value in ureg._units.items():
        key=key.replace("_"," ")
        voc.write(key+"\n")

with open("vocab/en-us/prefix.entity","w+") as voc:
    for key,value in ureg._prefixes.items():
        key=key.replace("_"," ")
        voc.write(key+"\n")
