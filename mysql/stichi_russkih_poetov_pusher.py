import mysql_connect
import os
# -*- coding: cp1251 -*-


db=mysql_connect.connect()

dir_read_length="../beatiful_soup/stihi_russkih_poetov/meta/"
num_files_1 = (len(os.listdir(dir_read_length)))
for i in range(0,num_files_1):#num_files_1):
    with open(dir_read_length + str(i) + ".txt", "r") as file:
        vector_=str(file.read()).split('\n')#[file.read(),file.read(),file.read(),file.read(),file.read(),file.read()]
    str_=""
    with open("../beatiful_soup/stihi_russkih_poetov/texts/" + str(i) + ".txt", "r") as file1:
        for string_ in file1:
           str_+=string_+'\n'
    #str_=str_.decode('windows-1251').encode('cp1251')
    print(vector_)
    mysql_connect.insert_poem_new(db,vector_[1],vector_[3],vector_[5],str_)
    #mysql_connect.insert_neuron_poem(db,str_,final_vector)


#mysql_connect.insert_partion(db,1,"fd","jf")
mysql_connect.disconnect(db)