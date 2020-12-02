# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 13:38:48 2020

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
from datetime import datetime
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

#Cargamos la ruta en donde se encuentran los archivos de banco azteca
ruta = 'C:/Users/LENOVO T520/Documents/ERICK/CREDIFIEL'

#Leemos los dos archivos importantes donde se localiza 
facturacion = pd.read_csv(''+ruta+'/CREDIFIEL 2020 FACTURACION.csv',encoding = "ISO-8859-1", engine='python',skipinitialspace=True)
asignacion = pd.read_csv(''+ruta+'/CREDIFIEL 2020 ASIGNACION.csv',encoding = "ISO-8859-1", engine='python',skipinitialspace=True)
asignacion.columns = asignacion.columns.str.rstrip()

#Juntamos ambos archivos en uno
consolidado_final = pd.merge(asignacion[['MES', 'DAP', 'EDAD', 'RFC', 'IRR', 'INACTIVIDAD', 'NIVEL DE RIESGO', 'MONTO DISPERSADO', 'CAPITAL', 'IVA COLOCACION', 'INTERES COLOCACION', 'PAGARE', 'CUOTA', 'PLAZO', 'PAGO PERIODO MENSUAL', 'TOTAL PAGADO', 'SALDO K', 'SALDO INT ACT', 'SALDO IVA ACT', 'SALDO TOTAL', 'SALDO VENCIDO', 'MONTO EN TRANSITO', 'No PAGOS EN TRANSITO', 'SALDO TOTAL REAL', 'SALDO VENCIDO REAL', 'CUOTAS VENCIDAS', 'FECHA ULTIMO PAGO', 'PERIODO ULTIMO PAGO ORIGEN', 'MONTO PARA LIQUIDAR', 'NIVEL DE ATENCION']],
                       facturacion[['DAP', 'IMPORTE', 'CUENTA', 'BANCO', 'MES']], how='outer', on=['DAP','MES'])

consolidado = consolidado_final.loc[(consolidado_final['RFC'] != '0') & (consolidado_final['RFC'] != 'D') & (consolidado_final['DAP'] != 98904121161)]
consolidado = consolidado[consolidado['RFC'].notna()]
consolidado['NACIMIENTO'] = consolidado['RFC'].str[4:6]
consolidado['NACIMIENTO'] = pd.to_numeric(consolidado['NACIMIENTO'], errors='coerce')
consolidado['NACIMIENTO'] = np.where(consolidado['NACIMIENTO']>=20,'19'+consolidado['NACIMIENTO'].map(str),'20'+consolidado['NACIMIENTO'].map(str))
now = datetime.now()
año = now.year
consolidado['EDAD'] = [año-int(float(x)) for x in consolidado['NACIMIENTO']]
consolidado = consolidado.loc[(consolidado['EDAD'] >= 18) & (consolidado['EDAD'] <= 100)]

#Trabajamos con pagos
pagos1 = pd.pivot_table(facturacion,index=['DAP','CUENTA','MES'],values=['IMPORTE'],aggfunc=np.sum)
pagos1 = pd.DataFrame(pagos1.to_records())
pagos = pd.merge(pagos1, asignacion[['MES', 'DAP', 'EDAD', 'RFC', 'IRR', 'INACTIVIDAD', 'NIVEL DE RIESGO', 'MONTO DISPERSADO', 'CAPITAL', 'IVA COLOCACION', 'INTERES COLOCACION', 'PAGARE', 'CUOTA', 'PLAZO', 'PAGO PERIODO MENSUAL', 'TOTAL PAGADO', 'SALDO K', 'SALDO INT ACT', 'SALDO IVA ACT', 'SALDO TOTAL', 'SALDO VENCIDO', 'MONTO EN TRANSITO', 'No PAGOS EN TRANSITO', 'SALDO TOTAL REAL', 'SALDO VENCIDO REAL', 'CUOTAS VENCIDAS', 'FECHA ULTIMO PAGO', 'PERIODO ULTIMO PAGO ORIGEN', 'MONTO PARA LIQUIDAR', 'NIVEL DE ATENCION']],how='left',on=['DAP','MES'])
pagos.dropna(subset=['RFC'],inplace=True)
pagos = pagos.loc[(pagos['RFC'] != '0')]
pagos['NACIMIENTO'] = pagos['RFC'].str[4:6]
pagos['NACIMIENTO'] = pd.to_numeric(pagos['NACIMIENTO'], errors='coerce')
pagos['NACIMIENTO'] = np.where(pagos['NACIMIENTO']>=20,'19'+pagos['NACIMIENTO'].map(str),'20'+pagos['NACIMIENTO'].map(str))
now = datetime.now()
año = now.year
pagos['EDAD'] = [año-int(float(x)) for x in pagos['NACIMIENTO']]
pagos = pagos.loc[(pagos['EDAD'] >= 18) & (pagos['EDAD'] <= 100)]
pagos['CUENTA'] = np.where(pagos['CUENTA']=='STP',1,pagos['CUENTA'])
pagos['CUENTA'] = pd.to_numeric(pagos['CUENTA'],errors='coerce')
pagos['IRR2'] = np.where(pagos['IRR']=='SI',1,0)


