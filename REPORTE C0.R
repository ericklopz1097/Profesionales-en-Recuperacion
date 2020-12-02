rm(list = ls(all=T))

#install.packages("stringi")
#install.packages('reshape2')

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

ruta <- "C:\\Users\\LENOVO T520\\Documents\\ERICK\\ASIGNACION_C0_N"
mes_actual <- "NOVIEMBRE2020"
mes_pasado <- "OCTUBRE2020"


#new_asignacion <- read.xlsx(paste0("", ruta,"\\ASIGNACION C0 ", mes_actual,".xlsx"), sheet = 1 )
asignacion_ant <- read.xlsx(paste0("", ruta,"\\ASIGNACION C0.xlsx"), sheet = 1)
asignacionc0 <- data.frame()
asignacionc0 <- rbind(asignacionc0,asignacion_ant)
#asignacionc0 <- rbind(asignacionc0,asignacion_nueva)
asignacionc0$MES <- excel_numeric_to_date(asignacionc0$MES)
asignacionc0 <- asignacionc0[!duplicated(asignacionc0),]
#write.csv(asignacionc0,"C:\\Users\\LENOVO T520\\Documents\\ERICK\\ASIGNACION_C0_N\\ASIGNACION C0",row.names = FALSE)

#Leemos el archivo donde tenemos todas nuestras facturaciones

# facturacionc0ca <- read.xlsx(paste0("C:\\Users\\LENOVO T520\\Documents\\ERICK\\FACTURACION_C0_N\\FACTURACION C0 ", mes_pasado,".xlsx"), sheet = 1 )
# facturacionc0so <- read.xlsx(paste0("C:\\Users\\LENOVO T520\\Documents\\ERICK\\FACTURACION_C0_N\\FACTURACION C0 ", mes_pasado,".xlsx"), sheet = 2 )
# facturacionc0_new <- rbind(facturacionc0ca,facturacionc0so)
# facturacionc0_new$MES <- excel_numeric_to_date(facturacionc0_new$MES)

facturacionc0_ant <- read.xlsx(paste0("C:\\Users\\LENOVO T520\\Documents\\ERICK\\FACTURACION_C0_N\\FACTURACION C0.xlsx"), sheet = 1)
facturacionc0 <- data.frame()
facturacionc0 <- rbind(facturacionc0,facturacionc0_ant)
#facturacionc0 <- rbind(facturacionc0,facturacionc0_new)
facturacionc0$MES <- excel_numeric_to_date(facturacionc0$MES)
facturacionc0 <- facturacionc0[!duplicated(facturacionc0),]
#write.xlsx(facturacionc0,"C:\\Users\\LENOVO T520\\Documents\\ERICK\\FACTURACION_C0_N\\FACTURACION C0.xlsx",row.names = FALSE)

#Arreglamos los casos en los que num_cliente es num_tarjeta

n_factc0 <- left_join(facturacionc0,asignacionc0[,c("NUMERO_CUENTA","NUMERO_TARJETA","MES")], by = c("TARJETA"="NUMERO_CUENTA","MES"))
n_factc0$FECHA <- excel_numeric_to_date(n_factc0$FECHA)
n_factc0 <- n_factc0[!duplicated(n_factc0),]
n_factc0[is.na(n_factc0)] <- 0
n_factc0$TARJETA <- ifelse(n_factc0$NUMERO_TARJETA>0,n_factc0$NUMERO_TARJETA,n_factc0$TARJETA)
n_factc0 <- n_factc0[,c(1,2,3,4,5,6,7,8,9,10,11)]

#comenzamos juntando ambos archivos

consolidado <- left_join(asignacionc0,n_factc0, by = c("NUMERO_TARJETA"="TARJETA","MES"))
consolidado <- consolidado[!duplicated(consolidado),]
consolidado$PAG_VENC <- ifelse(consolidado$PAGOSVENCIDOS == "C0 (HOYO NEGRO II)",6,substr(consolidado$PAGOSVENCIDOS,4,4))

#analizaremos el volumen de cartera 

volumen_cartera <- consolidado %>% group_by(MES,CODIGO_ORG) %>% summarize(VOLUM_CAR = n()) 
g_vol_cartera <- ggplot(volumen_cartera, aes(MES,VOLUM_CAR, color = CODIGO_ORG)) + geom_line() + ggtitle("VOL CARTERA") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_vol_cartera
#ggsave(grafica_vol_cartera, device = "pdf")

