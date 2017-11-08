#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 22:13:26 2017

vizualizace voleb 
data: vysledky_krajmesta

@author: bob
"""
from lxml import etree
import os
import pandas as pd
#from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import numpy as np
from numpy import nan
import matplotlib.pyplot as plt
import seaborn as sns

# datovy soubor 
#file_name = 'vysledky.xml' 
#base_path = os.path.dirname(os.path.realpath(__file__))
#xml_file = os.path.join(base_path, file_name)



# parse XML
tree = ET.parse("/home/bob/Documents/python_projects/volby2017/vysledky.xml")
root = tree.getroot()

df = pd.DataFrame([])
data = []


#okresu = len(root.getchildren())
#okresu = len(root.getchildren())
#
#okresu = len(root.findall('{http://www.volby.cz/ps/}KRAJ'))


# init np.array
data = np.full((15, 32), None)

# init nazvy sloupcu 
data[0,0] = "Kraj"
for strana in tree.iter(tag = "{http://www.volby.cz/ps/}STRANA"):
    data[0, int(strana.get("KSTRANA"))] = strana.get("NAZ_STR")
    # projít pouze jednu větev stromu! Nyní prochází celý strom. 
        
# init data
for elem in tree.iter(tag = "{http://www.volby.cz/ps/}KRAJ"):
    data[int(elem.get("CIS_KRAJ")), 0] = elem.get("NAZ_KRAJ")
    for subelem in elem.iter(tag = "{http://www.volby.cz/ps/}STRANA"):
        for strana in subelem.iter(tag = "{http://www.volby.cz/ps/}HODNOTY_STRANA"):
            data[int(elem.get("CIS_KRAJ")), int(subelem.get("KSTRANA"))] = float(strana.get("PROC_HLASU"))

# data to df 
df = pd.DataFrame(data)
df.columns = df.iloc[0]
df = df.reindex(df.index.drop(0))
#df.fillna(value=nan, inplace=True)
df.fillna(0, inplace=True)

# úprava datasetu - strany nad 5 procent + přejmenování col a index
df_5proc = df.iloc[:,[0,1,4,7,8,15,20,21,24,29]]
df_5proc.columns = (['Kraj', 'ODS', 'CSSD', 'STAN', 'KSCM', 'CPS', 'TOP09', 'ANO2011', 'KDU-CSL', 'SPD'])
df_5proc = df_5proc.set_index('Kraj')


# Basic correlogram
sns.pairplot(df_5proc, kind = "reg")
sns.plt.show()


# Calculate correlations
partaj = 'TOP09'
corr = df_5proc.corr()
corr1 = corr.T.sort_values(partaj, ascending=False).T
corr2 = corr1.sort_values(partaj, ascending=False)

# Heatmap
plt.yticks(rotation=0)
plt.xticks(rotation=90)
sns.heatmap(corr2, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})
sns.heatmap(corr2, center=0, square=True, linewidths=.5)


# Line Plot
partajLine = 'ANO2011'
df_5proc_sorted = df_5proc.sort_values(partajLine, ascending = False)
df_5proc_sorted.plot(style='.-')

## multiple line plot
#plt.plot(df_5proc, df_5proc.CSSD, marker='', color='olive', linewidth=2)
#plt.plot( 'x', 'y3', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
#plt.legend()





