import pandas as pd 
import numpy as np 
import os

mes = 'Diciembre2020'

new_asignaciones = os.listdir('/home/estadistico/Documents/Erick/Banco Azteca/Asignacion/'+mes+'/')
asignaciones = pd.DataFrame()
for i in new_asignaciones:
    day_asignacion = pd.read_excel('/home/estadistico/Documents/Erick/Banco Azteca/Asignacion/'+mes+'/'+i+'')
    day_asignacion = day_asignacion[['#FIIDCAMPANA', 'FIPAIS', 'FICANAL','FISUCURSAL','FIFOLIO']]
    asignaciones = pd.concat([asignaciones, day_asignacion], ignore_index=True)
    print(i)

asignaciones.to_csv('/home/estadistico/Documents/Erick/Banco Azteca/Asignacion csv/Asignacion banco azteca '+mes+'.csv',header=True,index=False)

