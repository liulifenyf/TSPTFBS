from __future__ import absolute_import
from __future__ import print_function
import numpy as np
import pandas as pd
import os
import re
import sys
from tensorflow import keras
from tensorflow.keras.models import load_model
np.random.seed(7)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'
modelpath = 'Models/'


def get_all_model(modelpath):
    models = []
    for root, file_name, files in os.walk(modelpath):
        for file in files:
            models.append(os.path.join(root, file))
    return models


def ONEHOT(files):
    files = open(files, 'r')
    sample=[];ids = []
    for line in files:
            if (re.match('>',line) is None) or (not len(line.strip())): 
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
                    sample.append(value)
            elif re.match('>',line): 
                    ids.append(line[1:].strip())
    files.close()
    return np.array(sample),ids


def predict(sample_to_predict, models):
    print("Load %d sequences to predict!"% sample_to_predict.shape[0])
    result_array = np.zeros([sample_to_predict.shape[0]+1,1])    
    result = []
    count = 0
    for model in models:
        model_tf = re.split('[/-]', model)[1]
        count += 1 
        print('Now loading the trained model of factor {} for predicting! this is the num {} model, totally 265 models!'.format(model_tf, count))
        one_model = load_model(model)
        pred = one_model.predict(sample_to_predict)
        result.append(model_tf)
        result.append(pred)
        result = np.array(result)
        result = np.vstack(result)
        result_array = np.concatenate((result_array, result), axis=1)
        keras.backend.clear_session()
        result = []
    return result_array[:,1:]
    

def write2file(result_array, seq_id):
    result_DF = pd.DataFrame(result_array).T
    #result_DF.pop(0)
    result_DF.columns =  ['TF Name']+seq_id
    result_DF.to_csv('result.csv',index=False)


def main():
    filename = sys.argv[1]
    sample_to_predict, seq_id = ONEHOT(filename)
    models = get_all_model(modelpath)
    result_array = predict(sample_to_predict, models)
    write2file(result_array, seq_id)


if __name__ == '__main__':
    main()
