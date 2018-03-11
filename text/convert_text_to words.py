import re


def convert_text_to_words(name):
    voc = []
    with open(name,"r") as file:
        for line in file:
            line = str(re.sub(r"[,.!?-_()#@$%&*+=/1234567890]", "", line)).replace("\n", "").split(" ")
            print(line)
            for i in line:
                if i!="":
                    voc.append(i)
    return voc



def write_words_to_file(name,words):
    with open(name,"w") as file:
        for i in words:
            file.write(i + "\n")

write_words_to_file("our_word_4.txt",convert_text_to_words("row_interpol.txt"))
