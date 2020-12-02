#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 12:21:59 2020

@author: estadistico
"""


import pandas as pd
import numpy as np
import functools as ft 
import csv
import datetime
from dateutil.relativedelta import relativedelta
#import matplotlib.pyplot as plt
#from sklearn.linear_model import LinearRegression

ruta = "/home/estadistico/Documents/Erick/Banco Azteca"

def rango_fechas(desde, hasta):
    return [desde + relativedelta(days=days) for days in range((hasta - desde).days + 1)]

desde = datetime.date(2020,11,1)
hasta = datetime.date(2020,11,30)
periodos = rango_fechas(desde,hasta)
periodos_asignacion = [date_obj.strftime('%d-%m-%Y') for date_obj in periodos]

asignacion_ba = pd.DataFrame() 
for i in periodos_asignacion:
    asignacion = pd.read_excel(''+ruta+'/Asignacion/baz_layout_carga_asignacion_renta_posiciones_'+i+'.xlsx')
    asignacion = asignacion[['#FIIDCAMPANA', 'FIPAIS', 'FICANAL','FISUCURSAL','FIFOLIO','FISEMATRASMAX','FNSALDO','FNSALDOCAPITAL','FNPAGOREQ','FCTEL1','FCTIPO1','FNDIA_PAGO','FIDIASATRASOMAX','FNCAPPAGODISP','FNABONOSEMANAL','FNCAPACIDADPAGO','FILCRACTIVA','FDFECPROXPAG','FNTASAINT','CP','fcnombreos','fcappaternoos','FITERRITORIO','FCDESCTERRITORIO','FIZONA','FCDESCZONA','FIREGION','FCDESCREGION','FIGERENCIA','FCDESCGERENCIA','FCBESTTIMETOCALL']]
    asignacion['FECHA'] = pd.to_datetime(i)
    asignacion['FECHA'] = asignacion['FECHA'].dt.strftime('%d/%m/%Y')
    asignacion_ba.reset_index(drop=True, inplace=True)
    asignacion.reset_index(drop=True, inplace=True)
    asignacion_ba = pd.concat([asignacion_ba, asignacion], ignore_index=True)
    print(i)
asignacion_ba.drop_duplicates(subset=['#FIIDCAMPANA', 'FIPAIS', 'FICANAL','FISUCURSAL','FIFOLIO','FISEMATRASMAX','FNSALDO','FNSALDOCAPITAL','FNPAGOREQ','FCTEL1','FCTIPO1','FNDIA_PAGO','FIDIASATRASOMAX','FNCAPPAGODISP','FNABONOSEMANAL','FNCAPACIDADPAGO','FILCRACTIVA','FDFECPROXPAG','FNTASAINT','CP','fcnombreos','fcappaternoos','FITERRITORIO','FCDESCTERRITORIO','FIZONA','FCDESCZONA','FIREGION','FCDESCREGION','FIGERENCIA','FCDESCGERENCIA','FCBESTTIMETOCALL'],keep=False,inplace=True)

asignacion_ba.to_csv(''+ruta+'/Asignacion_csv/Asignacion banco azteca Noviembre2020.csv', index = False, header=True)

