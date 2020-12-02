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
#library(sqldf)
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

codigo_correcto <- read.xlsx(paste0("", ruta,"BRADESCO\\CODIGOS_PRO.xlsx"),sheet = 1)

#Hacemos la carga de las asignaciones extrajudiciales

#asignaciones <- c("NOVIEMBRE2020","OCTUBRE2020","SEPTIEMBRE2020","AGOSTO2020","JULIO2020","JUNIO2020","MAYO2020","ABRIL2020","MARZO2020","FEBRERO2020","ENERO2020",
#                  "DICIEMBRE2019","NOVIEMBRE2019","OCTUBRE2019","SEPTIEMBRE2019","AGOSTO2019","JULIO2019","JUNIO2019","MAYO2019","ABRIL2019","MARZO2019","FEBRERO2019","ENERO2019",
#                  "DICIEMBRE2018","NOVIEMBRE2018","OCTUBRE2018","SEPTIEMBRE2018","AGOSTO2018","JULIO2018","JUNIO2018","MAYO2018","ABRIL2018","MARZO2018","FEBRERO2018","ENERO2018",)
asignaciones <- c("OCTUBRE2020","SEPTIEMBRE2020","AGOSTO2020","JULIO2020","JUNIO2020","MAYO2020","ABRIL2020","MARZO2020","FEBRERO2020","ENERO2020",
                  "DICIEMBRE2019","NOVIEMBRE2019","OCTUBRE2019","SEPTIEMBRE2019","AGOSTO2019","JULIO2019","JUNIO2019","MAYO2019","ABRIL2019","MARZO2019","FEBRERO2019","ENERO2019",
                  "DICIEMBRE2018","NOVIEMBRE2018","OCTUBRE2018","SEPTIEMBRE2018","AGOSTO2018")
#asignaciones <- c("OCTUBRE2020","SEPTIEMBRE2020","AGOSTO2020")
asignacion_extra <- read.xlsx(paste0("", ruta,"ASIGNACION_EXTRA_N\\ASIGNACION EXTRA ", mes_actual,".xlsx"),sheet = 1)
for (x in asignaciones) {
  asig_extra <- read.xlsx(paste0("", ruta,"ASIGNACION_EXTRA_N\\ASIGNACION EXTRA ", x,".xlsx"),sheet = 1)
  names(asig_extra) <- names(asignacion_extra)
  asignacion_extra <- rbind(asignacion_extra,asig_extra)
  print(x)
}

asignacion_extra$MES <- excel_numeric_to_date(asignacion_extra$MES)
asignacion_extra <- asignacion_extra[!duplicated(asignacion_extra),]
asignacion_extra$SALDO.TOTAL <- as.numeric(asignacion_extra$SALDO.TOTAL)
asignacion_extra <- left_join(asignacion_extra, codigo_correcto, by = c("PRODUCTO" = "CODIGO"))
asignacion_extra$PRODUCTO <- ifelse(is.na(asignacion_extra$CODIGO.BIEN),asignacion_extra$PRODUCTO, asignacion_extra$CODIGO.BIEN )
asignacion_extra$NACIMIENTO <- as.character(substr(asignacion_extra$RFC,5,10))
asignacion_extra$NACIMIENTO <- ifelse(as.numeric(substr(asignacion_extra$NACIMIENTO,1,2))>15,paste0("19", asignacion_extra$NACIMIENTO,""),paste0("20", asignacion_extra$NACIMIENTO,""))
asignacion_extra$NACIMIENTO <- as.Date(asignacion_extra$NACIMIENTO,"%Y%m%d")
asignacion_extra$EDAD <- year(Sys.Date())-year(asignacion_extra$NACIMIENTO)
asignacion_extra <- asignacion_extra[,c(1,2,3,4,6,8,9,10,11,12,13,14,15,26,27,29,31,32,36,37,40)]

#Hacemos la carga de las facturaciones 

factura_ca <- read.xlsx(paste0("", ruta,"FACTURACION_EXTRA_N\\FACTURACION EXTRA.xlsx"),sheet = 1)
factura_socios <- read.xlsx(paste0("", ruta,"FACTURACION_EXTRA_N\\FACTURACION EXTRA.xlsx"),sheet = 2)
facturacion_extra <- rbind(factura_ca, factura_socios)

#factura_nueva_ca <- read.xlsx(paste0("C:\\Users\\LENOVO T520\\Documents\\ERICK\\FACTURACION_EXTRA_N\\FACTURACION EXTRA", mes_pasado,".xlsx"),sheet = 1)
#factura_nueva_socios <- read.xlsx(paste0("C:\\Users\\LENOVO T520\\Documents\\ERICK\\FACTURACION_EXTRA_N\\FACTURACION EXTRA", mes_pasado,".xlsx"),sheet = 2)
#facturacion_nueva <- rbind(factura_nueva_ca,factura_nueva_socios)
#facturacion_extra <- rbind(facturacion_extra,facturacion_nueva)
facturacion_extra$MES <- excel_numeric_to_date(facturacion_extra$MES)
facturacion_extra <- facturacion_extra[!duplicated(facturacion_extra),]
#write.xlsx(facturacion_extra,"", ruta,"FACTURACION_EXTRA_N\\FACTURACION EXTRA1.xlsx",colNames = TRUE)


