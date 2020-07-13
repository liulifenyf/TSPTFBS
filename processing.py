import numpy as np
import re
import os
import pandas as pd
from tensorflow.keras.models import load_model
dir = "./"


def Matrix(file_name):
        lines = file_name.readlines()
        sample=[]; ids = []; num=0
        for line in lines:
                if (re.match('>',line.decode('utf-8')) is None) or (not len(line.decode('utf-8').strip())): 
                        value=np.zeros((201,4),dtype='float32')
                        for index,base in enumerate(line.decode('utf-8').strip()):
                                if re.match(base,'A|a'):
                                        value[index,0]=1
                                if re.match(base,'T|t'):
                                        value[index,1]=1
                                if re.match(base,'C|c'):
                                        value[index,2]=1
                                if re.match(base,'G|g'):
                                        value[index,3]=1
                        sample.append(value)
                elif re.match('>',line.decode('utf-8')): 
                        ids.append(line.decode('utf-8')[1:])
        # files.close()
        return np.array(sample), ids


def load_trained_model(model_path):
    model = load_model(model_path)
    return model


def get_all_model(dir):
    models = []
    for root,file_name,files in os.walk(dir):
        for file in files:
            if file  =="checkmodel.hdf5":
                models.append(os.path.join(root,file))
    return models

def write2file(result_array,seq_id):
    result_DF = pd.DataFrame(result_array).T
    #result_DF.pop(0)
    result_DF.columns =  ['Factor Name']+seq_id
    result_DF.to_csv('result.csv',index=False)
#     for i in range(len(seq_id)):
#         result_DF.loc[i+1].to_csv("output/"+seq_id[i][1:]+".csv",header = False) 