#Ahora el volumen de pagos

volumen_pagos <- consolidado %>% drop_na(PRODUCTO) %>%  group_by(MES,CODIGO_ORG) %>% summarize(VOLUM_PAG = n()) 
g_vol_pagos <- ggplot(volumen_pagos, aes(MES,VOLUM_PAG, color = CODIGO_ORG)) + geom_line() + ggtitle("VOL PAGOS") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_vol_pagos

#Eficiencia en cuanto a volumen de cartera

efic_vol_cartera <- left_join(volumen_pagos,volumen_cartera,by = c("MES","CODIGO_ORG"))
#efic_vol_cartera <- efic_vol_cartera %>% drop_na()
efic_vol_cartera$EFICIENCIA <- efic_vol_cartera$VOLUM_PAG/efic_vol_cartera$VOLUM_CAR
efic_vol_cartera$EFICIENCIA <- as.numeric(efic_vol_cartera$EFICIENCIA)
efic_vol_cartera <- efic_vol_cartera %>% filter(CODIGO_ORG != "BRADESCARD")
g_efic_vol <- ggplot(efic_vol_cartera, aes(MES,EFICIENCIA, color = CODIGO_ORG)) + geom_line() + ggtitle("EFICIENCIA VOLUMEN") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_efic_vol

#Trabajaremos eficiencia de cartera por pagos vencidos

vol_car_pv <- consolidado %>% group_by(MES,PAG_VENC) %>% summarize(VOLUM_CAR = n()) 
g_vol_car_pv <- ggplot(vol_car_pv, aes(MES,VOLUM_CAR, color = PAG_VENC)) + geom_line() + ggtitle("VOL CART PV") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_vol_car_pv

vol_pagos_pv <- consolidado %>% drop_na(PAGO) %>% group_by(MES,PAG_VENC) %>% summarize(VOLUM_PAG = n()) 
g_vol_pagos_pv <- ggplot(vol_pagos_pv, aes(MES,VOLUM_PAG, color = PAG_VENC)) + geom_line() + ggtitle("VOL PAGOS PV") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_vol_pagos_pv

efic_vol_pv <- left_join(vol_pagos_pv,vol_car_pv,by = c("MES","PAG_VENC"))
efic_vol_pv$EFICIENCIA <- efic_vol_pv$VOLUM_PAG/efic_vol_pv$VOLUM_CAR
efic_vol_pv$EFICIENCIA <- as.numeric(efic_vol_pv$EFICIENCIA)
g_efic_vol <- ggplot(efic_vol_pv, aes(MES,EFICIENCIA, color = PAG_VENC)) + geom_line() + ggtitle("EFICIENCIA VOLUMEN PV") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_efic_vol

#Veremos la suma de pago

consolidado$PAGO <- as.numeric(consolidado$PAGO)
pago_total <- consolidado %>% drop_na(PAGO) %>% group_by(MES,CODIGO_ORG) %>% summarize(SUM_PAGOS = sum(PAGO))  
g_pago_total <- ggplot(pago_total, aes(MES,SUM_PAGOS, color = CODIGO_ORG)) + geom_line() + ggtitle("SUMA PAGOS") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_pago_total

#Trabajamos con el ticket promedio de deuda

r_ticket_pagos <- consolidado %>% drop_na(PAGO) %>% group_by(MES,CODIGO_ORG) %>% summarize(PAGOS_PROM = mean(PAGO), MEDIANA_PAGOS = median(PAGO), SD_PAGOS = sd(PAGO), PAGO_MIN = min(PAGO), PAGO_MAX = max(PAGO))  
g_ticket_pagos <- ggplot(r_ticket_pagos, aes(MES,PAGOS_PROM, color = CODIGO_ORG)) + geom_line() + ggtitle("PAGO PROMEDIO") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_ticket_pagos

r_ticket_pagos_pv <- consolidado %>% drop_na(PAGO) %>% group_by(MES,PAG_VENC) %>% summarize(PAGOS_PROM = mean(PAGO), MEDIANA_PAGOS = median(PAGO), SD_PAGOS = sd(PAGO), PAGO_MIN = min(PAGO), PAGO_MAX = max(PAGO))  
g_ticket_pagos_pv <- ggplot(r_ticket_pagos_pv, aes(MES,PAGOS_PROM, color = PAG_VENC)) + geom_line() + ggtitle("PAGO PROMEDIO") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_ticket_pagos_pv

