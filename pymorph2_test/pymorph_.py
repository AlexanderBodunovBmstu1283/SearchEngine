# -*- coding: cp1251 -*-
import os
import pymorphy2

dir_base="../buitifull_soup/stihi_russkih_poetov"
dir_texts=dir_base+"/texts"
dir_norm_texts=dir_base+"/norm_texts"
morph = pymorphy2.MorphAnalyzer()

try:
    os.makedirs(dir_norm_texts)
except:
    pass

def normal_str(input_str):
    word_list= input_str.split()
    res=[]
    for word in word_list:
        p=morph.parse(word)[0]
        res.append(p.normal_form)
    return ' '.join(res)

num_files_1 = (len(os.listdir(dir_texts)))-1

for filename in range(0,num_files_1):
    filename=str(filename)
    #filename="pymorph_"
    file_source = open(dir_texts+filename+".txt")
    file_res=open(dir_norm_texts+filename+"2.txt","w")
    for str in file_source:
        file_res.writelines(normal_str(str)+"\n")
    print("Файл "+filename+ ".txt сформирован в исходной директории!")