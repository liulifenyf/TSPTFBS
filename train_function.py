from __future__ import absolute_import
from __future__ import print_function
import numpy as np
np.random.seed(7)
import re
import sys
import random
import time
import keras
from keras.models import Sequential,model_from_json
from keras.callbacks import EarlyStopping,ModelCheckpoint 
from keras.layers import Dense, Dropout, Activation, Flatten,Conv1D, MaxPooling1D,Merge
from keras.optimizers import SGD

np.set_printoptions(threshold=np.nan)

# make ont-hot matrix
def Matrix(dirs,label_value,num_need):
        files=open(dirs,'r')
        sample=[];label=[];num=0
        for line in files:
                if re.match('>',line) is None:
                        value=np.zeros((201,4),dtype='float32')
                        for index,base in enumerate(line.strip()):
                                if re.match(base,'A|a'):
                                        value[index,0]=1
                                if re.match(base,'T|t'):
                                        value[index,1]=1
                                if re.match(base,'C|c'):
                                        value[index,2]=1
                                if re.match(base,'G|g'):
                                        value[index,3]=1
                #       value.reshape([201,4,1])
                        sample.append(value)
                        label.append(label_value)
                else:
                        num+=1
                        if num<=num_need:
                                continue
                        else:
                                break
        files.close()
        return sample,label


# create train and test set
def create_train_and_test_data(pos_sample, pos_label, neg_sample, neg_label, train_size):
	pos_train=pos_matrix[0:train_size]
	pos_label_train=pos_label[0:train_size]
    pos_train.extend(neg_train[0:train_size])
	input_train=np.array(pos_train,dtype='float32')
	pos_label_train.extend(neg_label_train[0:train_size])
	input_label_train=np.array(pos_label_train,dtype='int32')
	print (np.shape(input_train))
	print (np.shape(input_label_train))
    #shuffle the input data
	shuffle_index=np.arange(len(input_train))
	np.random.shuffle(shuffle_index)
	#gain the train database of model
	input_train=input_train[shuffle_index]
	input_label_train=input_label_train[shuffle_index]
	#gain the test database of model
	pos_test=pos_matrix[train_size:]
	neg_test=neg_train[train_size:]
	pos_test.extend(neg_test)
	input_test=np.array(pos_test,dtype='float32')
	pos_label_test=pos_label[train_size:]
	neg_label_test=neg_label_train[train_size:]
	pos_label_test.extend(neg_label_test)
	input_label_test=np.array(pos_label_test,dtype='int32')
    return input_train, input_test, input_label_train, input_label_test


# create model
def Model(filter_num, filer_len):
    model=Sequential()
	model.add(Conv1D(filters=int(filter_num),kernel_size=int(filter_len),padding='same', activation='relu', input_shape=(201,4)))
	model.add(MaxPooling1D(pool_size=3))
	model.add(Flatten())
	model.add(Dense(100,activation='relu'))
	model.add(Dropout(0.3))
	model.add(Dense(50,activation='relu'))
	model.add(Dropout(0.3))
	model.add(Dense(1))
	model.add(Activation('sigmoid'))
    return model


def main(dir_pos_file,dir_neg_file,dir_out,num_epoch,filter_num,filter_len):
    start = time.time()
    # create file to sumthe process and result
    out=open(dir_out+'/result.txt','w')
    #read file and create positive and negitive data
	f=open(dir_pos_file,'r')
	pos_num=f.read().count('>')
	f.close()
	train_size=int(pos_num*0.8)
    pos_matrix,pos_label=Matrix(dirs=dir_pos_file,label_value=1,num_need=pos_num)
    neg_train,neg_label_train=Matrix(dirs=dir_neg_file,label_value=0,num_need=pos_num)
    input_train, input_test, input_label_train, input_label_test = create_train_and_test_data(pos_matrix, pos_label, neg_train, neg_label_train, train_size)
    out.write ('The number of train datas: %s\n' % len(input_train))
	out.write ('The number of test datas: %s\n' % len(input_test))
    # train_and test_models
    model = Model()
    checkpoint = ModelCheckpoint(filepath=dir_out+'/checkmodel.hdf5', save_best_only=True,monitor='val_acc',mode='max')
	model.compile(loss='binary_crossentropy',optimizer=sgd,metrics=['accuracy'])
	early_stopping =EarlyStopping(monitor='val_loss', patience=2)
	result=model.fit(input_train,input_label_train,batch_size=128,epochs=num_epoch,shuffle=True,validation_data=(input_test,input_label_test), callbacks=[checkpoint]) 
	end = time.time()
    all_time=end-start
    val_acc_value=0;epoch_value=0;acc_value=0
	out.write('epoch\ttrain_loss\ttrain_acc\tval_loss\tval_acc\n')
	for epochs in range(len(result.epoch)):
		out.write('%s\t%s\t%s\t%s\t%s\n' %(result.epoch[epochs],result.history['loss'][epochs],result.history['acc'][epochs],result.history['val_loss'][epochs],result.history['val_acc'][epochs]))
		if float(result.history['val_acc'][epochs])>=val_acc_value:
			val_acc_value=float(result.history['val_acc'][epochs])
			epoch_value=result.epoch[epochs]
			acc_value=result.history['acc'][epochs]
	out.write('\nThe optimal condition:\n')
	out.write('\tepoch: %s\n' % epoch_value)
	out.write('\ttrain_acc: %s\n' % acc_value)
	out.write('\tval_acc: %s\n' % val_acc_value)
	out.write('\tusing time: %s\n' % all_time)
	out.close()

