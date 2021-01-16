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

#periodos_promesas = ['20200105','20200112','20200119','20200126','20200202','20200203','20200209','20200216','20200301','20200308','20200315','20200316','20200322','20200329']
periodos_promesas = os.listdir('C:/Users/LENOVO T520/Downloads/prom')
periodos_promesas = pd.DataFrame(periodos_promesas)
periodos_promesas[0] = periodos_promesas[0].str[14:22]
periodos_promesas[0] = periodos_promesas[0].map(str)
periodos_promesas = periodos_promesas[0].to_list()




for i in periodos_promesas:
    promesas = pd.read_excel('C:/Users/LENOVO T520/Downloads/prom/Prom_Pago_Exi_'+i+'.xlsx')
    promesas = promesas[['FCEMPNUMCORTE','FDFECHAGENPROMESA','FDFECHAPROMESA','FIIDPERIODO','FNMONTOPROMETIDO',	'FNMONTOPAGADO','FDFECHAABONO',	'FNMONTOREQUERIDO',	'CAMPANAID','CAMPANA',	'FNSCOMPROMISO']]
    promesas.to_csv(''+ruta+'PROMESAS PAGO/Prom_Pago_Exi_'+i+'.csv',index = False, header=True)
    print(i)
