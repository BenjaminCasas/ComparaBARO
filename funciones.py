#LEE LA INFORMACION DEL FICHERO 'info.txt'###################
def leeInfo(info):
    f_info    = open(info, 'r')
    datos     = f_info.readlines()
    Station   = datos[0].split('"')[1]
    TestDate  = datos[1].split('"')[1]
    Instr_TP  = datos[2].split('"')[1]    
    InsRef_ID = datos[3].split('"')[1]
    InsRef_DR = datos[4].split('"')[1]
    InsRef_DT = datos[5].split('"')[1]
    InsEst_ID = datos[6].split('"')[1]
    InsEst_DR = datos[7].split('"')[1]
    InsEst_DT = datos[8].split('"')[1]
    Toler     = datos[9].split('"')[1]
    Convolve  = datos[10].split('"')[1]
    Operator  = datos[11].split('"')[1]
    del datos
    return Station,TestDate, Instr_TP, InsRef_ID, InsRef_DR, InsRef_DT, InsEst_ID, InsEst_DR, InsEst_DT, Toler, Convolve, Operator
#############################################################
#
#
#%% FUNCION DE LECTURA DE DATOS
def leeBaro(DIR):
    import os
    import numpy as np
    from datetime import datetime

#Prepara variables
    LIST_FILES = []   
    TIMELINE   = []
    PRESION    = []
#Lista con todos los ficheros del directorio:
    LIST_DIR   = os.walk(DIR)   #os.walk()Lista directorios y ficheros
#Crea una lista de los ficheros ail que existen en el directorio y los incluye a la lista.
    for root, dirs, files in LIST_DIR:
        for FILE in files:
            (FILE_NAME, EXT) = os.path.splitext(FILE)
            if(EXT == ".ail"):
                LIST_FILES.append(FILE_NAME+EXT)     
        N_FILES = len(LIST_FILES)            
        print ("Se han encomntrado ", N_FILES," ficheros en el directorio "+DIR)
#Lee los datos
    for N in range (N_FILES): 
        FILE  = DIR+LIST_FILES[N]
        DATOS = np.genfromtxt(FILE, dtype=bytes).astype(str)
        PRESION.extend(list(map(float,DATOS[:,3])))
        for i in range(len(DATOS)):
            TIMELINE.append (datetime.strptime(DATOS[i,0]+' '+DATOS[i,1], '%Y-%m-%d %H:%M:%S'))
        del FILE, DATOS
    return TIMELINE, PRESION
###############################################################################
#
#
#%% FUNCION DE CREACION DE GRAFICA UNA SERIE TEMPORAL
def Plt_SERIE (FILENAME,STATION,DATE,INSTR,TIMELINE,VAR,INSTR_ID,Y_LABEL):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(TIMELINE, VAR)
    hours = mdates.HourLocator(interval = 3)  #
    date_form = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(date_form)
    plt.title (INSTR+' en '+STATION)
    plt.xlabel (DATE)
    plt.ylabel (Y_LABEL)
    plt.legend([INSTR_ID])
    plt.grid(True)
    plt.savefig(FILENAME, bbox_inches='tight')
#    plt.show()
###############################################################################
#
#
#%% FUNCION DE CREACION DE GRAFICA DOS SERIES
def Plt_2_SERIES (FILENAME,STATION,DATE,INSTR,TIMELINE_1,VAR_1,INST_ID_1,TIMELINE_2,VAR_2,INST_ID_2,Y_LABEL):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    fig, ax = plt.subplots(figsize=(10,5))
    plt.plot(TIMELINE_1,VAR_1)
    plt.plot(TIMELINE_2,VAR_2,'r')
    hours = mdates.HourLocator(interval = 3)  #
    date_form = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(date_form)
    plt.title (INSTR+'S en '+STATION+' en fecha '+DATE)
    plt.ylabel (Y_LABEL)
    plt.xlabel (DATE)
    plt.legend([INST_ID_1, INST_ID_2])
    plt.grid(True)
    plt.savefig(FILENAME, bbox_inches='tight')
