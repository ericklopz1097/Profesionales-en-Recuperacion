import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
from datetime import date
from datetime import datetime
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

#Definimos la ruta en donde queremos guardar los archivos
ruta = '/home/estadistico/Documents/Erick/Reportes diarios/Promesas Diarias'
#Definimos la ruta donde estan las asignaciones
ruta_asig_baz = '/home/estadistico/Documents/Erick/Banco Azteca/Asignacion csv'
mes2 = 'Diciembre2020'

