#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import decode
import string






def file_reader(file_name):
    our_string=[]
    with open(file_name, "r") as file:
        for line in file:
            line = line.replace("\n", "").lower()
            print(line)
            our_string.append(line)
    return our_string


def find_root(our_string):
    print('\n','Ищем корни','\n')
    pre_s=[]
    with open("pre_changed.txt", "r") as file:
        for line in file:
            line = line.replace("\n", "")
            pre_s.append(line)
    for j in range (len(our_string)-1):
        for i in pre_s:
                if (our_string[j].startswith(i)):
                    print(i)#, end="")
                    suspected_root=our_string[j][len(i):].zfill(4)[:4]
                    if suspected_root!="0000":
                        our_string.append(suspected_root)
        our_string[j]=our_string[j].zfill(4)[:4]
    print("\n",pre_s)
    for i in our_string:
        print("\n",i)
    return sorted(our_string)

def file_writer(name,our_string):
    with open(name, "w") as file:
        for i in our_string:
            file.write(i + "\n")

#***********************************************************


file_writer("out.txt",find_root(file_reader("our_word.txt")))
file_writer("out_2.txt",find_root(file_reader("our_word_2.txt")))
file_writer("out_3.txt",find_root(file_reader("our_word_3.txt")))
file_writer("out_4.txt",find_root(file_reader("our_word_4.txt")))

file_writer("poems_same_roots.txt",find_root(file_reader("all_poems.txt")))




