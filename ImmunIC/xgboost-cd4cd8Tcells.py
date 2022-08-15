import os
import sys
import pandas as pd
import xgboost as xgb
from xgboost import XGBClassifier
import pickle
from genefilter import *

scriptdir=os.path.dirname(os.path.realpath(__file__))

numpy.warnings.filterwarnings('ignore')
numpy.set_printoptions(suppress=True)

inputfile=sys.argv[1]
if not os.path.isfile(inputfile):
   exit()
outputpath = os.path.dirname(os.path.realpath(inputfile))
outputfile = 'xgboostoutput_{}'.format(os.path.basename(inputfile))
genescoreinputfile=os.path.join(scriptdir,'cd4cd8Tcellmodel-genescore.txt')
model=os.path.join(scriptdir,'cd4cd8Tcellmodel.pkl')
       
A, B, cellname, C=filtergene(inputfile,genescoreinputfile) 
pickled_model=pickle.load(open(model,'rb'))
PRED=pickled_model.predict(A)
PROB=pickled_model.predict_proba(A)

with open(os.path.join(outputpath,outputfile),"w") as fout:
    print('Cell_Index','CD4T','CD4T_probability',sep=',',file=fout)
    for i in range(len(PRED)):
        print(cellname[i],PRED[i],PROB[i][0],sep=',',file=fout)
