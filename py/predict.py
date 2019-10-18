from __future__ import absolute_import
from __future__ import print_function
import numpy as np
import pandas as pd
np.random.seed(7)
from constants import *
import re
import os
import sys
import keras
from keras.models import load_model
os.environ["TF_CPP_MIN_LOG_LEVEL"]='3'
dir = "./"
if not os.path.exists("output"):
    os.mkdir("output")
def get_all_model(dir):
    models = []
    for root,dirs,files in os.walk(dir):
        for file in files:
            if file  =="checkmodel.hdf5":
                models.append(os.path.join(root,file))
    return models
def Matrix(dirs):
            files=open(dirs,'r')
            sample=[];ids = [];num=0
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
                            ids.append(line)
            files.close()
            return sample,ids
def load_trained_model(model_path):
    model = load_model(model_path)
    return model
def write2file(result_array,seq_id):
    result_DF = pd.DataFrame(result_array)
    result_DF.pop(0)
    result_DF.columns =  result_DF.loc[0]
    result_DF.drop(index = [0])
    for i in range(len(seq_id)):
        result_DF.loc[i+1].to_csv("output/"+seq_id[i][1:]+".csv",header = False) 
def main():
    print("================================================")
    result=[]
    filename = sys.argv[1]
    #get all model name
    models = get_all_model(dir)
    #change seq to array
    sample_to_predict,seq_id=Matrix(filename)
    sample_to_predict=np.array(sample_to_predict)
    print("Load %d sequences to predict!"% sample_to_predict.shape[0])
    print("it may cost a long time to calculate the result,so we suggest you to run the process with command line 'nohup python ./py/predict.py %s &'. "% filename)
    result_array = np.zeros([sample_to_predict.shape[0]+1,1])    
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
    write2file(result_array,seq_id)
    print ("Predicted!")
    
#print(pred)
if __name__ == "__main__":
    main()
