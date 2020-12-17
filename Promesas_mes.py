#!/usr/bin/env python
# coding: utf-8

# # Reporte de promesas acumuladas en el mes

# In[1]:


import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
from datetime import date
from datetime import datetime
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# In[2]:


#Definimos la ruta en donde queremos guardar los archivos
ruta = '/home/estadistico/Documents/Erick/Reportes diarios/Promesas Mes'
#Definimos la ruta donde estan las asignaciones
ruta_asig_baz = '/home/estadistico/Documents/Erick/Banco Azteca/Asignacion csv'
mes = 20201201
mes2 = 'Diciembre2020'


# In[3]:


#Agregamos las variables a ocupar
servidor = '192.168.15.12'
puerto = int('3306')
usuario = 'estadisticas'
contraseña = 'estadisticas8474'
base = 'procesos_externos'


# In[4]:


#Asignamos valores a los parametros \n",
today = date.today().strftime('%Y%m%d')
now = datetime.now().strftime('%d-%m-%Y-%H:%M')


# In[5]:


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


# # Liverpool

# In[6]:


#Hacemos la consulta referente a las gestiones de Liverpool
sql_gest_liv = cursor.callproc('liverpool_rpt_gestiones_detallado', [mes,today])
for result in cursor.stored_results():
    gestion_liv = pd.DataFrame(result.fetchall())
gestion_liv.columns = ['folio_gestion','firma_id','unegocio_id','credito','nombre_credito','telefono','tipo_telefono','fecha_gestion','usuario','nombre_usuario','dictamen','accion','resultado','fecha_promesa','monto_promesa','comentarios']
gestion_liv = gestion_liv.loc[gestion_liv['dictamen']=='PROMESA']
gestion_liv['credito'] = pd.to_numeric(gestion_liv['credito'])
#gestion_liv.head(3)


# In[7]:


#Hacemos la consulta de la asignacion
sql_asig_liv = cursor.callproc('liverpool_rpt_asignacion_activa',)
for result in cursor.stored_results():
    asignacion_liv = pd.DataFrame(result.fetchall())
asignacion_liv = asignacion_liv.iloc[:,[0,1,3,24,6,26]]
asignacion_liv.columns = ['firma_id','unegocio_id','credito','estado','rfc','division']
asignacion_liv['credito'] = pd.to_numeric(asignacion_liv['credito'])
#asignacion_liv.head(3)


# In[8]:


#Hacemos el consolidado 
consolidado_liv = pd.merge(gestion_liv,asignacion_liv,how='left',on=['firma_id','unegocio_id','credito'])
cols = ['monto_promesa','credito']
consolidado_liv[cols] = consolidado_liv[cols].apply(pd.to_numeric, errors='coerce')
consolidado_liv = consolidado_liv[(consolidado_liv['monto_promesa']>50)]
consolidado_liv = consolidado_liv[(consolidado_liv['monto_promesa']<500000)]
consolidado_liv.fillna('COBRANZA',inplace=True)
#consolidado_liv.head(3)


# In[9]:


#Obtenemos datos de las promesas de Liverpool
consolidado_liv2 = consolidado_liv.drop_duplicates(subset=['credito','fecha_promesa','monto_promesa'])
pivot_liv = pd.pivot_table(consolidado_liv2,index=['division'],values=['credito','monto_promesa'],aggfunc=['count',np.sum],margins=True)
pivot_liv = pd.DataFrame(pivot_liv.to_records())
pivot_liv = pivot_liv.iloc[:,[0,1,4]]
pivot_liv.columns = ['Division','NumeroPromesas','SumaPromesas']
pivot_liv.fillna(0,inplace=True)
#pivot_liv[['NumeroPromesas','PromedioPromesa','SumaPromesas']] = pivot_liv[['NumeroPromesas','PromedioPromesa','SumaPromesas']].applymap("{0:.2f}".format)
pivot_liv


# # Bradesco 

# In[10]:


#Hacemos la consulta referente a las gestiones de Bradesco
sql_gest_brad = cursor.callproc('bradescard_rpt_gestiones_detallado', [mes,today])
for result in cursor.stored_results():
    gestion_brad = pd.DataFrame(result.fetchall())
