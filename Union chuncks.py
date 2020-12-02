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

ruta = "C:/Users/LENOVO T520/Documents/ERICK/BANCO AZTECA/"

periodos_promesas = ['20200105','20200112','20200119','20200126','20200202','20200203','20200209','20200216','20200301','20200308','20200315','20200316','20200322','20200329']

promesas_pago = pd.DataFrame()
for i in periodos_promesas:
    promesas = pd.read_excel(''+ruta+'PROMESAS PAGO/Prom_Pago_Exi_'+i+'.xlsx')
    promesas['FECHA'] = pd.to_datetime(i)
    promesas['FECHA']=promesas['FECHA'].dt.strftime('%Y/%m/%d')
    promesas_pago.reset_index(drop=True, inplace=True)
    promesas.reset_index(drop=True, inplace=True)
    promesas_pago = pd.concat([promesas_pago, promesas], axis=1)
    print(i)
promesas_pago.drop_duplicates(subset=['CALL_CENTER','FCEMPNUMCORTE','FDFECHAGENPROMESA','FDFECHAPROMESA','FIIDPERIODO','FNMONTOPROMETIDO','FNMONTOPAGADO','FDFECHAABONO','FNMONTOREQUERIDO','CAMPANAID','CAMPANA','FNSCOMPROMISO','DIASENTREGENYCOMPROMISO','CIERR_SEM','FCIDGESTOR','DESPACHO','DESCRIPCION','FECARRIBO'],keep=False,inplace=True)

def rango_fechas(desde, hasta):
    return [desde + relativedelta(days=days) for days in range((hasta - desde).days + 1)]

desde = datetime.date(2020,6,1)
hasta = datetime.date(2020,8,31)
periodos = rango_fechas(desde,hasta)
periodos_asignacion = [date_obj.strftime('%d-%m-%Y') for date_obj in periodos]
#periodos_asignacion = periodos_asignacion1+periodos_asignacion2

asignacion_ba = pd.DataFrame() 
for i in periodos_asignacion:
    asignacion = pd.read_excel(''+ruta+'ASIGNACION/baz_layout_carga_asignacion_renta_posiciones_'+i+'.xlsx')
    asignacion['FECHA'] = pd.to_datetime(i)
    asignacion['FECHA'] = asignacion['FECHA'].dt.strftime('%d/%m/%Y')
    asignacion_ba = asignacion_ba.append(asignacion, ignore_index=True)
    print(i)
asignacion_ba.drop_duplicates(subset=['#FIIDCAMPANA','FIPAIS','FICANAL','FISUCURSAL','FIFOLIO','FISEMATRASMAX','FNSALDO','FNSALDOCAPITAL','FNPAGOREQ','FCNOMBRE','FCAPPATERNO','FCAPMATERNO','FCTEL1','FCTIPO1','FCTEL2','FCTIPO2','FCTEL3','FCTIPO3','FCTEL4','FCTIPO4','FCTEL5','FCTIPO5','FNDIA_PAGO','FIDIASATRASOMAX','FNPAGOMIND','FNPAGOPNGI','FNCAPPAGODISP','FNABONOPUNTUAL','FNABONOSEMANAL','FNCAPACIDADPAGO','FITIPOGARAN','FILCRACTIVA','FDFECPROXPAG','FDFECVENCI','FNLINCREDAUT','FNTASAINT','FIORDENA','calle','NumInterior','NumExterior','Colonia','CP','fcctepoblacion','fccteestado','fcnombreos','fcappaternoos','fcapmaternoos','fctel1os','fctipo1os','fctel2os','fctipo2os','fctel3os','fctipo3os','fctel4os','fctipo4os','fctel5os','fctipo5os','FITERRITORIO','FCDESCTERRITORIO','FIZONA','FCDESCZONA','FIREGION','FCDESCREGION','FIGERENCIA','FCDESCGERENCIA','FCBESTTIMETOCALL'],keep=False,inplace=True)





meses_asignacion = ['Enero2020','Febrero2020','Julio2020']
#meses_asignacion = ['Enero2020','Febrero2020','Marzo2020','Junio2020','Julio2020','Agosto2020','Septiembre2020','Octubre2020']
sample_cols_to_keep =['#FIIDCAMPANA', 'FIPAIS', 'FICANAL','FISUCURSAL','FIFOLIO','FISEMATRASMAX','FNSALDO','FNSALDOCAPITAL','FNPAGOREQ','FCTEL1','FCTIPO1','FNDIA_PAGO','FIDIASATRASOMAX','FNCAPPAGODISP','FNABONOSEMANAL','FNCAPACIDADPAGO','FILCRACTIVA','FDFECPROXPAG','FNTASAINT','CP','fcnombreos','fcappaternoos','FITERRITORIO','FCDESCTERRITORIO','FIZONA','FCDESCZONA','FIREGION','FCDESCREGION','FIGERENCIA','FCDESCGERENCIA','FCBESTTIMETOCALL','FECHA']

asignacion_ba = pd.DataFrame()
for i in meses_asignacion:
    df_iter = pd.read_csv(''+ruta+'ASIGNACION_CSV/Asignacion banco azteca '+i+'.csv', chunksize=20000, usecols=sample_cols_to_keep) 
    df_lst = [] 
    for df_ in df_iter: 
            tmp_df = (df_.rename(columns={col: col.lower() for col in df_.columns}))
            df_lst += [tmp_df.copy()] 
    df_final = pd.concat(df_lst)
    asignacion_ba = pd.concat([asignacion_ba,df_final], ignore_index=True)
    print(i)





periodos_promesas = ['20200415','20200412','20200405','20200402','20200329','20200322','20200316','20200105','20200112','20200119','20200126','20200202','20200203','20200209','20200216','20200301','20200308','20200315']

promesas_pago = pd.DataFrame()
for i in periodos_promesas:
    promesas = pd.read_excel(''+ruta+'PROMESAS PAGO/Prom_Pago_Exi_'+i+'.xlsx')
    promesas = promesas[['FCEMPNUMCORTE','FDFECHAGENPROMESA','FDFECHAPROMESA','FIIDPERIODO','FNMONTOPROMETIDO',	'FNMONTOPAGADO','FDFECHAABONO',	'FNMONTOREQUERIDO',	'CAMPANAID','CAMPANA',	'FNSCOMPROMISO','DIASENTREGENYCOMPROMISO']]
    promesas_pago.to_csv(''+ruta+'PROMESAS PAGO/Prom_Pago_Exi_'+i+'.csv',index = False, header=True)
    print(i)
promesas_pago.drop_duplicates(subset=['FCEMPNUMCORTE','FDFECHAGENPROMESA','FDFECHAPROMESA','FIIDPERIODO','FNMONTOPROMETIDO','FNMONTOPAGADO','FDFECHAABONO',	'FNMONTOREQUERIDO',	'CAMPANAID','CAMPANA',	'FNSCOMPROMISO','DIASENTREGENYCOMPROMISO'],keep=False,inplace=True)










