import os
import sys
import pandas as pd
import numpy
from scipy.stats.stats import pearsonr

scriptdir=os.path.dirname(os.path.realpath(__file__))

numpy.warnings.filterwarnings('ignore')
numpy.set_printoptions(suppress=True)

inputfile=sys.argv[1]
if not os.path.isfile(inputfile):
   exit()
outputpath = os.path.dirname(os.path.realpath(inputfile))
outputfile="ImmunIC_{}".format(os.path.basename(inputfile))

xgboostinputfile="xgboostoutput_{}".format(os.path.basename(inputfile))
cd4={}
with open(os.path.join(outputpath,xgboostinputfile),"r") as fin:
  for i,line in enumerate(fin.readlines()):
    if i>0:
      list0=str(line).strip().split(",")
      cd4[list0[0]]=list0[1]

with open(os.path.join(scriptdir,'LM22.csv'),'r') as FIF:
       d1={}
       for i,line in enumerate(FIF.readlines()):
          if i>0:
              list0=str(line).strip().split(",")
              genename=str(list0[0]).casefold().replace("_","-")
              if genename not in d1.keys():
                   d1[genename]=str(list0[0])

lm22=pd.read_csv(os.path.join(scriptdir,'LM22.csv'), index_col=0)
lm22=lm22.sort_index()
lm22=lm22.apply(pd.to_numeric)
lm22collist=lm22.columns.values.tolist()

ma=pd.read_csv(inputfile, index_col=0)
ma=ma[~ma.index.duplicated(keep='first')]
macolist=ma.columns.values.tolist()
genelist=ma.index.tolist()

coldrop=[]
for col in macolist:
    if ma[col].sum()<500.:
        coldrop.append(col)
ma=ma.drop(columns=coldrop)

macolist=ma.columns.values.tolist()
for col in macolist:
    ma[col]=(ma[col]/ma[col].sum())*10000.
    ma[col]=ma[col].replace(numpy.nan,0.0)

genelist=ma.index.tolist()
onlyma=pd.DataFrame([pd.Series(0.0,index=ma.columns)],index=['predict'])

thelist=[]
indexnamearr=[]
for ii in range(len(genelist)):
           gene=str(genelist[ii]).casefold().replace("_","-")
           if gene not in thelist:
                thelist.append(gene)
                if gene in d1.keys():
                    onlyma=onlyma.append([ma.ix[genelist[ii],]])
                    indexnamearr=onlyma.index.values
                    indexnamearr[-1]=d1[gene]

for k in d1.keys():
            if d1[k] not in indexnamearr:
                 onlyma=onlyma.append([onlyma.ix['predict',]])
                 indexnamearr=onlyma.index.values
                 indexnamearr[-1]=d1[k]

onlyma=onlyma.drop('predict', axis=0)
onlyma=onlyma.sort_index()
onlyma=onlyma.apply(pd.to_numeric)
onlymacolist=onlyma.columns.values.tolist()

A=1580.7
B=413.
with open(os.path.join(outputpath,outputfile),"w") as fout:
      print('Cell_Index','Cell_Type','Maximum_Correlation_Coefficient','Total_Immune_Gene_Expression',sep=',',file=fout)
      onlymacolist=onlyma.columns.values.tolist()
      for col in onlymacolist:
          SUM=onlyma[col].sum()
          pvalue=1.
          celltype='Non_Immune_Cell'

          maximum_corr=-1.
          for lm22col in lm22collist:
               correlation=round(pearsonr(onlyma[col],lm22[lm22col])[0],3)
               pvaluetmp=round(pearsonr(onlyma[col],lm22[lm22col])[1],3)
               if correlation>maximum_corr:
                     maximum_corr=correlation
                     celltype=str(lm22col)
                     pvalue=pvaluetmp

          if SUM<float(-A*maximum_corr+B):
                 celltype='Non_Immune_Cell'
          else:
                if celltype=='BCN' or celltype=='BCM': celltype='B_cell'
                if celltype=='BCP': celltype='Plasma_cell'
                if 'NK' in celltype: celltype='NK_cell'
                if 'MYMO' in celltype: celltype='Monocyte'
                if 'MYMA' in celltype: celltype='Macrophage'
                if 'DC' in celltype: celltype='Dendritic_cell'
                if 'MYNU' in celltype : celltype='Neutrophil'
                if 'MYMS' in celltype or 'MYEO' in celltype: celltype='Other_Myeloid_cell'
                if 'CD' in celltype:
                    if cd4[col]=='0': celltype='CD4T_cell'
                    else: celltype='CD8T_cell'

          print(col,celltype,round(maximum_corr,2),round(SUM,1),sep=',',file=fout)