gestion_brad.columns = ['folio_gestion','firma_id','unegocio_id','credito','nombre_credito','telefono','tipo_telefono','fecha_gestion','usuario','nombre_usuario','dictamen','accion','resultado','accion_resultado','fecha_promesa','monto_promesa','comentarios']
gestion_brad = gestion_brad.loc[gestion_brad['dictamen']=='PROMESA']
gestion_brad['credito'] = pd.to_numeric(gestion_brad['credito'])
gestion_brad['monto_promesa'] = pd.to_numeric(gestion_brad['monto_promesa'])
#gestion_brad.head(3)


# In[22]:


#Hacemos la consulta de la asignacion
sql_asig_brad = cursor.callproc('bradescard_rpt_asignacion_activa',)
for result in cursor.stored_results():
    asignacion_brad = pd.DataFrame(result.fetchall())
asignacion_brad = asignacion_brad.iloc[:,[0,1,3,24,6,26]]
asignacion_brad.columns = ['firma_id','unegocio_id','credito','estado','rfc','division']
asignacion_brad['credito'] = pd.to_numeric(asignacion_brad['credito'])
asignacion_brad.head(3)


# In[23]:


#Hacemos la union de asignacion y promesas
consolidado_brad = pd.merge(gestion_brad,asignacion_brad,how='left',on=['firma_id','unegocio_id','credito'])
cols = ['monto_promesa','credito']
consolidado_liv[cols] = consolidado_liv[cols].apply(pd.to_numeric, errors='coerce')
consolidado_brad = consolidado_brad[(consolidado_brad['monto_promesa']>50)]
consolidado_brad = consolidado_brad[(consolidado_brad['monto_promesa']<500000)]
consolidado_brad.fillna('COBRANZA',inplace=True)
#consolidado_brad.head(3)


# In[24]:


#Obtenemos datos de las promesas de Bradesco
consolidado_brad2 = consolidado_brad.drop_duplicates(subset=['credito','fecha_promesa','monto_promesa'])
pivot_brad = pd.pivot_table(consolidado_brad2,index=['division'],values=['credito','monto_promesa'],aggfunc=['count',np.sum],margins=True)
pivot_brad = pd.DataFrame(pivot_brad.to_records())
pivot_brad = pivot_brad.iloc[:,[0,1,4]]
pivot_brad.columns = ['Division','NumeroPromesas','SumaPromesas']
pivot_brad.fillna(0,inplace=True)
#pivot_brad[['NumeroPromesas','PromedioPromesa','SumaPromesas']] = pivot_gestion_brad[['NumeroPromesas','PromedioPromesa','SumaPromesas']].applymap("{0:.2f}".format)
pivot_brad


# # Credifiel

# In[25]:


#Hacemos la consulta referente a las gestiones de Credifiel
sql_gest_cred = cursor.callproc('credifiel_rpt_gestiones_detallado', [mes,today])
for result in cursor.stored_results():
    gestion_cred = pd.DataFrame(result.fetchall())
gestion_cred.columns = ['folio_gestion','unegocio_id','fecha_gestion','hora_gestion','credito','nombre_credito','telefono','usuario','nombre_usuario','accion','resultado','fecha_promesa','monto_promesa','comentarios','accion_credifiel','resultado_credifiel','dictamen']
gestion_cred['monto_promesa'] = pd.to_numeric(gestion_cred['monto_promesa'])
gestion_cred = gestion_cred.loc[gestion_cred['accion_credifiel']=='PDP']
gestion_cred.head(3)


# In[26]:


#Hacemos la consulta de la asignacion
sql_asig_cred = cursor.callproc('credifiel_rpt_asignacion_activa',)
for result in cursor.stored_results():
    asignacion_cred = pd.DataFrame(result.fetchall())
asignacion_cred = asignacion_cred.iloc[:,[1,3,32]]
asignacion_cred.columns = ['unegocio_id','credito','division']
#asignacion_brad['credito'] = pd.to_numeric(asignacion_brad['credito'])
asignacion_cred.head(3)


# In[27]:


#Hacemos el consolidado de la asignacion y promesado
consolidado_cred = pd.merge(gestion_cred,asignacion_cred,how='left',on=['unegocio_id','credito'])
cols = ['monto_promesa','unegocio_id']
consolidado_cred[cols] = consolidado_cred[cols].apply(pd.to_numeric, errors='coerce')
consolidado_cred = consolidado_cred.loc[consolidado_cred['monto_promesa']>50]
consolidado_cred = consolidado_cred[(consolidado_cred['monto_promesa']<500000)]
consolidado_cred.fillna('COBRANZA',inplace=True)
consolidado_cred.replace('','COBRANZA',inplace=True)
consolidado_cred.head(3)


