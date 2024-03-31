# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 17:11:17 2019

@author: ngtrk
"""
from KnowledgeBase import KnowledgeBase

def read_file(file):
    try:
        with open(file, "r") as f:
            alpha = f.readline().rstrip("\n")
            length_KB = int(f.readline())
            KB = KnowledgeBase()
            for _ in range(length_KB):
                KB.add_sentence(f.readline().rstrip("\n"))
        return KB, alpha
    except IOError:
        print("Could not open file!!!")
        return None, None

def write_file(f, lst):
    f.write(str(len(lst)) + "\n")
    for item in lst:
        f.write(" OR ".join(item) + "\n")

        