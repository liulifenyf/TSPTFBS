from __future__ import absolute_import
from __future__ import print_function
import numpy as np
import re
import os
import sys
import random
import time
from sklearn.model_selection import train_test_split
from keras.models import Sequential,model_from_json
from keras.callbacks import EarlyStopping,ModelCheckpoint 
from keras.layers import Dense, Dropout, Activation, Flatten,Conv1D, MaxPooling1D
from keras.optimizers import SGD

np.set_printoptions(threshold=sys.maxsize)
output = 'output'
models='Trained_models'

# create a file folder for saving output files
if not os.path.exists(output):
    os.mkdir(output)
    print('{0} creat successful!'.format(output))
else:
    print('{0} has been exists.'.format(output))

# create a file folder for saving trained models 
if not os.path.exists(models):
    os.mkdir(models)
    print('{0} creat successful!'.format(models))
else:
    print('{0} has been exists.'.format(models))

# Create the ont-hot matrix
def Matrix(dirs, label_value, num_need):
    files = open(dirs, 'r')
    sample = []
    label = []
    num = 0
    for line in files:
        if re.match('>', line) is None:
            value = np.zeros((201, 4), dtype='float32')
            for index, base in enumerate(line.strip()):
                if re.match(base, 'A|a'):
                    value[index, 0] = 1
                if re.match(base, 'T|t'):
                    value[index, 1] = 1
                if re.match(base, 'C|c'):
                    value[index, 2] = 1
                if re.match(base, 'G|g'):
                    value[index, 3] = 1
            sample.append(value)
            label.append(label_value)
        else:
            num += 1
            if num <= num_need:
                continue
            else:
                break
    files.close()
    return np.array(sample), np.array(label).reshape(
        [np.array(sample).shape[0], 1])


# create training and testing datasets
def CTTD(pos_sample, pos_label, neg_sample, neg_label):
    X = np.row_stack((pos_sample, neg_sample))
    Y = np.row_stack((pos_label, neg_label))
    input_train, input_test, input_label_train, input_label_test = train_test_split(
        X, Y, train_size=0.8, random_state=2020)
    return input_train, input_test, input_label_train, input_label_test


# Model construction
def Model(filter_num, filter_len):
    model = Sequential()
    model.add(
        Conv1D(filters=int(filter_num),
               kernel_size=int(filter_len),
               padding='same',
               activation='relu',
               input_shape=(201, 4)))
    model.add(MaxPooling1D(pool_size=3))
    model.add(Flatten())
    model.add(Dense(100, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(50, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    return model


def train(pos_file,neg_file,filter_len,num_epoch=100,filter_num=16):
    start = time.time()
    # create a file to record training results
    out = open(
        output +
        '/{}-result-{}.txt'.format(re.split('[/.]', pos_file)[-2], filter_len),
        'w')
    #read files and create positive and negitive datasets
    f = open(pos_file, 'r')
    pos_num = f.read().count('>')
    f.close()
    pos_matrix, pos_label = Matrix(dirs=pos_file,
                                   label_value=1,
                                   num_need=pos_num)
    neg_train, neg_label_train = Matrix(dirs=neg_file,
                                        label_value=0,
                                        num_need=pos_num)
    input_train, input_test, input_label_train, input_label_test = CTTD(
        pos_matrix, pos_label, neg_train, neg_label_train)
    out.write('The number of training samples: %s\n' % len(input_train))
    out.write('The number of testing samples: %s\n' % len(input_test))
    # train and test model
    model = Model(filter_num, filter_len)
    sgd = SGD(lr=0.001, decay=1e-5, momentum=0.9, nesterov=True)
    checkpoint = ModelCheckpoint(
        filepath=models +
        '/{}-model-{}.hdf5'.format(re.split('[/.]', pos_file)[-2], filter_len),
        save_best_only=True,
        monitor='val_accuracy',
        mode='max')
    model.compile(loss='binary_crossentropy',
                  optimizer=sgd,
                  metrics=['accuracy'])
    early_stopping = EarlyStopping(monitor='val_loss', patience=2)
    result = model.fit(input_train,
                       input_label_train,
                       batch_size=128,
                       epochs=num_epoch,
                       shuffle=True,
                       verbose=0,
                       validation_data=(input_test, input_label_test),
                       callbacks=[checkpoint])
    end = time.time()
    training_time = end - start
    val_acc_value = 0
    out.write('epoch\ttrain_loss\ttrain_acc\tval_loss\tval_acc\n')
    for epochs in range(len(result.epoch)):
        if float(result.history['val_accuracy'][epochs]) >= val_acc_value:
            val_acc_value = float(result.history['val_accuracy'][epochs])
            epoch_value = result.epoch[epochs]
            acc_value = result.history['accuracy'][epochs]
    out.write('\nThe optimal condition:\n')
    out.write('\tepoch: %s\n' % epoch_value)
    out.write('\ttrain_acc: %s\n' % acc_value)
    out.write('\tval_acc: %s\n' % val_acc_value)
    out.write('\tusing time: %s\n' % training_time)
    out.close()


# grid search for the optimal filter length
def grid_train(pos_file, neg_file):
    for filter_len in range(11, 22, 2):
        train(pos_file, neg_file, filter_len=filter_len)


def main():
    pos_file = 'Example/ABF2.fasta'
    neg_file = 'Example/neg.fasta'
    grid_train(pos_file, neg_file)
	'''
	Here we take ABF2 as an example to show the training process. For other users, just change pos_file to be your desired fasta file name.
    '''


if __name__ == "__main__":
	main()