#    plt.show()
###############################################################################
#
#
#%% FUNCION PARA ENCONTRAR EL INDICE MAS CERCANO ##############################
def find_nearest(array, value):
    import numpy as np 
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx
###############################################################################
#
#
#%% FUNCION PARA HACER CONVOLUCIÓN DE UNA SERIE ###############################
def CONVO(TIMELINE, VAR, CONVO):
    import math
    import numpy as np 
    CONVO = int(CONVO)
    CONV_VAR      = np.convolve(VAR, np.ones((CONVO,))/CONVO, mode='valid')
    CONV_TIMELINE = TIMELINE[math.floor(CONVO/2):len(TIMELINE)-math.floor(CONVO/2)]
    return CONV_TIMELINE, CONV_VAR
###############################################################################
#
#
#%% BUSCA LA SUBSERIE COINCIDENTE DE DOS SERIES TEMPORALES ####################    
def SUB_SERIES (TIMELINE_1, VAR_1, TIMELINE_2, VAR_2):
    
    if (TIMELINE_1[1] > TIMELINE_2[1]):
        TIMELINE_INI = TIMELINE_1[1]
    else:
        TIMELINE_INI = TIMELINE_2[1]

    if (TIMELINE_1[len(TIMELINE_1)-1] < TIMELINE_2[len(TIMELINE_2)-1]):
        TIMELINE_END = TIMELINE_1[len(TIMELINE_1)-1]
    else:
        TIMELINE_END = TIMELINE_2[len(TIMELINE_2)-1]
        
    IND_INI_1     = find_nearest(TIMELINE_1, TIMELINE_INI)
    IND_FIN_1     = find_nearest(TIMELINE_1, TIMELINE_END)
    SB_TIMELINE_1 = TIMELINE_1[IND_INI_1:IND_FIN_1]
    SB_VAR_1      = VAR_1[IND_INI_1:IND_FIN_1]
    IND_INI_2     = find_nearest(TIMELINE_2, TIMELINE_INI)
    IND_FIN_2     = find_nearest(TIMELINE_2, TIMELINE_END)
    SB_TIMELINE_2 = TIMELINE_2[IND_INI_2:IND_FIN_2]
    SB_VAR_2      = VAR_2[IND_INI_2:IND_FIN_2]
    
    return SB_TIMELINE_1, SB_VAR_1, SB_TIMELINE_2, SB_VAR_2
###############################################################################
#
#
#%% FUNCION DE CREACION DE GRAFICA DIFERENCIAS
def Plt_DIFF (FILENAME,STATION,DATE,INSTR,TIMELINE_REF,VAR_REF,INST_ID_REF,TIMELINE_1,VAR_1,INST_ID_1, TOLERA, Y_LABEL):
    import numpy as np    
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    
    DIFF = []
    for i in range(len(VAR_1)):
        DIFF.append(VAR_REF[i]-VAR_1[i])
    MeanDIFF = np.mean(DIFF)       
        
    fig, ax = plt.subplots(figsize=(10,5))        
    inter = mdates.HourLocator(interval = 3)  #
    date_form = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_locator(inter)
    ax.xaxis.set_major_formatter(date_form)
    plt.fill_between(TIMELINE_REF, float(TOLERA), float(TOLERA)*3, color='salmon')
    plt.fill_between(TIMELINE_REF, -float(TOLERA), float(TOLERA)*-3, color='salmon')
    plt.plot(TIMELINE_REF,DIFF,'g')
    plt.axhline(MeanDIFF, color = 'k')
    plt.axhline(float(TOLERA), color = 'r')
    plt.axhline(-float(TOLERA), color = 'r')
    plt.ylim(min(DIFF)-float(TOLERA)/4, max(DIFF)+float(TOLERA)/4)
    plt.title ('Comprobación de '+INSTR+'S en '+STATION)
    plt.ylabel (Y_LABEL)
    plt.xlabel (DATE)
    UNITS = Y_LABEL[Y_LABEL.find('(')+1:Y_LABEL.find(')')]
    plt.legend([INSTR+'_REF - '+INSTR+'_'+STATION,'Diferencia promedio '+str(round(MeanDIFF,3))+' '+UNITS, 'Umbrar ('+TOLERA+')'])
    plt.grid(True)
    plt.savefig(FILENAME, bbox_inches='tight')
    plt.show()
    return MeanDIFF
