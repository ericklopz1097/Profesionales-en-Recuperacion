import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
from datetime import date
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

#Definimos la ruta en donde queremos guardar los archivos
ruta = '/home/estadistico/Documents/Erick/Reportes diarios/Promesas'

#Agregamos las variables a ocupar
servidor = '192.168.15.12'
puerto = int('3306')
usuario = 'estadisticas'
contraseña = 'estadisticas8474'
base = 'procesos_externos'

#Asignamos valores a los parametros \n",
today = date.today().strftime('%Y%m%d')
today

#Hacemos la conexion con el servidor\n",
try:
    conn = mysql.connector.connect(user=usuario,
                               password=contraseña,
                               host=servidor,
                               port=3306,
                               database=base)
    conn.set_charset_collation('latin1')
except mysql.Error as e:
    print("Failed to execute stored procedure: {}".format(error))

cursor = conn.cursor()

#Hacemos la consulta referente a las gestiones de Liverpool
sql_gest_liv = cursor.callproc('liverpool_rpt_gestiones_detallado', [today,today])
for result in cursor.stored_results():
    gestion_liv = pd.DataFrame(result.fetchall())
gestion_liv.columns = ['folio_gestion','firma_id','unegocio_id','credito','nombre_credito','telefono','tipo_telefono','fecha_gestion','usuario','nombre_usuario','dictamen','accion','resultado','fecha_promesa','monto_promesa','comentarios']


#Convertimos a numero las columnas que necesitemos
cols = ['monto_promesa','credito']
gestion_liv[cols] = gestion_liv[cols].apply(pd.to_numeric, errors='coerce')

#Obtenemos datos de las promesas de Liverpool
pivot_gestion_liv = pd.pivot_table(gestion_liv,index=['dictamen'],values=['credito','monto_promesa'],aggfunc=('count',np.sum,np.mean))
pivot_gestion_liv = pd.DataFrame(pivot_gestion_liv.to_records())
pivot_gestion_liv = pivot_gestion_liv.iloc[:,[0,1,5,6]]
pivot_gestion_liv.columns = ['Dictamen','NumeroPromesas','PromedioPromesa','SumaPromesas']
pivot_gestion_liv.fillna(0,inplace=True)
pivot_gestion_liv[['NumeroPromesas','PromedioPromesa','SumaPromesas']] = pivot_gestion_liv[['NumeroPromesas','PromedioPromesa','SumaPromesas']].applymap("{0:.2f}".format)

#Vemos las promesas reales eliminando duplicados
gestion_liv2 = gestion_liv.drop_duplicates(subset=['credito','fecha_promesa','monto_promesa'])
pivot_gestion_liv2 = pd.pivot_table(gestion_liv2,index=['dictamen'],values=['credito','monto_promesa'],aggfunc=('count',np.sum,np.mean))
pivot_gestion_liv2 = pd.DataFrame(pivot_gestion_liv2.to_records())
pivot_gestion_liv2 = pivot_gestion_liv2.iloc[:,[0,1,5,6]]
pivot_gestion_liv2.columns = ['Dictamen','NumeroPromesas','PromedioPromesa','SumaPromesas']
pivot_gestion_liv2.fillna(0,inplace=True)
pivot_gestion_liv2[['NumeroPromesas','PromedioPromesa','SumaPromesas']] = pivot_gestion_liv2[['NumeroPromesas','PromedioPromesa','SumaPromesas']].applymap("{0:.2f}".format)

#Hacemos la consulta referente a las gestiones de Bradesco
sql_gest_brad = cursor.callproc('bradescard_rpt_gestiones_detallado', [today,today])
for result in cursor.stored_results():
    gestion_brad = pd.DataFrame(result.fetchall())
gestion_brad.columns = ['folio_gestion','firma_id','unegocio_id','credito','nombre_credito','telefono','tipo_telefono','fecha_gestion','usuario','nombre_usuario','dictamen','accion','resultado','accion_resultado','fecha_promesa','monto_promesa','comentarios']

#Convertimos a numero las columnas que necesitemos
gestion_brad[cols] = gestion_brad[cols].apply(pd.to_numeric, errors='coerce')

#Obtenemos datos de las promesas de Bradesco
pivot_gestion_brad = pd.pivot_table(gestion_brad,index=['dictamen'],values=['credito','monto_promesa'],aggfunc=('count',np.sum,np.mean))
pivot_gestion_brad = pd.DataFrame(pivot_gestion_brad.to_records())
pivot_gestion_brad = pivot_gestion_brad.iloc[:,[0,1,5,6]]
pivot_gestion_brad.columns = ['Dictamen','NumeroPromesas','PromedioPromesa','SumaPromesas']
pivot_gestion_brad.fillna(0,inplace=True)
pivot_gestion_brad[['NumeroPromesas','PromedioPromesa','SumaPromesas']] = pivot_gestion_brad[['NumeroPromesas','PromedioPromesa','SumaPromesas']].applymap("{0:.2f}".format)

#Vemos las promesas reales eliminando duplicados
gestion_brad2 = gestion_brad.drop_duplicates(subset=['credito','fecha_promesa','monto_promesa'])
pivot_gestion_brad2 = pd.pivot_table(gestion_brad2,index=['dictamen'],values=['credito','monto_promesa'],aggfunc=('count',np.sum,np.mean))
pivot_gestion_brad2 = pd.DataFrame(pivot_gestion_brad2.to_records())
pivot_gestion_brad2 = pivot_gestion_brad2.iloc[:,[0,1,5,6]]
pivot_gestion_brad2.columns = ['Dictamen','NumeroPromesas','PromedioPromesa','SumaPromesas']
pivot_gestion_brad2.fillna(0,inplace=True)
pivot_gestion_brad2[['NumeroPromesas','PromedioPromesa','SumaPromesas']] = pivot_gestion_brad2[['NumeroPromesas','PromedioPromesa','SumaPromesas']].applymap("{0:.2f}".format)

#Hacemos la consulta referente a las gestiones de Banco Azteca
sql_gest_cred = cursor.callproc('credifiel_rpt_gestiones_detallado', [today,today])
for result in cursor.stored_results():
    gestion_cred = pd.DataFrame(result.fetchall())
gestion_cred.columns = ['folio_gestion','unegocio_id','fecha_gestion','hora_gestion','credito','nombre_credito','telefono','usuario','nombre_usuario','accion','resultado','fecha_promesa','monto_promesa','comentarios','accion_credifiel','resultado_credifiel','dictamen']
