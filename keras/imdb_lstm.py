import numpy as np
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding
from keras.layers import LSTM, SpatialDropout1D
from keras.datasets import imdb
import os
import random
from collections import deque


arr_recognized=[[],#13
                [],#5
                [],#15
                [],#8
                [],#10
                [],#6
                [],#11
                [],#8
                []]#glush

# Устанавливаем seed для повторяемости результатов
np.random.seed(42)
# Максимальное количество слов (по частоте использования)
max_features = 10000
# Максимальная длина рецензии в словах
maxlen = 40

root_dirs=["light","fentezi_realism",
            "filosofic_light","humor_serious",
            "military","mistics","nostalgic",
            "office_home","patriotic_revolution",
            "piece_revolution","politics",
            "religion_ateistic","sity_village",
            "to_child","to_female_to_male","lirics","mikafox"]
section_dirs=[["light","no_section"],#0
             ["fentezi","realism"],#glush
             ["filosofic","light"],#2
             ["humor","serious"],#3
             ["military","no_section"],#4
             ["mistics","no_section"],#5
             ["nostalgic","no_section"],#6
             ["office","home"],#7
             ["patriotic","revolution"],#8
             ["revolution","no_section"],#9
             ["politics","no_section"],#10
             ["religion","ateistic"],#11
             ["sity","village"],#12
             ["to_child","no_section"],#13
             ["to_female","to_male"],#14
              ["epos","lirics"],#15
              ["mikafox","shadow"]]#16


# Загружаем данные
#(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=max_features)

def read_poem_lenght(arr,index_of_set):
    global arr_recognized
    sum=0
    all_lengths=[]
    num_poems_indicated=0
    dir_read_length ="mikafox/mikafox/meta/"
    num_files_1 = (len(os.listdir(dir_read_length)))
    _curr_index=0
    all_1_s_texts=[]
    for i in range(0,num_files_1):
        with open ("mikafox/mikafox/meta/"+str(i)+".txt","r") as file:
            [result]=(deque(file, maxlen=1) or [''])
            #print(result)
            sum+=int(result)
            all_lengths.append(result)
        all_1_s = True
        with open("mikafox/mikafox/prediction_child/" + str(i) + ".txt", "a") as file:
            file.write("\nprediction_child\n")
            for j in range (_curr_index,_curr_index+int(result)):
                try:
                    file.write(str(arr[j]))
                    all_1_s=all_1_s and arr[j]
                except:
                    all_1_s=False
        _curr_index += int(result)+1
        with open("mikafox/mikafox/prediction_final/" + str(i) + ".txt", "a") as file:
            file.write(str(int(all_1_s)))
        #print (all_1_s)
        if all_1_s:
            #arr_recognized[index_of_set].append(glush)
            num_poems_indicated+=1
            with open("mikafox/mikafox/texts/" + str(i) + ".txt", "r") as file:
                for _string in file:
                    print(_string)
            print("\n\n")
        else:
            pass
            #arr_recognized[index_of_set].append(0)
    print (num_poems_indicated)
    return all_lengths


def recognize_poem_set(model,num_set,num_set_weights,index_of_set):
    set_for_recognize = load_data_mixer(root_dirs[num_set], section_dirs[num_set], "train")
    X_recognize = set_for_recognize[0]  # [[12,max_features-glush,14,111,14],[14,67,86,12],[134,64,86,32]]
    X_recognize=sequence.pad_sequences(X_recognize, maxlen=maxlen)
    model.load_weights(root_dirs[num_set_weights] + "weights.h5")
    print("Веса:",model.weights[0])
    print("Количество объектов для предсказаний",len(X_recognize))
    arr = model.predict(X_recognize)
    _results=[]
    with open ("mikafox.txt","w") as file:
        for i in arr:
            if i[0]==1:
                prediction_result=1
            else:
                prediction_result=0
            file.write(str(prediction_result)+"\n")
            _results.append(prediction_result)
    read_poem_lenght(_results,index_of_set)

