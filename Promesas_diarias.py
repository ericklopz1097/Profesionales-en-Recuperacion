#!/usr/bin/env python
# coding: utf-8

# # Reporte diario promesas realizadas durante el dia

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
ruta = '/home/estadistico/Documents/Erick/Reportes diarios/Promesas Diarias'
#Definimos la ruta donde estan las asignaciones
ruta_asig_baz = '/home/estadistico/Documents/Erick/Banco Azteca/Asignacion csv'
mes2 = 'Diciembre2020'


# In[3]:


#Agregamos las variables a ocupar
servidor = '192.168.15.12'
puerto = int('3306')
usuario = 'estadisticas'
contrasena = 'estadisticas8474'
base = 'procesos_externos'


# In[4]:


#Asignamos valores a los parametros \n",
today = date.today().strftime('%Y%m%d')
now = datetime.now().strftime('%d-%m-%Y-%H-%M')
today


# In[5]:


#Hacemos la conexion con el servidor\n",
try:
    conn = mysql.connector.connect(user=usuario,
                               password=contrasena,
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
sql_gest_liv = cursor.callproc('liverpool_rpt_gestiones_detallado', [today,today])
for result in cursor.stored_results():
    gestion_liv = pd.DataFrame(result.fetchall())
gestion_liv.columns = ['folio_gestion','firma_id','unegocio_id','credito','nombre_credito','telefono','tipo_telefono','fecha_gestion','usuario','nombre_usuario','dictamen','accion','resultado','fecha_promesa','monto_promesa','comentarios']
gestion_liv = gestion_liv.loc[gestion_liv['dictamen']=='PROMESA']
gestion_liv['credito'] = pd.to_numeric(gestion_liv['credito'])
gestion_liv.head(3)


# In[7]:


#Hacemos la consulta de la asignacion
sql_asig_liv = cursor.callproc('liverpool_rpt_asignacion_activa',)
for result in cursor.stored_results():
    asignacion_liv = pd.DataFrame(result.fetchall())
asignacion_liv = asignacion_liv.iloc[:,[0,1,3,24,6,26]]
asignacion_liv.columns = ['firma_id','unegocio_id','credito','estado','rfc','division']
asignacion_liv['credito'] = pd.to_numeric(asignacion_liv['credito'])
asignacion_liv.head(3)


# In[8]:


#Hacemos el consolidado 
consolidado_liv = pd.merge(gestion_liv,asignacion_liv,how='left',on=['firma_id','unegocio_id','credito'])
cols = ['monto_promesa','credito']
consolidado_liv[cols] = consolidado_liv[cols].apply(pd.to_numeric, errors='coerce')
consolidado_liv = consolidado_liv[(consolidado_liv['monto_promesa']>50)]
consolidado_liv = consolidado_liv[(consolidado_liv['monto_promesa']<500000)]
consolidado_liv.fillna('COBRANZA',inplace=True)
consolidado_liv.head(3)


# In[9]:


#Obtenemos datos de las promesas de Liverpool
pivot_liv = pd.pivot_table(consolidado_liv,index=['division'],values=['credito','monto_promesa'],aggfunc=['count',np.sum],margins=True)
pivot_liv = pd.DataFrame(pivot_liv.to_records())
pivot_liv = pivot_liv.iloc[:,[0,1,4]]
pivot_liv.columns = ['Division','NumeroPromesas','SumaPromesas']
pivot_liv.fillna(0,inplace=True)
#pivot_liv[['NumeroPromesas','PromedioPromesa','SumaPromesas']] = pivot_liv[['NumeroPromesas','PromedioPromesa','SumaPromesas']].applymap("{0:.2f}".format)
pivot_liv


# In[10]:


#Vemos las promesas reales eliminando duplicados
consolidado_liv2 = consolidado_liv.drop_duplicates(subset=['credito','fecha_promesa','monto_promesa'])
pivot_liv2 = pd.pivot_table(consolidado_liv2,index=['division'],values=['credito','monto_promesa'],aggfunc=['count',np.sum],margins=True)
pivot_liv2 = pd.DataFrame(pivot_liv2.to_records())
pivot_liv2 = pivot_liv2.iloc[:,[0,1,4]]
pivot_liv2.columns = ['Dictamen','NumeroPromesas','SumaPromesas']
pivot_liv2.fillna(0,inplace=True)
#pivot_liv2[['NumeroPromesas','PromedioPromesa','SumaPromesas']] = pivot_gestion_liv2[['NumeroPromesas','PromedioPromesa','SumaPromesas']].applymap("{0:.2f}".format)
pivot_liv2


# # Bradesco

# In[11]:


#Hacemos la consulta referente a las gestiones de Bradesco
sql_gest_brad = cursor.callproc('bradescard_rpt_gestiones_detallado', [today,today])
for result in cursor.stored_results():
    gestion_brad = pd.DataFrame(result.fetchall())
gestion_brad.columns = ['folio_gestion','firma_id','unegocio_id','credito','nombre_credito','telefono','tipo_telefono','fecha_gestion','usuario','nombre_usuario','dictamen','accion','resultado','accion_resultado','fecha_promesa','monto_promesa','comentarios']
gestion_brad = gestion_brad.loc[gestion_brad['dictamen']=='PROMESA']
gestion_brad['credito'] = pd.to_numeric(gestion_brad['credito'])
gestion_brad.head(3)


# In[12]:


#Convertimos a numero las columnas que necesitemos
gestion_brad[cols] = gestion_brad[cols].apply(pd.to_numeric, errors='coerce')


# In[13]:


#Hacemos la consulta de la asignacion
sql_asig_brad = cursor.callproc('bradescard_rpt_asignacion_activa',)
for result in cursor.stored_results():
    asignacion_brad = pd.DataFrame(result.fetchall())
asignacion_brad = asignacion_brad.iloc[:,[0,1,3,24,6,26]]
asignacion_brad.columns = ['firma_id','unegocio_id','credito','estado','rfc','division']
asignacion_brad['credito'] = pd.to_numeric(asignacion_brad['credito'])
asignacion_brad.head(3)


# In[14]:


#Hacemos la union de asignacion y promesas
consolidado_brad = pd.merge(gestion_brad,asignacion_brad,how='left',on=['firma_id','unegocio_id','credito'])
cols = ['monto_promesa','credito']
consolidado_brad[cols] = consolidado_brad[cols].apply(pd.to_numeric, errors='coerce')
consolidado_brad = consolidado_brad[(consolidado_brad['monto_promesa']>50)]
consolidado_brad = consolidado_brad[(consolidado_brad['monto_promesa']<500000)]
consolidado_brad.fillna('COBRANZA',inplace=True)
consolidado_brad.head(3)


# In[15]:


#Obtenemos datos de las promesas de Bradesco
pivot_brad = pd.pivot_table(consolidado_brad,index=['division'],values=['credito','monto_promesa'],aggfunc=['count',np.sum],margins=True)
pivot_brad = pd.DataFrame(pivot_brad.to_records())
pivot_brad = pivot_brad.iloc[:,[0,1,4]]
pivot_brad.columns = ['Division','NumeroPromesas','SumaPromesas']
pivot_brad.fillna(0,inplace=True)
#pivot_brad[['NumeroPromesas','PromedioPromesa','SumaPromesas']] = pivot_gestion_brad[['NumeroPromesas','PromedioPromesa','SumaPromesas']].applymap("{0:.2f}".format)
pivot_brad


# In[16]:


#Vemos las promesas reales eliminando duplicados
consolidado_brad2 = consolidado_brad.drop_duplicates(subset=['credito','fecha_promesa','monto_promesa'])
pivot_brad2 = pd.pivot_table(consolidado_brad2,index=['division'],values=['credito','monto_promesa'],aggfunc=['count',np.sum],margins=True)
pivot_brad2 = pd.DataFrame(pivot_brad2.to_records())
pivot_brad2 = pivot_brad2.iloc[:,[0,1,4]]
pivot_brad2.columns = ['Division','NumeroPromesas','SumaPromesas']
pivot_brad2.fillna(0,inplace=True)
#pivot_brad2[['NumeroPromesas','PromedioPromesa','SumaPromesas']] = pivot_gestion_brad2[['NumeroPromesas','PromedioPromesa','SumaPromesas']].applymap("{0:.2f}".format)
pivot_brad2


# # Credifiel

# In[17]:


#Hacemos la consulta referente a las gestiones de Credifiel
sql_gest_cred = cursor.callproc('credifiel_rpt_gestiones_detallado',[today,today])
for result in cursor.stored_results():
    gestion_cred = pd.DataFrame(result.fetchall())
gestion_cred.columns = ['folio_gestion','unegocio_id','fecha_gestion','hora_gestion','credito','nombre_credito','telefono','usuario','nombre_usuario','accion','resultado','fecha_promesa','monto_promesa','comentarios','accion_credifiel','resultado_credifiel','dictamen']
gestion_cred = gestion_cred.loc[gestion_cred['accion_credifiel']=='PDP']
cols = ['monto_promesa','unegocio_id']
gestion_cred[cols] = gestion_cred[cols].apply(pd.to_numeric, errors='coerce')
gestion_cred = gestion_cred.loc[gestion_cred['monto_promesa']>0]
gestion_cred.head(3)


# In[18]:


#Hacemos la consulta de la asignacion
sql_asig_cred = cursor.callproc('credifiel_rpt_asignacion_activa',)
for result in cursor.stored_results():
    asignacion_cred = pd.DataFrame(result.fetchall())
asignacion_cred = asignacion_cred.iloc[:,[1,3,32]]
asignacion_cred.columns = ['unegocio_id','credito','division']
#asignacion_brad['credito'] = pd.to_numeric(asignacion_brad['credito'])
asignacion_cred.head(3)


# In[19]:


#Hacemos la union de asignacion y promesas
consolidado_cred = pd.merge(gestion_cred,asignacion_cred,how='left',on=['unegocio_id','credito'])
cols = ['monto_promesa','unegocio_id']
consolidado_cred[cols] = consolidado_cred[cols].apply(pd.to_numeric, errors='coerce')
consolidado_cred = consolidado_cred[(consolidado_cred['monto_promesa']>50)]
consolidado_cred = consolidado_cred[(consolidado_cred['monto_promesa']<500000)]
consolidado_cred.fillna('COBRANZA',inplace=True)
consolidado_cred.replace('','COBRANZA',inplace=True)
consolidado_cred.head(3)


# In[20]:


#Obtenemos datos de las promesas de Credifiel
pivot_cred = pd.pivot_table(consolidado_cred,index=['division'],values=['unegocio_id','monto_promesa'],aggfunc=('count',np.sum))
pivot_cred = pd.DataFrame(pivot_cred.to_records())
pivot_cred = pivot_cred.iloc[:,[0,3,2]]
pivot_cred.columns = ['Division','NumeroPromesas','SumaPromesas']
pivot_cred.fillna(0,inplace=True)
pivot_cred = pivot_cred.loc[pivot_cred['SumaPromesas']>0]
#pivot_gestion_cred[['NumeroPromesas','PromedioPromesa','SumaPromesas']] = pivot_gestion_brad[['NumeroPromesas','PromedioPromesa','SumaPromesas']].applymap("{0:.2f}".format)
pivot_cred


# In[21]:


#Vemos las promesas reales eliminando duplicados
consolidado_cred2 = consolidado_cred.drop_duplicates(subset=['credito','fecha_promesa','monto_promesa'])
pivot_cred2 = pd.pivot_table(consolidado_cred2,index=['division'],values=['unegocio_id','monto_promesa'],aggfunc=('count',np.sum))
pivot_cred2 = pd.DataFrame(pivot_cred2.to_records())
pivot_cred2 = pivot_cred2.iloc[:,[0,3,2]]
pivot_cred2.columns = ['Division','NumeroPromesas','SumaPromesas']
pivot_cred2.fillna(0,inplace=True)
pivot_cred2 = pivot_cred2.loc[pivot_cred2['SumaPromesas']>0]
#pivot_gestion_cred[['NumeroPromesas','PromedioPromesa','SumaPromesas']] = pivot_gestion_brad[['NumeroPromesas','PromedioPromesa','SumaPromesas']].applymap("{0:.2f}".format)
pivot_cred2


# # Banco Azteca

# In[22]:


#Hacemos la consulta referente a las gestiones de Banco Azteca
sql_gest_baz = cursor.callproc('baz_rpt_gestiones_detallado', [today,today])
for result in cursor.stored_results():
     gestion_baz = pd.DataFrame(result.fetchall())
gestion_baz.columns = ['folio_gestion','firma_id','unegocio_id','credito','nombre_credito','telefono','tipo_telefono','fecha_gestion','usuario','nombre_usuario','dictamen','accion_resultado','fecha_promesa','monto_promesa','comentarios']
gestion_baz = gestion_baz.loc[gestion_baz['dictamen']=='PROMESA']
gestion_baz.head(3)


# In[23]:


#new_asignaciones = os.listdir('/home/estadistico/Documents/Erick/Banco Azteca/Asignacion')
#sample_cols_to_keep =['#FIIDCAMPANA', 'FIPAIS', 'FICANAL','FISUCURSAL','FIFOLIO','FISEMATRASMAX','FNSALDO','FNSALDOCAPITAL','FNPAGOREQ','FCTEL1','FCTIPO1','FNDIA_PAGO','FIDIASATRASOMAX','FNCAPPAGODISP','FNABONOSEMANAL','FNCAPACIDADPAGO','FILCRACTIVA','FDFECPROXPAG','FNTASAINT','CP','fcnombreos','fcappaternoos','FITERRITORIO','FCDESCTERRITORIO','FIZONA','FCDESCZONA','FIREGION','FCDESCREGION','FIGERENCIA','FCDESCGERENCIA','FCBESTTIMETOCALL','FECHA']
#df_iter = pd.read_csv('/home/estadistico/Documents/Erick/Banco Azteca/Asignacion_csv/Asignacion banco azteca '+mes+'.csv', chunksize=20000, usecols=sample_cols_to_keep) 
#df_lst = [] 
#for df_ in df_iter: 
#            tmp_df = (df_.rename(columns={col: col.lower() for col in df_.columns}))
#            df_lst += [tmp_df.copy()] 
#asignacion_baz = pd.concat(df_lst)


# In[24]:


asignacion_baz = pd.read_csv(''+ruta_asig_baz+'/Asignacion banco azteca '+str(mes2)+'.csv')
asignacion_baz = asignacion_baz.rename(columns=str.lower)
asignacion_baz.head(3)


# In[25]:


asignacion_baz['credito'] = asignacion_baz['fipais'].map(str)+'-'+asignacion_baz['ficanal'].map(str)+'-'+asignacion_baz['fisucursal'].map(str)+'-'+asignacion_baz['fifolio'].map(str)
asignacion_baz.head(3)


# In[26]:


consolidado_baz = pd.merge(gestion_baz,asignacion_baz,how='left',on='credito')
cols = ['monto_promesa','#fiidcampana']
consolidado_baz[cols] = consolidado_baz[cols].apply(pd.to_numeric, errors='coerce')
consolidado_baz = consolidado_baz[(consolidado_baz['monto_promesa']>50)]
consolidado_baz = consolidado_baz[(consolidado_baz['monto_promesa']<500000)]
consolidado_baz.fillna('COBRANZA',inplace=True)
consolidado_baz.head(3)


# In[27]:


#Obtenemos datos de las promesas de Banco Azteca
pivot_baz = pd.pivot_table(consolidado_baz,index=['dictamen'],values=['unegocio_id','monto_promesa'],aggfunc=('count',np.sum))
pivot_baz = pd.DataFrame(pivot_baz.to_records())
pivot_baz = pivot_baz.iloc[:,[0,3,2]]
pivot_baz.columns = ['Dictamen','NumeroPromesas','SumaPromesas']
pivot_baz.fillna(0,inplace=True)
#pivot_baz[['NumeroPromesas','PromedioPromesa','SumaPromesas']] = pivot_gestion_baz[['NumeroPromesas','PromedioPromesa','SumaPromesas']].applymap("{0:.2f}".format)
pivot_baz


# In[28]:


#Vemos las promesas reales eliminando duplicados
consolidado_baz2 = consolidado_baz.drop_duplicates(subset=['credito','fecha_promesa','monto_promesa'])
pivot_baz2 = pd.pivot_table(consolidado_baz2,index=['dictamen'],values=['unegocio_id','monto_promesa'],aggfunc=('count',np.sum))
pivot_baz2 = pd.DataFrame(pivot_baz2.to_records())
pivot_baz2 = pivot_baz2.iloc[:,[0,3,2]]
pivot_baz2.columns = ['Dictamen','NumeroPromesas','SumaPromesas']
pivot_baz2.fillna(0,inplace=True)
#pivot_baz2[['NumeroPromesas','PromedioPromesa','SumaPromesas']] = pivot_gestion_baz2[['NumeroPromesas','PromedioPromesa','SumaPromesas']].applymap("{0:.2f}".format)
pivot_baz2


# In[29]:


writer = pd.ExcelWriter(''+ruta+'/Reporte Promesas Diarias '+now+'.xlsx', engine='xlsxwriter')
pivot_liv.to_excel(writer,'PromDiariaLivBruto',index=False,header=True)
pivot_liv2.to_excel(writer,'PromDiariaLivReal',index=False,header=True)
pivot_brad.to_excel(writer,'PromDiariaBradBruto',index=False,header=True)
pivot_brad2.to_excel(writer,'PromDiariaBradReal',index=False,header=True)
pivot_cred.to_excel(writer,'PromDiariaCredBruto',index=False,header=True)
pivot_cred2.to_excel(writer,'PromDiariaCredReal',index=False,header=True)
pivot_baz.to_excel(writer,'PromDiariaBAZBruto',index=False,header=True)
pivot_baz2.to_excel(writer,'PromDiariaBAZReal',index=False,header=True)

writer.save()



# In[ ]:




