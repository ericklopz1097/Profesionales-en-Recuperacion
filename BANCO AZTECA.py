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

#def rango_fechas(desde, hasta):
#    return [desde + relativedelta(days=days) for days in range((hasta - desde).days + 1)]

#desde = datetime.date(2020,6,1)
#hasta = datetime.date(2020,8,31)
#periodos = rango_fechas(desde,hasta)
#periodos_asignacion1 = [date_obj.strftime('%d-%m-%Y') for date_obj in periodos]


#meses_asignacion = ['Enero2020','Febrero2020','Marzo2020','Junio2020','Julio2020','Agosto2020','Septiembre2020','Octubre2020','Noviembre2020']
sample_cols_to_keep =['#FIIDCAMPANA', 'FIPAIS', 'FICANAL','FISUCURSAL','FIFOLIO','FISEMATRASMAX','FNSALDO','FNSALDOCAPITAL','FNPAGOREQ','FCTEL1','FCTIPO1','FNDIA_PAGO','FIDIASATRASOMAX','FNCAPPAGODISP','FNABONOSEMANAL','FNCAPACIDADPAGO','FILCRACTIVA','FDFECPROXPAG','FNTASAINT','CP','fcnombreos','fcappaternoos','FITERRITORIO','FCDESCTERRITORIO','FIZONA','FCDESCZONA','FIREGION','FCDESCREGION','FIGERENCIA','FCDESCGERENCIA','FCBESTTIMETOCALL','FECHA']

meses_asignacion = ['Octubre2020','Noviembre2020']

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
asignacion_ba = asignacion_ba.rename(columns=str.upper)
asignacion_ba.drop_duplicates(subset=['#FIIDCAMPANA',
 'FIPAIS',
 'FICANAL',
 'FISUCURSAL',
 'FIFOLIO',
 'FISEMATRASMAX',
 'FNSALDO',
 'FNSALDOCAPITAL',
 'FNPAGOREQ',
 'FCTEL1',
 'FCTIPO1',
 'FNDIA_PAGO',
 'FIDIASATRASOMAX',
 'FNCAPPAGODISP',
 'FNABONOSEMANAL',
 'FNCAPACIDADPAGO',
 'FILCRACTIVA',
 'FDFECPROXPAG',
 'FNTASAINT',
 'CP',
 'FCNOMBREOS',
 'FCAPPATERNOOS',
 'FITERRITORIO',
 'FCDESCTERRITORIO',
 'FIZONA',
 'FCDESCZONA',
 'FIREGION',
 'FCDESCREGION',
 'FIGERENCIA',
 'FCDESCGERENCIA',
 'FCBESTTIMETOCALL'], keep=False, inplace=True)


territorio = pd.read_excel(''+ruta+'CODIGOS_TERRITORIO.xlsx', sheet_name='Territorio')
zona = pd.read_excel(''+ruta+'CODIGOS_TERRITORIO.xlsx', sheet_name='Zona')
gerencia = pd.read_excel(''+ruta+'CODIGOS_TERRITORIO.xlsx', sheet_name='Gerencia')



###################################################TABLAS DINAMICAS###################################################

#Comenzamos obteniendo promedio de promesas de pago
promesa_promedio = pd.pivot_table(promesas_pago, index=['FECHA'],columns=['CAMPANAID'], values=['FNMONTOPROMETIDO'], aggfunc=np.mean, fill_value=0)

#Pagos realizados
pagos_realizados = promesas_pago.loc[pd.DatetimeIndex(promesas_pago['FDFECHAABONO']).year >=2000]
vol_pagos = pd.pivot_table(pagos_realizados, index=['FECHA','CAMPANAID'], values=['FNMONTOPROMETIDO'], aggfunc='count' , fill_value=0)
vol_pagos = pd.DataFrame(pagos_realizados.to_records())

#Volumen asignacion
asignacion_ba['FIFOLIO'] = asignacion_ba['FIFOLIO'].astype(int)
volumen_cartera = pd.pivot_table(asignacion_ba, index=['FECHA','#FIIDCAMPANA'], values=['FIFOLIO'], aggfunc='count', fill_value=0)
volumen_cartera = pd.DataFrame(volumen_cartera.to_records())

#Eficiencia en cuanto a volumen
eficiencia_volumen = pd.merge(volumen_cartera, vol_pagos, how = 'left', left_on=['FECHA','#FIIDCAMPANA'], right_on=['FECHA','CAMPANAID'])

#Pago promedio 
pago_promedio = pd.pivot_table(pagos_realizados, index=['FECHA'], columns=['CAMPANAID'], values=['FNMONTOPAGADO'], aggfunc=np.mean, fill_value=0)
pago_promedio = pd.DataFrame(pago_promedio.to_records())

#Por fecha de cuando se asigno la promesa
fecha_promesa_prom = pd.pivot_table(pagos_realizados, index=['FDFECHAABONO'], columns=['CAMPANAID'], values=['FNMONTOPROMETIDO'], aggfunc=np.mean, fill_value=0)
fecha_promesa_prom = pd.DataFrame(fecha_promesa_prom.to_records())

#Eficiencia promesas contra pagado
promesas_realizadas_fecha = pd.pivot_table(promesas_pago, index=['FDFECHAPROMESA','CAMPANAID'], values=['FNMONTOPROMETIDO'], aggfunc=np.sum, fill_value=0)
pagos_realizados_fecha = pd.pivot_table(pagos_realizados, index=['FDFECHAPROMESA','CAMPANAID'], values=['FNMONTOPAGADO'], aggfunc=np.sum, fill_value=0)

