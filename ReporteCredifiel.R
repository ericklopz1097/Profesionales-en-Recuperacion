rm(list = ls(all=T))

#install.packages("eeptools")
#install.packages('reshape2')

library(eeptools)
library(plyr)
library(stringi)
library(imputeTS)
library(qwraps2)
library(scales)
library(ggplot2) 
library(reshape2)
library(rpivotTable)
library(dplyr)
library(sqldf)
library(openxlsx)
library(tidyr)
library(data.table)
library(janitor)
library(tidyverse)
library(lubridate)
library(datos)
library(csv)

#Primero leemos los archivos asignacion año con año

ruta <- "C:\\Users\\LENOVO T520\\Documents\\ERICK\\"
mes_actual <- "NOVIEMBRE2020"
mes_pasado <- "OCTUBRE2020"

x <- C("DEPENDENCIA","IRR","ESTADO")



asignacion_cred <- read.xlsx(paste0("", ruta,"CREDIFIEL\\CREDIFIEL 2020 ASIGNACION.xlsx"), sheet = 1)
facturacion_cred <- read.xlsx(paste0("", ruta,"CREDIFIEL\\CREDIFIEL 2020 FACTURACION.xlsx"), sheet = 1)

asignacion_cred$MES <- excel_numeric_to_date(asignacion_cred$MES)
asignacion_cred$DAP <- as.numeric(asignacion_cred$DAP)
facturacion_cred$MES <- excel_numeric_to_date(facturacion_cred$MES)
facturacion_cred$DAP <- as.numeric(facturacion_cred$DAP)

asignacion_cred$NACIMIENTO <- substr(asignacion_cred$RFC,5,10)
asignacion_cred$NACIMIENTO <- ifelse(as.numeric(substr(asignacion_cred$NACIMIENTO,1,2))>15,paste0("19", asignacion_cred$NACIMIENTO,""),paste0("20", asignacion_cred$NACIMIENTO,""))
asignacion_cred$EDAD <- year(Sys.Date())-year(as.Date(asignacion_cred$NACIMIENTO,"%Y%m%d"))

consolidado_cred <- left_join(asignacion_cred,facturacion_cred[,c("DAP","IMPORTE")],by=c("DAP"))
consolidado_cred <- consolidado_cred[!duplicated(consolidado_cred),]

facturacion_cred <- left_join(facturacion_cred,asignacion_cred[,c("MES","DAP","ESTADO","IRR","EDAD")],by = c("MES","DAP"))
facturacion_cred <- verificar[!duplicated(verificar),]




################################# EMPEZAMOS A TRABAJAR LAS BASES ############################################

#Volumen cartera

cred_vol_cart <- asignacion_cred %>% group_by(MES,DEPENDENCIA) %>% summarize(VOL_CARTERA = n())

#Volumen pagos

cred_vol_pagos <- facturacion_cred %>% group_by(MES,DEPENDENCIA) %>% summarize(VOL_PAGOS = n())

#Eficiencia en cuanto a volumen

cred_eficiencia_vol <- left_join(cred_vol_pagos,cred_vol_cart,by=c("MES","DEPENDENCIA"))
cred_eficiencia_vol$EFICIENCIA <- cred_eficiencia_vol$VOL_PAGOS/cred_eficiencia_vol$VOL_CARTERA

#Ticket promedio deuda

cred_tp_deuda <- asignacion_cred %>% group_by(MES,DEPENDENCIA) %>% summarise(DEUDA_PROMEDIO = mean(CAPITAL))

#Ticket promedio pago

cred_tp_pago <- facturacion_cred %>% group_by(MES,DEPENDENCIA) %>% summarise(PAGO_PROMEDIO = mean(IMPORTE))

#Descuento promedio

asignacion_cred$CAPITAL <- as.numeric(asignacion_cred$CAPITAL)
asignacion_cred$MONTO.PARA.LIQUIDAR <- as.numeric(asignacion_cred$MONTO.PARA.LIQUIDAR)
asignacion_cred$DESCUENTO <- 1-(asignacion_cred$MONTO.PARA.LIQUIDAR/asignacion_cred$CAPITAL)
cred_descuento_promedio <- asignacion_cred %>% group_by(MES,DEPENDENCIA) %>% summarize(DESCUENTO_PROMEDIO = mean(DESCUENTO))















list_datasets_cred <- list("VolumenCartera" = cred_vol_cart,"VolumenPagos" = cred_vol_pagos,"EficienciaVolumen"=cred_eficiencia_vol,"TicketPromedioDeuda"=cred_tp_deuda,"TicketPromedioPago"=cred_tp_pago,"DescuentoPromedio"=cred_descuento_promedio)
openxlsx::write.xlsx(list_datasets_cred,file = paste0("", ruta,"", mes_actual,"\\REPORTE CREDIFIEL\\DASHBOARD CREDIFIEL.xlsx"),row.names=FALSE,colNames = TRUE)
