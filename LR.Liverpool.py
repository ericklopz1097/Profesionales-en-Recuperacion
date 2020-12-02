# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 16:32:08 2020

@author: Erick
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
from scipy import stats

ruta = 'C:/Users/LENOVO T520/Documents/ERICK/LIVERPOOL'

#Leemos los pagos
arch_liv_pag = os.listdir(''+ruta+'/PAGOS')
dtype_dic = {'Cuenta':str}
pagos_liv = pd.DataFrame()
for i in arch_liv_pag:
    file_name = pd.read_excel(''+ruta+'/PAGOS/'+i+'',dtype=dtype_dic)
    file_name['Division'] = i[12:-5]
    pagos_liv = pd.concat([pagos_liv,file_name],ignore_index=True)
    print(i)
pagos_liv = pagos_liv[['Cuenta','Fecha pago','Fecha Posteo','monto','Descripcion','Division']]

pagos_liv['Fecha pago'] = pd.to_datetime(pagos_liv['Fecha pago'])
pagos_liv['Dia semana'] = [x.weekday() for x in pagos_liv['Fecha pago']] 
pagos_liv['Dia mes'] = pagos_liv['Fecha pago'].dt.day
pagos_liv['Mes'] = pagos_liv['Fecha pago'].dt.month

pivot_pagos = pd.pivot_table(pagos_liv, index=['Mes','Dia semana','Cuenta','Division'], values=['monto'], aggfunc=np.sum,fill_value=(0))
pivot_pagos = pd.DataFrame(pivot_pagos.to_records())




#Leemos asignaciones
arch_liv_asig = os.listdir(''+ruta+'/ASIGNACION/ASIGNACIONESCSV')
dtype_dic = {'# CUENTA':str}
asignaciones_liv = pd.DataFrame()
for j in arch_liv_asig:
    asignacion = pd.read_csv(''+ruta+'/ASIGNACION/ASIGNACIONESCSV/'+j+'',encoding = "ISO-8859-1", engine='python',dtype=dtype_dic) 
    asignaciones_liv = pd.concat([asignaciones_liv,asignacion],ignore_index=True)
    print(j)
asignacion_liv2 = asignaciones_liv[['ID AGENCIA','# CUENTA','CIUDAD','ESTADO','CODIGO POSTAL','LADA CASA','TELEFONO CASA','LADA CELULAR','TELEFONO CELULAR','CURP / RFC','SALDO ABOGADO','SALDO ACTUAL','SALDO DISPOSICION','FECHA ULTIMO PAGO','IMPORTE ULTIMO PAGO','FECHA APERTURA','STATUS PP','FECHA CREACION PP','FECHA VENCIMIENTO PP','IMPORTE PP','ULT ACCION','ULT RESULTADO','FECHA ULT ACTIVIDAD','ALMACEN','ORGANIZACION','LOGO','DIA DE CORTE','BLOQUEO 1','FECHA BLOQUEO 1','BLOQUEO 2','FECHA BLOQUEO 2','NIVEL DE MOROSIDAD','STATUS DE CASTIGO','FECHA DE CASTIGO','FECHA ASIGNACION AGENCIA','FILA','ULT ACTUALIZACION SISTEMA','NUM DE TC DEL CLIENTE','2DA CUENTA DEL CLIENTE','NIVEL DE MORA 2DA CUENTA DEL CLIENTE']]
asignacion_liv2['FECHA ASIGNACION AGENCIA'] = pd.to_datetime(asignacion_liv2['FECHA ASIGNACION AGENCIA']) 
asignacion_liv2['MES'] = asignacion_liv2['FECHA ASIGNACION AGENCIA'].dt.day

#Obtenemos edad
asignacion_liv2 = asignacion_liv2[asignacion_liv2['CURP / RFC'].notna()]
asignacion_liv2['NACIMIENTO'] = asignacion_liv2['CURP / RFC'].str[4:6]
asignacion_liv2['NACIMIENTO'] = pd.to_numeric(asignacion_liv2['NACIMIENTO'], errors='coerce')
asignacion_liv2['NACIMIENTO'] = np.where(asignacion_liv2['NACIMIENTO']>=10,'19'+asignacion_liv2['NACIMIENTO'].map(str),'20'+asignacion_liv2['NACIMIENTO'].map(str))
now = datetime.datetime.now()
año = now.year
asignacion_liv2['EDAD'] = [año-int(float(x)) for x in asignacion_liv2['NACIMIENTO']]
asignacion_liv2 = asignacion_liv2.loc[(asignacion_liv2['EDAD'] >= 18) & (asignacion_liv2['EDAD'] <= 100)]


#consolidado = pd.merge(asignacion_liv2,pivot_pagos,how='left', left_on=['# CUENTA','MES'], right_on=['Cuenta','Mes'])
#consolidado = consolidado.drop_duplicates()

geografico = pd.pivot_table(asignacion_liv2, index=['MES','ESTADO'], values=['SALDO ACTUAL'], aggfunc=('count','mean','sum'))
geografico = pd.DataFrame(geografico.to_records())
geografico.rename(columns={"('SALDO ACTUAL', 'count')":'NUM CUENTAS',"('SALDO ACTUAL', 'mean')":'PROMEDIO SALDO',"('SALDO ACTUAL', 'sum')":'SUMA SALDO'}, inplace=True)

#geografico["('SALDO ABOGADO', 'count')"].plot(kind='bar')

