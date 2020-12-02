# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 13:05:39 2020

@author: Usuario
"""

# Imports necesarios
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
plt.style.use('classic')
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime
from datetime import date
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os

#Cargamos la ruta en donde se encuentran los archivos de banco azteca
ruta = 'C:/Users/LENOVO T520/Documents/ERICK/BANCO AZTECA'

#Leemos las promesas de pago y las unimos 
periodos_pps = os.listdir(''+ruta+'/PROMESAS/PPS')
periodos_pps = pd.DataFrame(periodos_pps)
periodos_pps[0] = periodos_pps[0].str[4:8]
periodos_pps[0] = periodos_pps[0].map(str)
periodos_pps = periodos_pps[0].to_list()

promesas = pd.DataFrame()
for i in periodos_pps:
    promesas_ba = pd.read_csv(''+ruta+'/PROMESAS/PPS/PPS '+i+'.csv',encoding = "ISO-8859-1", engine='python')
    promesas_ba['FECHAPROM'] = datetime.strptime(i+'2020','%d%m%Y')
    promesas_ba.reset_index(drop=True,inplace=True)
    promesas.reset_index(drop=True,inplace=True)
    promesas = pd.concat([promesas,promesas_ba], ignore_index=True)
    print(i)

pps = promesas[['#FIIDCAMPANA','FNSALDOCAPITAL','FNDIA_PAGO','FICANAL']]
pps = pps.dropna()
pps = pps.drop(pps[pps['#FIIDCAMPANA'] == '#FIIDCAMPANA'].index)
pps = pps.apply(pd.to_numeric)

pps_filter = pps.loc[pps['FNSALDOCAPITAL']<40000]
pps_filter['FNDIA_PAGO'] = pps_filter['FNDIA_PAGO'].astype(str)
pps_filter['FNDIA_PAGO'] = pps_filter['FNDIA_PAGO'].str[0:1]
pps_filter = pps_filter.apply(pd.to_numeric)

pps_filter.corr()
pps_filter.describe()
pps_filter.hist()
    
x = pps_filter[['FNDIA_PAGO']]
y = pps_filter[['FNSALDOCAPITAL']]

plt.scatter(x,y)
plt.show()




















periodos_prod = os.listdir(''+ruta+'/PROMESAS/Prod')
periodos_prod = pd.DataFrame(periodos_prod)
periodos_prod[0] = periodos_prod[0].str[5:9]
periodos_prod[0] = periodos_prod[0].map(str)
periodos_prod = periodos_prod[0].to_list()

prod = pd.DataFrame()
for i in periodos_prod:
    prod_ba = pd.read_csv(''+ruta+'/PROMESAS/Prod/PROD '+i+'.csv',encoding = "ISO-8859-1", engine='python')
    prod_ba['FECHAPROM'] = datetime.strptime(i+'2020','%d%m%Y')
    prod_ba.reset_index(drop=True,inplace=True)
    prod.reset_index(drop=True,inplace=True)
    prod = pd.concat([prod,prod_ba], ignore_index=True)
    print(i)

prod2 = prod[['#FIIDCAMPANA','FISEMATRASMAX','FNSALDOCAPITAL','FITERRITORIO']]
prod2_filter = prod2.loc[prod2['FITERRITORIO']>0]


prod2_filter.corr()
prod2_filter.describe()
prod2_filter.hist()