facturacion_extra <- left_join(facturacion_extra,codigo_correcto,by = c("PRODUCTO" = "CODIGO"))
facturacion_extra$PRODUCTO <- ifelse(is.na(facturacion_extra$CODIGO.BIEN),facturacion_extra$PRODUCTO, facturacion_extra$CODIGO.BIEN )

facturacion_extra <- left_join(facturacion_extra,asignacion_extra[,c("NUMERO.DE.CUENTA","NUMERO.DE.TARJETA","MES","ESTADO","CIUDAD","EDAD")],by = c("TARJETA"="NUMERO.DE.CUENTA","MES"))
facturacion_extra$TARJETA <- ifelse(is.na(facturacion_extra$NUMERO.DE.TARJETA),facturacion_extra$TARJETA,facturacion_extra$NUMERO.DE.TARJETA)
facturacion_extra <- facturacion_extra[,c(1,2,3,4,5,6,7,9,12,13,14)]
#facturacion_extra$FECHA <- as.numeric(facturacion_extra$FECHA)
#facturacion_extra$FECHA <- excel_numeric_to_date(facturacion_extra$FECHA)
facturacion_extra <- facturacion_extra[!duplicated(facturacion_extra),]

#Ahora juntamos asignacion y facturacion

#consolidado_extra <- left_join(asignacion_extra,facturacion_extra,by = c("NUMERO.DE.TARJETA"="TARJETA","MES","PRODUCTO","TIPO_ASIGNACION"="BUCKET"))
#consolidado_extra <- consolidado_extra[!duplicated(consolidado_extra),]




                                #########Comenzamos viendo el volumen de cartera###########


e_volumen_cartera <- asignacion_extra %>% group_by(MES,ESTADO,TIPO_ASIGNACION) %>% summarize(VOLUMEN_CARTERA = n())
#g_e_volumen_cartera <- ggplot(e_volumen_cartera, aes(MES,VOLUMEN_CARTERA, color = TIPO_ASIGNACION)) + ggtitle("VOLUMEN CARTERA") + geom_line() + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
#g_e_volumen_cartera

#Veremos el volumen de pagos

e_volumen_pagos <- facturacion_extra %>% group_by(MES,ESTADO,BUCKET) %>% summarize(VOLUMEN_PAGOS = n())
#g_e_volumen_pagos <- ggplot(e_volumen_pagos, aes(MES,VOLUMEN_PAGOS, color = BUCKET)) + ggtitle("VOLUMEN PAGOS") + geom_line() + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
#g_e_volumen_pagos

#Obtenemos la eficiencia de los pagos respecto a la cartera

e_eficiencia_volumen <- left_join(e_volumen_cartera,e_volumen_pagos,by=c("MES","TIPO_ASIGNACION"="BUCKET","ESTADO"))
e_eficiencia_volumen$VOLUMEN_PAGOS[is.na(e_eficiencia_volumen$VOLUMEN_PAGOS)] <- 0
e_eficiencia_volumen$EFICIENCIA <- e_eficiencia_volumen$VOLUMEN_PAGOS/e_eficiencia_volumen$VOLUMEN_CARTERA
#g_e_eficiencia_volumen <- ggplot(e_eficiencia_volumen, aes(MES,EFICIENCIA, color = TIPO_ASIGNACION)) + ggtitle("EFICIENCIA VOLUMEN") + geom_line() + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
#g_e_eficiencia_volumen

#Ticket promedio de deuda

e_ticket_promedio_deuda <- asignacion_extra %>% group_by(MES,ESTADO,TIPO_ASIGNACION) %>% summarize(DEUDA_PROMEDIO = mean(SALDO.TOTAL))
#g_e_ticket_promedio_deuda <- ggplot(e_ticket_promedio_deuda, aes(MES,DEUDA_PROMEDIO, color = TIPO_ASIGNACION)) + ggtitle("TICKET PROMEDIO DEUDA") + geom_line() + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
#g_e_ticket_promedio_deuda

#Ticket promedio pago

e_ticket_promedio_pago <- facturacion_extra %>% group_by(MES,ESTADO,BUCKET) %>% summarize(PAGO_PROMEDIO = mean(PAGO))
#g_e_ticket_promedio_pago <- ggplot(e_ticket_promedio_pago, aes(MES,PAGO_PROMEDIO, color = BUCKET)) + ggtitle("TICKET PROMEDIO PAGO") + geom_line() + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
#g_e_ticket_promedio_pago