###Porcentaje de pago
pagos['PORCENTAJE'] = pagos['IMPORTE']/pagos['MONTO PARA LIQUIDAR']
pagos = pagos.loc[pagos['PORCENTAJE']<3]

porcentaje_pago_edad = pd.pivot_table(pagos,index=['EDAD'],values=['PORCENTAJE'],aggfunc=np.mean)
porcentaje_pago_edad = pd.DataFrame(porcentaje_pago_edad.to_records())
plt.bar(porcentaje_pago_edad['EDAD'],porcentaje_pago_edad['PORCENTAJE'])

porcentaje_pago_riesgo = pd.pivot_table(pagos,index=['NIVEL DE RIESGO'],values=['PORCENTAJE'],aggfunc=np.mean)
porcentaje_pago_riesgo = pd.DataFrame(porcentaje_pago_riesgo.to_records())
plt.bar(porcentaje_pago_riesgo['NIVEL DE RIESGO'],porcentaje_pago_riesgo['PORCENTAJE'])

#Nos quedamos unicamente con los pagos que se realizaron

edad = pagos[['EDAD','IRR2','IMPORTE','NIVEL DE RIESGO','INACTIVIDAD','PLAZO','SALDO TOTAL','CUOTAS VENCIDAS','CUENTA']]
cor = edad.corr()
edad.hist()
x=edad['SALDO TOTAL']
y=edad['IMPORTE']

plt.scatter(x, y)
plt.show()


pivot = pd.pivot_table(consolidado,values=['EDAD'],index=['NIVEL DE RIESGO'],aggfunc='count')
pivot2 = pd.pivot_table(pagos,values=['EDAD'],index=['NIVEL DE RIESGO'],aggfunc='count')

piv = pd.merge(pivot, pivot2, on='NIVEL DE RIESGO')
piv['EFICIENCIA'] = 100*piv.EDAD_y/piv.EDAD_x




consolidado['CUENTA'] = np.where(consolidado['CUENTA']=='STP',1,consolidado['CUENTA'])
consolidado['CUENTA'] = pd.to_numeric(consolidado['CUENTA'],errors='coerce')
consolidado['IRR2'] = np.where(consolidado['IRR']=='SI',1,0)
consolidado = consolidado.loc[(consolidado['CUOTAS VENCIDAS']<=200)&(consolidado['CUOTAS VENCIDAS']>0)]
consolidado = consolidado.loc[consolidado['SALDO TOTAL']<=500000]

edad = consolidado[['EDAD','IRR2','IMPORTE','NIVEL DE RIESGO','INACTIVIDAD','PLAZO','SALDO TOTAL','CUOTAS VENCIDAS','CUENTA']]
cor = edad.corr()
edad.hist(bins=10)


edad2 = pagos[['SALDO TOTAL','CUOTAS VENCIDAS','IMPORTE']]
array = edad2.values
x = edad2[['SALDO TOTAL']]
y = edad2[['IMPORTE']]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=1, shuffle=True)

model = LinearRegression()
model.fit(x_train,y_train)

y_predict = model.predict(x_test)

# Veamos los coeficienetes obtenidos, En nuestro caso, serán la Tangente
print('Coefficients: \n', model.coef_)
# Este es el valor donde corta el eje Y (en X=0)
print('Independent term: \n', model.intercept_)
# Error Cuadrado Medio
print("Mean squared error: %.2f" % mean_squared_error(y_test, y_predict))
# Puntaje de Varianza. El mejor puntaje es un 1.0
print('Variance score: %.2f' % r2_score(y_test, y_predict))

plt.scatter(x,y)
plt.plot(x_test, y_predict, color='red')
plt.show()
