# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 10:45:29 2020

@author: Usuario
"""

import pyodbc
import pandas as pd
import numpy as np
import functools as ft 
import csv
import seaborn as sns
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os

ruta = "C:/Users/LENOVO T520/Documents/ERICK/BANCO AZTECA/"
mes_act = 'Noviembre2020'


periodos_promesas = os.listdir(''+ruta+'/PROMESAS PAGO')
periodos_promesas = pd.DataFrame(periodos_promesas)
periodos_promesas[0] = periodos_promesas[0].str[14:22]
periodos_promesas[0] = periodos_promesas[0].map(str)
periodos_promesas = periodos_promesas[0].to_list()


promesas_pago = pd.DataFrame()
for i in periodos_promesas:
    promesas = pd.read_csv(''+ruta+'PROMESAS PAGO/Prom_Pago_Exi_'+i+'.csv')
    promesas = promesas[['FCEMPNUMCORTE','FDFECHAGENPROMESA','FDFECHAPROMESA','FIIDPERIODO','FNMONTOPROMETIDO',	'FNMONTOPAGADO','FDFECHAABONO',	'FNMONTOREQUERIDO',	'CAMPANAID','CAMPANA',	'FNSCOMPROMISO']]
    promesas['FECHA'] = pd.to_datetime(i)
    promesas['FECHA']=promesas['FECHA'].dt.strftime('%Y/%m/%d')
    promesas_pago.reset_index(drop=True, inplace=True)
    promesas.reset_index(drop=True, inplace=True)
    promesas_pago = pd.concat([promesas_pago, promesas], ignore_index=True)
    print(i)
promesas_pago.drop_duplicates(subset=['FCEMPNUMCORTE','FDFECHAGENPROMESA','FDFECHAPROMESA','FIIDPERIODO','FNMONTOPROMETIDO',	'FNMONTOPAGADO','FDFECHAABONO',	'FNMONTOREQUERIDO',	'CAMPANAID','CAMPANA',	'FNSCOMPROMISO'],keep=False,inplace=True)



###################################################TABLAS DINAMICAS###################################################

#Comenzamos obteniendo promedio de promesas de pago
promesa_promedio = pd.pivot_table(promesas_pago, index=['FECHA','CAMPANAID'], values=['FNMONTOPROMETIDO'], aggfunc=np.mean, fill_value=0)

#Pagos realizados
pagos_realizados = promesas_pago.loc[promesas_pago['FNMONTOPAGADO'] > 50]
vol_pagos = pd.pivot_table(pagos_realizados, index=['FECHA','CAMPANAID'], values=['FNMONTOPROMETIDO'], aggfunc='count' , fill_value=0)

#Pago promedio
pago_promedio = pd.pivot_table(pagos_realizados, index=['FECHA','CAMPANAID'], values=['FNMONTOPAGADO'], aggfunc=np.mean, fill_value=0)

#Por fecha de cuando se asigno la promesa
fecha_promesa_prom = pd.pivot_table(pagos_realizados, index=['FDFECHAABONO','CAMPANAID'], values=['FNMONTOPROMETIDO'], aggfunc=np.mean, fill_value=0)
fecha_promesa_prom = pd.DataFrame(fecha_promesa_prom.to_records())

#Eficiencia promesas contra pagado
promesas_realizadas_fecha = pd.pivot_table(promesas_pago, index=['FDFECHAPROMESA','CAMPANAID'], values=['FNMONTOPROMETIDO'], aggfunc=np.sum, fill_value=0)
pagos_realizados_fecha = pd.pivot_table(pagos_realizados, index=['FDFECHAPROMESA','CAMPANAID'], values=['FNMONTOPAGADO'], aggfunc=np.sum, fill_value=0)

eficiencia_pagos_promesas = pd.merge(promesas_realizadas_fecha, pagos_realizados_fecha, on=['FDFECHAPROMESA','CAMPANAID'], how='left')
eficiencia_pagos_promesas['EFICIENCIA'] = eficiencia_pagos_promesas['FNMONTOPAGADO']/eficiencia_pagos_promesas['FNMONTOPROMETIDO']

pivote_eficiencia_pagos_promesas = pd.pivot_table(eficiencia_pagos_promesas, index=['FDFECHAPROMESA','CAMPANAID'], values=['EFICIENCIA'], aggfunc=np.sum, fill_value=0)









writer = pd.ExcelWriter(''+ruta+''+mes_act+'/Reporte azteca '+mes_act+'.xlsx', engine='xlsxwriter')
promesa_promedio.to_excel(writer, sheet_name='PromesaPromedio')
pago_promedio.to_excel(writer, sheet_name='PagoPromedio')
vol_pagos.to_excel(writer, sheet_name='VolumenPagos')
pivote_eficiencia_pagos_promesas.to_excel(writer, sheet_name='EficienciaPagoProm')
writer.save()
writer.close()






pagos = pagos_realizados[['CAMPANAID','FNMONTOPAGADO','FNMONTOPROMETIDO']]

pivote = pd.pivot_table(pagos,index=['CAMPANAID'],values = ['FNMONTOPAGADO','FNMONTOPROMETIDO'],aggfunc=np.sum)

pagos.corr()
z = pagos.describe()
pagos.hist()

x=pagos[['CAMPANAID']]
y=pagos[['FNMONTOPAGADO']]

plt.scatter(x,y)
plt.show()


















