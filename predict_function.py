from __future__ import absolute_import
from __future__ import print_function
import numpy as np
import pandas as pd
from constants import *
from processing import *
import os
from tensorflow import keras

np.random.seed(7)
os.environ["TF_CPP_MIN_LOG_LEVEL"]='3'


def predict(sample_to_predict):
    #change seq to array
    print("Load %d sequences to predict!"% sample_to_predict.shape[0])
    #print("it may cost a long time to calculate the result,so we suggest you to run the process with command line 'nohup python ./py/predict.py %s &'. "% filename)
    result_array = np.zeros([sample_to_predict.shape[0]+1,1])    
    result = []
    for model in models:
        model_tf = model.split('/')
        if int(model_tf[-2]) == optimal[model_tf[-3]]:
            one_model = load_trained_model(model)
            pred = one_model.predict(sample_to_predict)
            result.append(model_tf[-3])
            result.append(pred)
            result = np.array(result)
            result = np.vstack(result)
            result_array = np.concatenate((result_array,result),axis=1)
            keras.backend.clear_session()
            result=[]
    return result_array[:,1:]
    
models = get_all_model(dir)
def main(seq2pre, ids):
    result_array = predict(seq2pre)
    write2file(result_array,ids)