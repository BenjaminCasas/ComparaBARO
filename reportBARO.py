# -*- coding: utf-8 -*-
"""
@author: bcasa
"""
VER = "2020-04-28 @bcasas" #Version construida a partir de una antigua
#%% IMPORTAL LAS LIBRERIAS QUE SE UTILIZARAN EN EL SCRIPT
import os
from funciones import leeInfo, leeBaro, SUB_SERIES, Plt_SERIE, Plt_2_SERIES, Plt_DIFF, Plt_TOLERA, CONVO, BARO_Report
info = os.path.dirname(os.path.abspath(__file__))+'/info.txt'
###############################################################################
#
#
#%% COMIENZA EL PROCESO
os.system('clear')
print ('         -Compara BAROMETROS- | Version:'+VER)
# Carga la informacion de los datos
Station,TestDate, Instr_Type, BARO_Ref_ID, BARO_Ref_FILE, BARO_Ref_DT, BARO_Est_ID, BARO_Est_FILE, BARO_Est_DT, Tolerancia, Convolve, Operador = leeInfo(info)
# Muestra por pantalla la info de los datos que se van a analizar
print()
print('*Se van a realizar una comparacion de '+Instr_Type+'S')
print('*Los datos proceden de la estacion: '+Station)
print('*Las medidas se realizaron en fecha: '+TestDate)
print('*El '+Instr_Type+' de referencia es: '+BARO_Ref_ID)
print('*El '+Instr_Type+' de la estacion es: '+BARO_Est_ID)
# Carga los datos del BARO de referencia y de la estacion
Dir      = os.getcwd()
File_Ref = Dir+'/'+BARO_Ref_FILE
File_Est = Dir+'/'+BARO_Est_FILE
[Timeline_Ref,Pres_Ref] = leeBaro(File_Ref)
[Timeline_Est,Pres_Est] = leeBaro(File_Est)
SUB_Timeline_Ref, SUB_Pres_Ref, SUB_Timeline_Est, SUB_Pres_Est = SUB_SERIES (Timeline_Ref, Pres_Ref, Timeline_Est, Pres_Est)
if (Convolve != '0'):
    CONV_SUB_Timeline_Ref,CONV_SUB_Pres_Ref = CONVO (SUB_Timeline_Ref, SUB_Pres_Ref, Convolve)
    CONV_SUB_Timeline_Est,CONV_SUB_Pres_Est = CONVO (SUB_Timeline_Est, SUB_Pres_Est, Convolve)


#  Hace la grafica de las dos series
#Plt_SERIE(Station, TestDate, Instr_Type, Timeline_Ref, Pres_Ref, BARO_Ref_ID, 'Atm. Pressure (hPa)')
Plt_2_SERIES('RESULTADOS/Figura_1.png',Station, TestDate, Instr_Type, Timeline_Ref, Pres_Ref, BARO_Ref_ID+' - Referencia', Timeline_Est, Pres_Est, BARO_Est_ID+' - '+Station,'Atm. Pressure (hPa)')
#Plt_TOLERA(Station, TestDate, Instr_Type, Timeline_Ref, Pres_Ref, BARO_Ref_ID, Timeline_Est, Pres_Est, BARO_Est_ID,Tolerancia,'Atm. Pressure (hPa)')
#Plt_DIFF(Station,TestDate,Instr_Type,SUB_Timeline_Ref,SUB_Pres_Ref,BARO_Est_ID,SUB_Timeline_Est,SUB_Pres_Est,BARO_Est_ID, Tolerancia, 'Atm. Pressure (hPa)')
Plt_2_SERIES('RESULTADOS/Figura_2.png',Station, TestDate, Instr_Type, SUB_Timeline_Ref, SUB_Pres_Ref, BARO_Ref_ID, CONV_SUB_Timeline_Ref, CONV_SUB_Pres_Ref, 'Convolucion ('+Convolve+') '+BARO_Ref_ID,'Atm. Pressure (hPa)')
Plt_2_SERIES('RESULTADOS/Figura_3.png',Station, TestDate, Instr_Type, SUB_Timeline_Est, SUB_Pres_Est, BARO_Est_ID, CONV_SUB_Timeline_Est, CONV_SUB_Pres_Est, 'Convolucion ('+Convolve+') '+BARO_Est_ID,'Atm. Pressure (hPa)')
Plt_2_SERIES('RESULTADOS/Figura_4.png',Station, TestDate, Instr_Type, CONV_SUB_Timeline_Ref, CONV_SUB_Pres_Ref, 'Convolucion ('+Convolve+') '+BARO_Ref_ID, CONV_SUB_Timeline_Est, CONV_SUB_Pres_Est, 'Convolucion ('+Convolve+') '+BARO_Est_ID,'Atm. Pressure (hPa)')
Plt_TOLERA('RESULTADOS/Figura_5.png',Station, TestDate, Instr_Type, CONV_SUB_Timeline_Ref, CONV_SUB_Pres_Ref, BARO_Ref_ID, CONV_SUB_Timeline_Est, CONV_SUB_Pres_Est, BARO_Est_ID,Tolerancia,'Atm. Pressure (hPa)')
Diff = Plt_DIFF('RESULTADOS/Figura_6.png',Station,TestDate,Instr_Type,CONV_SUB_Timeline_Ref,CONV_SUB_Pres_Ref,BARO_Est_ID,CONV_SUB_Timeline_Est,CONV_SUB_Pres_Est,BARO_Est_ID, Tolerancia, 'Atm. Pressure (hPa)')
Test_Ini = CONV_SUB_Timeline_Ref[0]
Test_Ini = Test_Ini.strftime('%Y-%m-%d %H:%M')
Test_End = CONV_SUB_Timeline_Ref[len(CONV_SUB_Timeline_Ref)-1]
Test_End = Test_End.strftime('%Y-%m-%d %H:%M')
BARO_Report ('RESULTADOS/report.pdf', Station, TestDate, Operador, BARO_Ref_ID, BARO_Ref_DT, BARO_Est_ID, BARO_Est_DT, Test_Ini, Test_End, Diff, Tolerancia,'RESULTADOS/Figura_6.png', 'RESULTADOS/Figura_1.png', 'RESULTADOS/Figura_5.png')
###############################################################################


#%% FINAL
print()
print()
print()