import os
import sys
import pandas as pd
import pickle
import numpy
import xgboost as xgb
from xgboost import XGBClassifier

def filtergene(inputfile,genescoreinputfile):
  with open(inputfile,'r') as MFN:
    with open(genescoreinputfile,'r') as FIF:
       d1={}
       for line in FIF:
          list0=str(line).strip().split(" ")
          genename=str(list0[0].casefold()).replace("_","-")
          if genename not in d1.keys():
                d1[genename]=str(list0[0])

       ma1 = pd.read_csv(MFN, index_col = 0)
       ma1colist=ma1.columns.values.tolist()
       for col in ma1colist:
               ma1[col]=ma1[col].astype(float)
               ma1[col]=(ma1[col]/ma1[col].sum())*10000.
               ma1[col]=numpy.log(ma1[col]+1.)
               ma1[col]=ma1[col].replace(numpy.nan,0.0)
      
       genelist=ma1.index.tolist()
       onlyma=pd.DataFrame([pd.Series(0.0,index=ma1.columns)],index=['predict'])

       thelist=[]
       indexnamearr=[]
       for ii in range(len(genelist)):
           gene=(str(genelist[ii])).casefold().replace("_","-")
           if gene not in thelist:
                thelist.append(gene)
                if gene in d1.keys():
                    onlyma=onlyma.append([ma1.ix[genelist[ii],]])
                    indexnamearr=onlyma.index.values
                    indexnamearr[-1]=d1[gene]
  
       for k in d1.keys():
            if d1[k] not in indexnamearr:
                 onlyma=onlyma.append([onlyma.ix['predict',]])
                 indexnamearr=onlyma.index.values
                 indexnamearr[-1]=d1[k]

       sortonlyma=onlyma.sort_index()
       cellname=list(sortonlyma.columns)
       df1 = sortonlyma.T
       df2 = df1.loc[:,'predict']
       df2 = pd.Series(df2, index = df2.index)
       df3 = df1.drop('predict', axis = 1)
       df3 = df3.apply(pd.to_numeric)
 
       return df3, df2, cellname, sortonlyma
