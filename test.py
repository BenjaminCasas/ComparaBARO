#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 14:54:12 2020

@author: benjamin
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from funciones import leeInfo
info = os.path.dirname(os.path.abspath(__file__))+'/info.txt'
os.system('clear')
# Carga la informacion de los datos
Station,TestDate, Instr_Type, BARO_Ref_ID , BARO_Ref_FILE, BARO_Ref_DT, BARO_Est_ID, BARO_Est_FILE, BARO_Est_DT, Tolerancia, Convolve, Operador = leeInfo(info)

#Tamanyos
A4_W, A4_H = A4
MAR_L, MAR_R = 50, A4_W-50
COL_1, COL_2, COL_3 = 160, A4_W/2, 420

reportFile = 'RESULTADOS/report.pdf'
Titulo     = 'BAROMETER OPERATION TEST'
Test_Ini = '2020-05-12 07:30'
Test_End = '2020-05-12 08:30'
Diff     = '0.245'
Figura_1 = 'RESULTADOS/DIFF_BARO2020-05-07.png'
Figura_2 = 'RESULTADOS/2SERIES_BARO_2020-05-07.png'
Figura_3 = 'RESULTADOS/TOLERA_BARO_2020-05-07.png'


momento = datetime.now()
momento= momento.strftime('%Y-%m-%d %H:%M')

#Crea el documento
report = canvas.Canvas(reportFile, pagesize=A4)

#Colocal la cabecera
report.drawImage('RECURSOS/encabezado.png',0 , 739.3097, width=A4_W, height=102.58)

#Coloca el título
report.setLineWidth(.3)
report.setFont('Helvetica-Bold', 18)
report.setFillColor('navy')
report.drawCentredString(A4_W/2,A4_H-140, Titulo)
report.setFillColor('black')

#Tabla 1, info del report
report.setStrokeColor('orange')
report.grid([MAR_L,COL_1,COL_2,COL_3,MAR_R],[A4_H-160, A4_H-190, A4_H-220] )

report.setFont('Helvetica-Bold', 14)
report.drawRightString(COL_1-5,A4_H-180, 'Station:')
report.drawRightString(COL_3-5,A4_H-180, 'Date:')
report.drawRightString(COL_1-5,A4_H-210, 'Operator:')

report.setFont('Helvetica', 14)
report.drawString(COL_1+5,A4_H-180, Station)
report.drawString(COL_1+5,A4_H-210, Operador)
report.drawString(COL_3+5,A4_H-180, TestDate)

#Tabla 2, info de los barometros
report.grid([MAR_L,COL_1,COL_2,COL_3,MAR_R],[A4_H-235, A4_H-265, A4_H-295, A4_H-325] )
report.setFont('Helvetica-Bold', 14)
report.drawRightString(COL_1-5,A4_H-255, 'Ref. BARO:')
report.drawRightString(COL_3-5,A4_H-255, 'Last cal. Date:')
report.drawRightString(COL_1-5,A4_H-285, 'Station BARO:')
report.drawRightString(COL_3-5,A4_H-285, 'Last cal. Date:')
report.drawRightString(COL_1-5,A4_H-315, 'Test start:')
report.drawRightString(COL_3-5,A4_H-315, 'Test end:')

report.setFont('Helvetica', 14)
report.drawString(COL_1+5,A4_H-255, BARO_Ref_ID)
report.drawString(COL_1+5,A4_H-285, BARO_Est_ID)
report.drawString(COL_3+5,A4_H-255, BARO_Ref_DT)
report.drawString(COL_3+5,A4_H-285, BARO_Est_DT)
report.drawString(COL_1+5,A4_H-315, Test_Ini)
report.drawString(COL_3+5,A4_H-315, Test_End)

#Tabla 3, Resultado
COL_1, COL_2, COL_3 = 170, A4_W/2, 460
report.setFont('Helvetica-Bold', 16)
report.drawCentredString(A4_W/2,A4_H-355, 'RESULT')
report.grid([MAR_L,COL_1,COL_2,COL_3,MAR_R],[A4_H-360, A4_H-390] )
report.setFont('Helvetica-Bold', 14)
report.drawRightString(COL_1-5,A4_H-380, 'Mean difference:')
report.drawRightString(COL_3-5,A4_H-380, 'Allowable threshold:')
report.setFont('Helvetica', 14)
report.drawCentredString(230,A4_H-380, Diff+' hPa')
report.drawString(COL_3+5,A4_H-380, Tolerancia+' hPa')

report.drawCentredString(A4_W/2,A4_H-430, 'The instrument has passed the test, can continue operative at the station')

#Tabla 4, Figura 1
report.grid([MAR_L,MAR_R],[A4_H-465, A4_H-780])
report.drawImage(Figura_1,60,100, width=460, height=230)

#Pie de página
report.drawImage('RECURSOS/pie.png',0 , 22, width=A4_W, height=21.63)
report.setFont('Helvetica-Bold', 10)
report.drawString(500,10, 'Pg. 1 / 2')
report.setFont('Helvetica-Bold', 8)
report.setFillColor('grey')
report.drawString(50,10, momento+' - '+Operador)



#Termina la página 1
report.showPage()

#Colocal la cabecera
report.drawImage('RECURSOS/encabezado.png',0 , 739.3097, width=A4_W, height=102.58)

#Tabla 5, Figura 2
report.setStrokeColor('orange')
report.grid([MAR_L,MAR_R],[A4_H-470, A4_H-780])
report.drawImage(Figura_2,60,450, width=460, height=230)

#Tabla 6, Figura 3
report.setStrokeColor('orange')
report.grid([MAR_L,MAR_R],[A4_H-120, A4_H-420])
report.drawImage(Figura_3,60,100, width=460, height=230)

#Pie de página
report.drawImage('RECURSOS/pie.png',0 , 22, width=A4_W, height=21.63)
report.setFont('Helvetica-Bold', 10)
report.drawString(500,10, 'Pg. 2 / 2')
report.setFont('Helvetica-Bold', 8)
report.setFillColor('grey')
report.drawString(50,10, momento+' - '+Operador)
#Guarda el docuemnto en un .pdf
report.save()
