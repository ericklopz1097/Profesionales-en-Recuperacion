rm(list = ls(all=T))

install.packages("plyr")
#install.packages('reshape2')

library(plyr)
library(ggplot2) 
library(reshape2)
library(rpivotTable)
#library(RJDBC)
library(dplyr)
library(sqldf)
library(openxlsx)
library(tidyr)
library(data.table)
library(janitor)
library(tidyverse)
library(lubridate)
library(datos)

n_factc0 <- left_join(facturacionc0,asignacion2020[,c("NUMERO_CUENTA","NUMERO_TARJETA")], by = c("TARJETA"="NUMERO_CUENTA"))
n_factc0$FECHA <- excel_numeric_to_date(n_factc0$FECHA)
n_factc0 <- n_factc0[!duplicated(n_factc0),]
n_factc0[is.na(n_factc0)] <- 0
n_factc0$TARJETA <- ifelse(n_factc0$NUMERO_TARJETA>0,n_factc0$NUMERO_TARJETA,n_factc0$TARJETA)
n_factc0 <- n_factc0[,c(1,2,3,4,5,6,7,8,9,10,11)]



ba1 <- read.xlsx("C:\\Users\\LENOVO T520\\Documents\\ERICK\\ASIGNACION_C0_N\\ASIGNACION C0 2017.xlsx", sheet = 1)
ba2 <- read.xlsx("C:\\Users\\LENOVO T520\\Documents\\ERICK\\ASIGNACION_C0_N\\ASIGNACION C0 2018.xlsx", sheet = 1)
ba3 <- read.xlsx("C:\\Users\\LENOVO T520\\Documents\\ERICK\\ASIGNACION_C0_N\\ASIGNACION C0 2019.xlsx", sheet = 1)
ba4 <- read.xlsx("C:\\Users\\LENOVO T520\\Documents\\ERICK\\ASIGNACION_C0_N\\ASIGNACION C0 2020.xlsx", sheet = 1)


asignacion <- rbind(ba1,ba2)
asignacion <- rbind(asignacion,ba3)
asignacion <- rbind(asignacion,ba4)
asignacion$MES.ASIGNACION <- excel_numeric_to_date(asignacion$MES.ASIGNACION)
asignacion <- asignacion[!duplicated(asignacion),]




dash <- consolidadoG %>% arrange(desc(MES))
dash <- dash[1:250000,]

write.xlsx(dash,"C:\\Users\\LENOVO T520\\Documents\\ERICK\\DASHBOARD C0.xlsx",row.names = FALSE, colNames = TRUE)









new_asignacion <- read.xlsx(paste0("", ruta,"\\ASIGNACION C0 ", mes_actual,".xlsx"), sheet = 1 )
new_asignacion$MES <- excel_numeric_to_date(new_asignacion$MES)

asig_nov <- rbind(asignacionc0,new_asignacion)

asig_nov$CONTEO <- ddply(asig_nov)



install.packages("DBI", repos = "https://cran.microsoft.com/snapshot/2019-01-01")
install.packages("dplyr", repos = "https://cran.microsoft.com/snapshot/2019-01-01")
install.packages("sparklyr", repos = "https://cran.microsoft.com/snapshot/2019-01-01")