#Descuento promedio

asignacion_extra$PAGO_DESCUENTO <- as.numeric(asignacion_extra$PAGO_DESCUENTO)
asignacion_extra$SALDO.TOTAL <- as.numeric(asignacion_extra$SALDO.TOTAL)
asignacion_extra$DESCUENTO <- 1-(asignacion_extra$PAGO_DESCUENTO/asignacion_extra$SALDO.TOTAL)
e_descuento_promedio <- asignacion_extra %>% group_by(MES,ESTADO,TIPO_ASIGNACION) %>% summarize(DESCUENTO_PROMEDIO = mean(DESCUENTO))

#Ciudades importantes

ciudades_imp <- read.xlsx(paste0("", ruta,"CIUDADES_IMPORTANTES.xlsx"), sheet = 1)
ciudades_imp$CIUDAD <- chartr("ÁÉÍÓÚ", "AEIOU", toupper(ciudades_imp$CIUDAD))
asignacion_extra$CIUDAD <- chartr("ÁÉÍÓÚ", "AEIOU", toupper(asignacion_extra$CIUDAD))
facturacion_extra$CIUDAD <- chartr("ÁÉÍÓÚ", "AEIOU", toupper(facturacion_extra$CIUDAD))

asignacion_extra2 <- left_join(asignacion_extra,ciudades_imp, by = "CIUDAD")
asignacion_extra2 <- asignacion_extra2[!duplicated(asignacion_extra2),]
asignacion_extra2$IMPORTANCIA[is.na(asignacion_extra2$IMPORTANCIA)] <- "NO IMPORTANTE"

facturacion_extra2 <- left_join(facturacion_extra,ciudades_imp, by = "CIUDAD")
facturacion_extra2 <- facturacion_extra2[!duplicated(facturacion_extra2),]
facturacion_extra2$IMPORTANCIA[is.na(facturacion_extra2$IMPORTANCIA)] <- "NO IMPORTANTE"

e_volumen_cart_cidimp <- asignacion_extra2 %>% group_by(MES,ESTADO,IMPORTANCIA,TIPO_ASIGNACION) %>% summarize(VOLUMEN_CARTERA = n())
#g_e_volumen_cart_cidimp <- ggplot(e_volumen_cart_cidimp, aes(MES,VOLUMEN_CARTERA, color = IMPORTANCIA)) + ggtitle("VOLUMEN CARTERA") + geom_line() + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
#g_e_volumen_cart_cidimp

e_volumen_pagos_cidimp <- facturacion_extra2 %>% group_by(MES,ESTADO,IMPORTANCIA,BUCKET) %>% summarize(VOLUMEN_PAGOS = n())
#g_e_volumen_pagos_cidimp <- ggplot(e_volumen_pagos_cidimp, aes(MES,VOLUMEN_CARTERA, color = IMPORTANCIA)) + ggtitle("VOLUMEN PAGOS") + geom_line() + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
#g_e_volumen_pagos_cidimp

e_eficiencia_cdsipm <- left_join(e_volumen_cart_cidimp,e_volumen_pagos_cidimp,by=c("MES","ESTADO","IMPORTANCIA","TIPO_ASIGNACION"="BUCKET"))
e_eficiencia_cdsipm$VOLUMEN_PAGOS[is.na(e_eficiencia_cdsipm$VOLUMEN_PAGOS)] <- 0
e_eficiencia_cdsipm$EFICIENCIA <- e_eficiencia_cdsipm$VOLUMEN_PAGOS/e_eficiencia_cdsipm$VOLUMEN_CARTERA
#g_e_eficiencia_cdsipm <- ggplot(e_eficiencia_cdsipm, aes(MES,EFICIENCIA, color = IMPORTANCIA)) + ggtitle("VOLUMEN CARTERA") + geom_line() + scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") + theme(axis.text.x = element_text(angle = 90, hjust = 1))
#g_e_eficiencia_cdsipm






list_of_datasets <- list("VolumenCartera" = e_volumen_cartera,"VolumenPagos" = e_volumen_pagos,"EficienciaVolumen"=e_eficiencia_volumen,"TicketPromedioDeuda"=e_ticket_promedio_deuda,"TicketPromedioPago"=e_ticket_promedio_pago,"DescuentoPromedio"=e_descuento_promedio,"VolCarteraCds"=e_volumen_cart_cidimp,"VolPagosCds"=e_volumen_pagos_cidimp,
                         "EficienciaCdsImp"=e_eficiencia_cdsipm)
openxlsx::write.xlsx(list_of_datasets,file = paste0("", ruta,"", mes_actual,"\\REPORTE EXTRA\\DASHBOARD EXTRA.xlsx"),row.names=FALSE,colNames = TRUE)