#Trabajamos con descuento respecto al salgo total y saldo minimo por codigo

consolidado$PAGO_DESCUENTO <- as.numeric(consolidado$PAGO_DESCUENTO)
consolidado$SALDO_TOTAL <- as.numeric(consolidado$SALDO_TOTAL)
consolidado$DESCUENTO <- 1-(consolidado$PAGO_DESCUENTO/consolidado$SALDO_TOTAL)

r_descuento_codigo <- consolidado %>% group_by(MES,CODIGO_ORG) %>% summarize(DESCUENTO_PROM = mean(DESCUENTO), MEDIANA_DESC = median(DESCUENTO), SD_DESC = sd(DESCUENTO), DESCUENTO_MIN = min(DESCUENTO), DESCUENTO_MAX = max(DESCUENTO))
g_descuento_codigo <- ggplot(r_descuento_codigo, aes(MES,DESCUENTO_PROM, color = CODIGO_ORG)) + geom_line() + ggtitle("DESCUENTO PROMEDIO COD") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month")  +theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_descuento_codigo

#Trabajamos con descuento respecto al salgo total y saldo minimo por morocidad en porcentaje

r_descuento_pv <- consolidado %>% drop_na(PAGO) %>% group_by(MES,PAG_VENC) %>% summarize(DESCUENTO_PROM = mean(DESCUENTO), MEDIANA_DESC = median(DESCUENTO), SD_DESC = sd(DESCUENTO), DESCUENTO_MIN = min(DESCUENTO), DESCUENTO_MAX = max(DESCUENTO))
g_descuento_pv <- ggplot(r_descuento_pv, aes(MES,DESCUENTO_PROM, color = PAG_VENC)) + geom_line() + ggtitle("DESCUENTO PROMEDIO PV%") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_descuento_pv

#Trabajamos con descuento respecto al salgo total y saldo minimo por morocidad cantidad promedio

r_min_req_pv <- consolidado %>% drop_na(PAGO) %>% group_by(MES,PAG_VENC) %>% summarize(PAGO_MIN = mean(PAGO_DESCUENTO), MEDIANA_DESC = median(PAGO_DESCUENTO), SD_DESC = sd(PAGO_DESCUENTO), DESCUENTO_MIN = min(PAGO_DESCUENTO), DESCUENTO_MAX = max(PAGO_DESCUENTO)) 
g_r_min_req_pv <- ggplot(r_min_req_pv, aes(MES,PAGO_MIN, color = PAG_VENC)) + geom_line() + ggtitle("PAGO DESCUENTO PROMEDIO PV") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_r_min_req_pv

#Trabajamos con el ticket promedio de deuda por codigo

r_ticket_deuda <- consolidado %>% filter(CODIGO_ORG != "BRADESCARD") %>% group_by(MES,CODIGO_ORG) %>% summarize(DEUDA_PROM = mean(SALDO_TOTAL), MEDIANA_DEUDA = median(SALDO_TOTAL), SD_DEUDA = sd(SALDO_TOTAL), DEUDA_MIN = min(SALDO_TOTAL), DEUDA_MAX = max(SALDO_TOTAL))
g_ticket_deuda <- ggplot(r_ticket_deuda, aes(MES,DEUDA_PROM, color = CODIGO_ORG)) + geom_line() + ggtitle("DEUDA PROMEDIO COD") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_ticket_deuda

#Trabajamos con el ticket promedio de deuda por codigo

r_ticket_deuda_pv <- consolidado %>% group_by(MES,PAG_VENC) %>% summarize(DEUDA_PROM = mean(SALDO_TOTAL), MEDIANA_DEUDA = median(SALDO_TOTAL), SD_DEUDA = sd(SALDO_TOTAL), DEUDA_MIN = min(SALDO_TOTAL), DEUDA_MAX = max(SALDO_TOTAL))
g_ticket_deuda_pv <- ggplot(r_ticket_deuda_pv, aes(MES,DEUDA_PROM, color = PAG_VENC)) + geom_line() + ggtitle("DEUDA PROMEDIO PV") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_ticket_deuda_pv