# In[28]:


#Obtenemos datos de las promesas de Credifiel
consolidado_cred2 = consolidado_cred.drop_duplicates(subset=['credito','fecha_promesa','monto_promesa'])
pivot_cred = pd.pivot_table(consolidado_cred,index=['division'],values=['unegocio_id','monto_promesa'],aggfunc=['count',np.sum],margins=True)
pivot_cred = pd.DataFrame(pivot_cred.to_records())
pivot_cred = pivot_cred.iloc[:,[0,2,3]]
pivot_cred.columns = ['Accion_Credifiel','NumeroPromesas','SumaPromesas']
pivot_cred.fillna(0,inplace=True)
#pivot_gestion_cred[['NumeroPromesas','PromedioPromesa','SumaPromesas']] = pivot_gestion_brad[['NumeroPromesas','PromedioPromesa','SumaPromesas']].applymap("{0:.2f}".format)
pivot_cred


# # Banco Azteca

# In[29]:


#Hacemos la consulta referente a las gestiones de Banco Azteca
sql_gest_baz = cursor.callproc('baz_rpt_gestiones_detallado', [mes,today])
for result in cursor.stored_results():
     gestion_baz = pd.DataFrame(result.fetchall())
gestion_baz.columns = ['folio_gestion','firma_id','unegocio_id','credito','nombre_credito','telefono','tipo_telefono','fecha_gestion','usuario','nombre_usuario','dictamen','accion_resultado','fecha_promesa','monto_promesa','comentarios']
gestion_baz = gestion_baz.loc[gestion_baz['dictamen']=='PROMESA']
gestion_baz.head(3)


# In[30]:


asignacion_baz = pd.read_csv(''+ruta_asig_baz+'/Asignacion banco azteca '+str(mes2)+'.csv')
asignacion_baz = asignacion_baz.rename(columns=str.lower)
asignacion_baz.head(3)


# In[31]:


asignacion_baz['credito'] = asignacion_baz['fipais'].map(str)+'-'+asignacion_baz['ficanal'].map(str)+'-'+asignacion_baz['fisucursal'].map(str)+'-'+asignacion_baz['fifolio'].map(str)
asignacion_baz.head(3)


# In[32]:


consolidado_baz = pd.merge(gestion_baz,asignacion_baz,how='left',on='credito')
cols = ['monto_promesa','#fiidcampana']
consolidado_baz[cols] = consolidado_baz[cols].apply(pd.to_numeric, errors='coerce')
consolidado_baz = consolidado_baz[(consolidado_baz['monto_promesa']>50)]
consolidado_baz = consolidado_baz[(consolidado_baz['monto_promesa']<500000)]
consolidado_baz.fillna('COBRANZA',inplace=True)
consolidado_baz.head(3)


# In[33]:


#Obtenemos datos de las promesas de Banco Azteca
consolidado_baz2 = consolidado_baz.drop_duplicates(subset=['credito','fecha_promesa','monto_promesa'])
pivot_baz = pd.pivot_table(consolidado_baz,index=['dictamen'],values=['unegocio_id','monto_promesa'],aggfunc=('count',np.sum))
pivot_baz = pd.DataFrame(pivot_baz.to_records())
pivot_baz = pivot_baz.iloc[:,[0,3,2]]
pivot_baz.columns = ['Dictamen','NumeroPromesas','SumaPromesas']
pivot_baz.fillna(0,inplace=True)
#pivot_baz[['NumeroPromesas','PromedioPromesa','SumaPromesas']] = pivot_gestion_baz[['NumeroPromesas','PromedioPromesa','SumaPromesas']].applymap("{0:.2f}".format)
pivot_baz


# In[ ]:





# In[34]:


writer = pd.ExcelWriter(''+ruta+'/Reporte Promesas Acumulado Mes '+now+'.xlsx', engine='xlsxwriter')
pivot_liv.to_excel(writer,'PromMesLiverpool',index=False,header=True)
pivot_brad.to_excel(writer,'PromMesBradesco',index=False,header=True)
pivot_cred.to_excel(writer,'PromMesCredifiel',index=False,header=True)
pivot_baz.to_excel(writer,'PromBancoAzteca',index=False,header=True)

writer.save()