eficiencia_pagos_promesas = pd.merge(promesas_realizadas_fecha, pagos_realizados_fecha, on=['FDFECHAPROMESA','CAMPANAID'], how='left')
eficiencia_pagos_promesas['EFICIENCIA'] = eficiencia_pagos_promesas['FNMONTOPAGADO']/eficiencia_pagos_promesas['FNMONTOPROMETIDO']

pivote_eficiencia_pagos_promesas = pd.pivot_table(eficiencia_pagos_promesas, index=['FDFECHAPROMESA'], columns=['CAMPANAID'], values=['EFICIENCIA'], aggfunc=np.sum, fill_value=0)

#Volumen promedio por semana de atraso
vol_semana_atraso = pd.pivot_table(asignacion_ba, index=['FECHA'], columns=['FISEMATRASMAX'], values=['FNSALDOCAPITAL'], aggfunc=np.mean, fill_value=0)

##########################################Cliente por semana##################################################

asignacion_ba['CLIENTEUNICO'] = asignacion_ba['FIPAIS'].map(str)+'-'+asignacion_ba['FICANAL'].map(str)+'-'+asignacion_ba['FISUCURSAL'].map(str)+'-'+asignacion_ba['FIFOLIO'].map(str)
asignacion_ba['PAGOSUGERIDO'] = asignacion_ba['FNPAGOREQ']+asignacion_ba['FNCAPPAGODISP']
asignacion_ba['FECHA'] = pd.to_datetime(asignacion_ba['FECHA'], errors ='coerce')
asignacion_ba['SEMANA'] = asignacion_ba['FECHA'].dt.week
asignacion_ba['UNICOSEMANA'] = asignacion_ba['CLIENTEUNICO'].map(str)+'-'+asignacion_ba['FISEMATRASMAX'].map(str)

asignacion_ba2 = asignacion_ba
asignacion_ba2 = asignacion_ba2.drop_duplicates(subset=['UNICOSEMANA'],keep=False)


cliente_semana = pd.pivot_table(asignacion_ba2, index=['CLIENTEUNICO'], columns=['FISEMATRASMAX'], values=['FIPAIS'], aggfunc='count', fill_value=0)
cliente_semana = pd.DataFrame(cliente_semana.to_records())
cliente_semana['TOTAL'] = cliente_semana.sum(axis=1)
cliente_semana_5 = cliente_semana.loc[cliente_semana['TOTAL']>=2]



#########################################Zona por territorio####################################################

asignacion_ba['FITERRITORIO'] = asignacion_ba['FCDESCTERRITORIO'].str[:4]
asignacion_ba['FIZONA'] = asignacion_ba['FCDESCZONA'].str[:4]
asignacion_ba['FITERRITORIO'].fillna(0, inplace=True)
asignacion_ba['FITERRITORIO'] = asignacion_ba['FITERRITORIO'].astype(int)
territorio['FITERRITORIO'].fillna(0, inplace=True)
territorio['FITERRITORIO'] = territorio['FITERRITORIO'].astype(int)
asignacion_ba['FIZONA'].fillna(0, inplace=True)
asignacion_ba['FIZONA'] = asignacion_ba['FIZONA'].astype(int)zona['FIZONA'] = zona['FIZONA'].astype(int
                                                                                                    ¿werfsdgxb m,.-
asignacion_ba = pd.merge(asignacion_ba, territorio, how='left', on='FITERRITORIO')
asignacion_ba = pd.merge(asignacion_ba, zona, how='left', on='FIZONA')

zona_territorio = pd.pivot_table(asignacion_ba, index=['TERRITORIO','ZONA'], columns=['#FIIDCAMPANA'], values=['FNSALDOCAPITAL'], aggfunc=np.mean,fill_value=0)
zona_territorio = pd.DataFrame(zona_territorio.to_records())


###############################################Gerencia#######################################################

asignacion_ba['FIGERENCIA'] = asignacion_ba['FCDESCGERENCIA'].str[:4]
asignacion_ba['FIGERENCIA'].fillna(0, inplace=True)
asignacion_ba['FIGERENCIA'] = asignacion_ba['FIGERENCIA'].astype(int)
gerencia['FIGERENCIA'] = gerencia['FIGERENCIA'].astype(int)
asignacion_ba = pd.merge(asignacion_ba, gerencia, on=['FIGERENCIA'], how='left')

gerencia_promesas = pd.pivot_table(asignacion_ba, index=['GERENCIA'],values=['PAGOSUGERIDO'], aggfunc=np.sum, fill_value=0)
gerencia_promesas = pd.DataFrame(gerencia_promesas.to_records())










writer = pd.ExcelWriter(''+ruta+'Reporte azteca_oct-nov.xlsx', engine='xlsxwriter')
pago_promedio.to_excel(writer, sheet_name='PagoPromedio')
vol_pagos.to_excel(writer, sheet_name='VolumenPagos')
volumen_cartera.to_excel(writer, sheet_name='VolumenCartera')
zona_territorio.to_excel(writer, sheet_name='ZonaTerritorio')
pivote_eficiencia_pagos_promesas.to_excel(writer, sheet_name='EficienciaPagoProm')
gerencia_promesas.to_excel(writer,sheet_name='Gerencia')
writer.save()
writer.close()

cliente_semana_5.to_csv(''+ruta+'ClienteSemana_oct-nov.csv', index=False, header=True)

print("Trabajo Finalizado")
#asignacion_ba.to_csv(''+ruta+'Asignacion banco azteca Ene-Oct', index = False, header=True)



list(asignacion_ba.columns)