##############ES MOMENTO DE VER GEOGRAFICAMENTE###############

ciudades_imp <- read.xlsx("C:\\Users\\LENOVO T520\\Documents\\ERICK\\CIUDADES_IMPORTANTES.xlsx", sheet = 1)
ciudades_imp$CIUDAD <- chartr("ÁÉÍÓÚ", "AEIOU", toupper(ciudades_imp$CIUDAD))
consolidado$CIUDAD <- chartr("ÁÉÍÓÚ", "AEIOU", toupper(consolidado$CIUDAD))

consolidadoG <- left_join(consolidado,ciudades_imp, by = "CIUDAD")
consolidadoG <- consolidadoG[!duplicated(consolidadoG),]
consolidadoG$IMPORTANCIA[is.na(consolidadoG$IMPORTANCIA)] <- "NO IMPORTANTE"

#Trabajamos con la eficiencia a nivel estado

vol_estado <- consolidadoG %>% group_by(MES,ESTADO) %>% summarize(CARTERA = n())
pago_estado <- consolidadoG %>% drop_na(PAGO) %>% group_by(MES,ESTADO) %>% summarize(PAGO = n())

efic_vol_estado <- left_join(vol_estado,pago_estado,by = c("MES","ESTADO")) %>% drop_na()
efic_vol_estado$EFICIENCIA <- efic_vol_estado$PAGO/efic_vol_estado$CARTERA
efic_vol_estado$EFICIENCIA <- as.numeric(efic_vol_estado$EFICIENCIA)
efic_vol_estado <- efic_vol_estado %>% drop_na(EFICIENCIA)
g_efic_vol_estado <- ggplot(efic_vol_estado, aes(MES,EFICIENCIA, color = ESTADO)) + geom_line() + ggtitle("EFICIENCIA VOLUMEN") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_efic_vol_estado

#Trabajamos con eficiencia ciudades principales y no principales

vol_cds_princ <- consolidadoG %>% group_by(MES,IMPORTANCIA) %>% summarize(VOLUMEN_TOTAL = n())
g_vol_cds_princ <- ggplot(vol_cds_princ, aes(MES,VOLUMEN_TOTAL, color = IMPORTANCIA)) + geom_line() + ggtitle("VOLUMEN CDS PRIN") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_vol_cds_princ

pagos_cds_princ <- consolidadoG %>% drop_na(PAGO) %>% group_by(MES,IMPORTANCIA) %>% summarize(VOLUMEN_PAGO = n())
g_pagos_cds_princ <- ggplot(pagos_cds_princ, aes(MES,VOLUMEN_PAGO, color = IMPORTANCIA)) + geom_line() + ggtitle("PAGOS CDS PRINCIPALES") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_pagos_cds_princ

efi_vol_cds_princ <- left_join(vol_cds_princ,pagos_cds_princ,by = c("MES","IMPORTANCIA"))
efi_vol_cds_princ$EFICIENCIA <- efi_vol_cds_princ$VOLUMEN_PAGO/efi_vol_cds_princ$VOLUMEN_TOTAL
g_efi_vol_cds_princ <- ggplot(efi_vol_cds_princ, aes(MES,EFICIENCIA, color = IMPORTANCIA)) + geom_line() + ggtitle("EFICIENCIA VOLUMEN") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_efi_vol_cds_princ


r_cds_princ_st <- consolidadoG %>% group_by(MES,IMPORTANCIA) %>% summarize(DEUDA_PROM = mean(SALDO_TOTAL), MEDIANA_DEUDA = median(SALDO_TOTAL), SD_DEUDA = sd(SALDO_TOTAL), DEUDA_MIN = min(SALDO_TOTAL), DEUDA_MAX = max(SALDO_TOTAL))
g_cds_princ_st <- ggplot(r_cds_princ_st, aes(MES,DEUDA_PROM, color = IMPORTANCIA)) + geom_line() + ggtitle("DEUDA PROM") + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
g_cds_princ_st


r_cp <- consolidadoG %>% group_by(MES,CP) %>% summarize(DEUDA_PROM = mean(SALDO_TOTAL), MEDIANA_DEUDA = median(SALDO_TOTAL), SD_DEUDA = sd(SALDO_TOTAL), DEUDA_MIN = min(SALDO_TOTAL), DEUDA_MAX = max(SALDO_TOTAL))