#Por agencia
agencia = pd.pivot_table(asignacion_liv2, index=['MES','ID AGENCIA'], values=['SALDO ACTUAL'], aggfunc=('count','mean','sum'))
agencia = pd.DataFrame(agencia.to_records())
agencia.rename(columns={"('SALDO ACTUAL', 'count')":'NUM CUENTAS',"('SALDO ACTUAL', 'mean')":'PROMEDIO SALDO',"('SALDO ACTUAL', 'sum')":'SUMA SALDO'}, inplace=True)

x,y = agencia['ID AGENCIA'],agencia['NUM CUENTAS']
plt.bar(x,y)

#Por edad
edad = pd.pivot_table(asignacion_liv2, index=['MES','EDAD'], values=['SALDO ACTUAL'], aggfunc=('count','mean','sum'))
edad = pd.DataFrame(edad.to_records())
edad.rename(columns={"('SALDO ACTUAL', 'count')":'NUM CUENTAS',"('SALDO ACTUAL', 'mean')":'PROMEDIO SALDO',"('SALDO ACTUAL', 'sum')":'SUMA SALDO'}, inplace=True)

#La union de estado agencia edad
asignacion_eae = pd.pivot_table(asignacion_liv2, index=['MES','ESTADO','ID AGENCIA','EDAD'], values=['SALDO ACTUAL'], aggfunc=('count','mean','sum'))
asignacion_eae = pd.DataFrame(asignacion_eae.to_records())
asignacion_eae.rename(columns={"('SALDO ACTUAL', 'count')":'NUM CUENTAS',"('SALDO ACTUAL', 'mean')":'PROMEDIO SALDO',"('SALDO ACTUAL', 'sum')":'SUMA SALDO'}, inplace=True)

#######################################Concatenamos la informacion################################### 
asignacion_liv2 = asignacion_liv2.sort_values('MES',ascending=True)
pagos_liv2 = pd.merge(pivot_pagos,asignacion_liv2,how='left',left_on=['Cuenta'],right_on=['# CUENTA'])
pagos_liv2.drop_duplicates(subset=['Mes','Cuenta','Dia semana'], inplace=True)

#Reporte pagos
pagos = pd.pivot_table(pagos_liv2,index=['Mes','ESTADO','ID AGENCIA','EDAD'],values=['monto'],aggfunc=('count','mean','sum'))
pagos = pd.DataFrame(pagos.to_records())
pagos.rename(columns={"('monto', 'count')":'PAGOS REALIZADOS',"('monto', 'mean')":'PROMEDIO PAGOS',"('monto', 'sum')":'SUMA PAGOS'},inplace=True)

#Pivot de pagos
pagos_geo = pd.pivot_table(pagos_liv2, index=['ESTADO'], values=['monto'], aggfunc=('sum'))
pagos_geo = pd.DataFrame(pagos_geo.to_records())
pagos_geo = pagos_geo.sort_values('monto',ascending=False)
pagos_geo.reset_index(drop=True,inplace=True)

plt.bar(pagos_geo['ESTADO'], pagos_geo['monto'])

#Pagos por edad
pagos_edad = pd.pivot_table(pagos_liv2, index=['EDAD'], values=['monto'], aggfunc=('sum'))
pagos_edad = pd.DataFrame(pagos_edad.to_records())

plt.bar(pagos_edad['EDAD'], pagos_edad['monto'])

#Pagos por division
pagos_division = pd.pivot_table(pagos_liv2, index=['Division'], values=['monto'], aggfunc=('sum'))
pagos_division = pd.DataFrame(pagos_division.to_records())
pagos_division = pagos_division.sort_values('monto',ascending=False)
pagos_division.reset_index(drop=True,inplace=True)

plt.bar(pagos_division['Division'], pagos_division['monto'])

pagos_liv3 = pagos_liv2.loc[pagos_liv2['SALDO ACTUAL']>0]
pagos_liv3['Porcentaje pago'] = pagos_liv3['monto']/pagos_liv3['SALDO ACTUAL']
pagos_liv3 = pagos_liv3.loc[pagos_liv3['Porcentaje pago']<3]

#Porcentaje de monto/saldo
pagos_porcentaje = pd.pivot_table(pagos_liv3,index=['Mes','ESTADO','ID AGENCIA','EDAD'],values=['Porcentaje pago'], aggfunc=np.mean)
pagos_porcentaje = pd.DataFrame(pagos_porcentaje.to_records())

#plt.bar(pagos_porcentaje_edad['EDAD'],pagos_porcentaje_edad['Porcentaje pago'])

####################################################################################################

pagos_liv4 = pagos_liv3[['EDAD','monto']]

plt.hist(pagos_liv4,bins=70)

pagos_liv4.describe()


plt.scatter(pagos_liv4['EDAD'],pagos_liv4['monto'])






##############################Escribimos el libro de excel##########################################
writer = pd.ExcelWriter(''+ruta+'/Reporte Liverpool Oct.xlsx', engine='xlsxwriter')
asignacion_eae.to_excel(writer,'ReporteAsignaciones',index=False,header=True)
pagos.to_excel(writer,'ReportePagos',index=False,header=True)
pagos_porcentaje.to_excel(writer,' PorcentajePagoProm',index=False, header=True)
pagos_liv3.to_excel(writer,'Pagos',index=False, header=True)
geografico.to_excel(writer,'AsignacionEstado',index=False, header=True)
agencia.to_excel(writer,'AsignacionAgencia',index=False, header=True)
edad.to_excel(writer,'AsignacionEdad',index=False,header=True)
pagos_geo.to_excel(writer,'PagosEstado',index=False, header=True)
pagos_division.to_excel(writer,'PagosAgencia',index=False, header=True)
pagos_edad.to_excel(writer,'PagosEdad',index=False, header=True)
writer.save()
writer.close()
