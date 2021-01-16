import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error

# COneccion a torreon en donde necesitamos la query
def query_torreon(query=''): 
    conn = mysql.connector.connect(user='estadisticas',
                                   password='estadisticas8474',
                                   host='192.168.2.178',
                                   port=3306,
                                   database='recovery_rts')
    conn.set_charset_collation('latin1')

    cursor = conn.cursor()         # Crear un cursor 
    cursor.execute(query)          # Ejecutar una consulta 

    if query.upper().startswith('SELECT'): 
        data = pd.DataFrame(cursor.fetchall())   # Traer los resultados de un select 
    else: 
        conn.commit()              # Hacer efectiva la escritura de datos 
        data = None 
    
    columns = [list(i[0] for i in cursor.description)]
    data.columns = columns

    cursor.close()                 # Cerrar el cursor 
    conn.close()                   # Cerrar la conexión 

    return data

# Coneccion a Naucalpan en donde necesitamos la tabla a consultar, fecha de inicio, fecha final, camapaña
def query_naucalpan(table,from_date=None,to_date=None,campana=None):
    conn = mysql.connector.connect(user='estadisticas',
                                   password='estadisticas8474',
                                   host='192.168.15.12',
                                   port=3306,
                                   database='procesos_externos')
    conn.set_charset_collation('latin1')

    cursor = conn.cursor()         # Crear un cursor 

    if campana is None:
        if from_date is None:
            sql_mes = cursor.callproc(table,)
            for result in cursor.stored_results():
                sql_mes = pd.DataFrame(result.fetchall())
        else:
            sql_mes = cursor.callproc(table, [from_date,to_date])
            for result in cursor.stored_results():
                sql_mes = pd.DataFrame(result.fetchall())
    else:
        sql_mes = cursor.callproc(table, [from_date,to_date,campana])
        for result in cursor.stored_results():
                sql_mes = pd.DataFrame(result.fetchall())
    sql_mes = sql_mes.drop_duplicates()
    
    #columns = [list(i[0] for i in cursor.description)]
    #sql_mes.columns = columns

    cursor.close()                 # Cerrar el cursor 
    conn.close()                   # Cerrar la conexión 

    return sql_mes