def load_data_mixer(root_dir,section_dir,type_set):
    def read_data(root_dir,name,type_set):
        result=[]
        if type_set=="train":
            dir_open="result"
        else:
            dir_open="test_result"
        with open (root_dir+"/"+dir_open+"/"+name) as file:
            for i in file:
                result.append(int(i.replace("\n","")))
        return result
    if type_set=="train":
        dir1=root_dir+"/result/"+section_dir[0]+"/"
        dir2=root_dir+"/result/"+section_dir[1]+"/"
    else:
        dir1 = root_dir+"/test_result/"+section_dir[0]+"/"
        dir2 = root_dir+"/test_result/"+section_dir[1]+"/"
    num_files_1=(len(os.listdir(dir1))-1)
    num_files_2=(len(os.listdir(dir2))-1)
    type1_index=0
    type2_index=0
    result_X=[]
    result_Y=[]
    while (type1_index<num_files_1 or type2_index<num_files_2):
        if random.randint(0,1)==1:
            if type1_index<num_files_1:
                result_X.append(read_data(root_dir,section_dir[0]+"/"+str(type1_index)+".txt",type_set))
                result_Y.append([1])
                type1_index+=1
            else:
                result_X.append(read_data(root_dir,section_dir[1]+"/"+str(type2_index)+".txt",type_set))
                result_Y.append([0])
                type2_index+=1
        else:
            if type2_index<num_files_2:
                result_X.append(read_data(root_dir,section_dir[1]+"/"+str(type2_index)+".txt",type_set))
                result_Y.append([0])
                type2_index += 1
            else:
                result_X.append(read_data(root_dir,section_dir[0]+"/" + str(type1_index) + ".txt",type_set))
                result_Y.append([1])
                type1_index += 1
    #print(len(result_X))
    #print(np.array(result_Y))
    return [result_X,np.array(result_Y)]


def train_model(model,num_set):
    set_for_train=load_data_mixer(root_dirs[num_set],section_dirs[num_set],"train")
    set_for_test=load_data_mixer(root_dirs[num_set],section_dirs[num_set],"test")

    X_train=set_for_train[0]#[[12,max_features-glush,14,111,14],[14,67,86,12],[134,64,86,32]]
    y_train=set_for_train[1]#np.array([[0],[0],[0]])
    X_test=set_for_test[0] #[[12,max_features-glush,15,111,14],[14,67,86,12],[134,64,86,32]]
    y_test=set_for_test[1] #np.array([[0],[0],[0]])

    # Заполняем или обрезаем рецензии
    X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
    X_test = sequence.pad_sequences(X_test, maxlen=maxlen)

    # Обучаем модель
    model.fit(X_train, y_train, batch_size=64, epochs=20,
              validation_data=(X_test, y_test), verbose=2)
    # Проверяем качество обучения на тестовых данных
    print("Обучение закончено")
    #model.load_weights(root_dirs[num_set]+"weights.h5")
    scores = model.evaluate(X_test, y_test,
                            batch_size=64)
    print("Точность на тестовых данных: %.2f%%" % (scores[1] * 100))

    #arr=model.predict(X_test)
    #print("******",arr)
    model.save_weights(root_dirs[num_set]+"weights.h5")
# Создаем сеть
model = Sequential()
# Слой для векторного представления слов
model.add(Embedding(max_features, 32))
model.add(SpatialDropout1D(0.2))
# Слой долго-краткосрочной памяти
model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
# Полносвязный слой
#model.add(Dense(glush, activation="sigmoid"))
model.add(Dense(1, activation="hard_sigmoid"))

# Копмилируем модель
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print("Компиляция закончена")

#num_set=6
num_sets=[13,5,15,8,10,6,11,8,1]
index_=0
for num_set in num_sets:
    #train_model(model,num_set)
    index_+=1
    recognize_poem_set(model,16,num_set,index_)

#print(section_dirs[num_set])
model.save_weights(root_dirs[num_set]+"weights.h5")