###############################################################################
#
#
#%% FUNCION DE CREACION DE TOLERANCIA
def Plt_TOLERA (FILENAME,STATION,DATE,INSTR,TIMELINE_REF,VAR_REF,INST_ID_REF,TIMELINE_1,VAR_1,INST_ID_1,TOLERA,Y_LABEL):
    import numpy as np    
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
        
    fig, ax = plt.subplots(figsize=(10,5))
    VAR_REF = np.array (VAR_REF)
    
    inter = mdates.HourLocator(interval = 1)  #
    date_form = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_locator(inter)
    ax.xaxis.set_major_formatter(date_form)

    P_UP = VAR_REF + float(TOLERA)
    P_LO = VAR_REF - float(TOLERA)
    if (TIMELINE_REF[1] > TIMELINE_1[1]):
        TIMELINE_INI = TIMELINE_REF[0]
    else:
        TIMELINE_INI = TIMELINE_1[0]

    if (TIMELINE_REF[len(TIMELINE_REF)-1] < TIMELINE_1[len(TIMELINE_1)-1]):
        TIMELINE_END = TIMELINE_REF[len(TIMELINE_REF)-1]
    else:
        TIMELINE_END = TIMELINE_1[len(TIMELINE_1)-1]
    plt.xlim(TIMELINE_INI, TIMELINE_END)    
    plt.ylim(min(VAR_REF)-float(TOLERA)*2, max(VAR_REF)+float(TOLERA)*2)
    
    plt.plot(TIMELINE_REF,VAR_REF,'k')    
    plt.plot(TIMELINE_REF,(P_UP),'salmon')
    plt.plot(TIMELINE_REF,(P_LO),'salmon')
    plt.fill_between(TIMELINE_REF, P_UP, P_LO, color='salmon')
    plt.plot(TIMELINE_1,VAR_1,'g')
    plt.title ('Comprobación de '+INSTR+'S en '+STATION)
    plt.ylabel (Y_LABEL)
    plt.xlabel (DATE)
    plt.legend([INST_ID_REF+' - Referencia', 'Límite tolerable superior (+'+str(TOLERA)+')' , 'Límite tolerable inferiro (-'+str(TOLERA)+')', INST_ID_1+' - '+STATION])
    plt.grid(True)
    plt.savefig(FILENAME, bbox_inches='tight')
    plt.show()
###############################################################################
#
#
#%% FUNCION PARA ELABORAR EL REPORT
def BARO_Report (reportFile, Station, TestDate, Operador, BARO_Ref_ID, BARO_Ref_DT, BARO_Est_ID, BARO_Est_DT, Test_Ini, Test_End, Diff, Tolerancia, Figura_1, Figura_2, Figura_3):
    from datetime import datetime
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    
    Titulo     = 'BAROMETER OPERATION TEST' 
    
#Tamanyos
    A4_W, A4_H = A4
    MAR_L, MAR_R = 50, A4_W-50
    COL_1, COL_2, COL_3 = 160, A4_W/2, 420

#Momento de creacion del report    
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
    report.drawCentredString(230,A4_H-380, str(round(Diff,3))+' hPa')
    report.drawString(COL_3+5,A4_H-380, str(Tolerancia)+' hPa')
    
    if (Diff < float(Tolerancia)):
        report.drawCentredString(A4_W/2,A4_H-430, 'The instrument has passed the test, can continue operative at the station.')
    else:
        report.setFillColor('red')
        report.drawCentredString(A4_W/2,A4_H-430, 'The instrument has NOT passed the test. Must be replaced.')
            
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
###############################################################################