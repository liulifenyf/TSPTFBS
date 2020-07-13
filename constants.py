import pandas as pd
import os
sys_path = os.getcwd()
paras = pd.read_excel(sys_path+'/source/Sup_Tables.xlsx','Table S2')
columns  = list(paras.columns)
TFs = list(paras[columns[0]][2:])
f_s = list(paras[columns[3]][2:])
optimal = dict(zip(TFs,f_s))
