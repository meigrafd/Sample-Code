#!/usr/bin/python2
# -*- coding: utf-8 -*-


def translate(text):
    new_text=""
    for char in text:
        if translation_table.get(char):
            new_text += translation_table.get(char)
        else:
            new_text += char
    return new_text

translation_table={"Ä":"Ae", "ä":"ae", "Ö":'Oe', "ö":"oe", "Ü":"Ue", "ü":"ue", "ß":"ss"}
print translate("Österreich ist äusserst fußlastig")
