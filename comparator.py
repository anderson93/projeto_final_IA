import pso_v4 as pTEST
from math import sqrt
from openpyxl import Workbook, workbook, load_workbook
wb = load_workbook('v_final_FESP_PadroesDeInfracao.xlsx', read_only = True, data_only=True)

ws = wb.active          #Grab the active worksheet

pso_COST, pso_POSITION = pTEST.pso() 

def compare(ROW_AUX, pso_POSITION):

    AAET_SHEET = ws.cell(row=ROW_AUX,column=70).value        #Get the values of the table
    AAST_SHEET = ws.cell(row=ROW_AUX,column=75).value
    VI_SHEET   = ws.cell(row=ROW_AUX,column=81).value
    QMA_SHEET  = ws.cell(row=ROW_AUX,column=82).value
    IMAI_SHEET = ws.cell(row=ROW_AUX,column=83).value
    VA_SHEET   = ws.cell(row=ROW_AUX,column=80).value

    ALVO_SHEET = ws.cell(row=ROW_AUX,column=14).value

    AAET = pso_POSITION[0]      # x = AAET = x[0] ;
    AAST = pso_POSITION[1]      # y = AAST = x[1] ;
    VI   = pso_POSITION[2]      # z = VI = x[2] ;
    QMA  = pso_POSITION[3]      # v = QMA = x[3] ;
    IMAI = pso_POSITION[4]      # w = IMAI = x[4] ;
    VA   = pso_POSITION[5]      # u = VA = x[5].
    print "\n"
    print "These are the selected parameters by the PSO:"
    print "CA=", (pso_POSITION[5]/(pso_POSITION[1]-pso_POSITION[0]))**(-1) ,"CP=", pso_POSITION[2]/(pso_POSITION[1]-pso_POSITION[0]), "CC=", (pso_POSITION[1]/pso_POSITION[0])**(-1), "CI=", pso_POSITION[3]/pso_POSITION[4]
    print "\n"
    try:
        CA = (pso_POSITION[5]/(pso_POSITION[1]-pso_POSITION[0]))**(-1)
    except ZeroDivisionError:
        CA = 'inf'
    try:
        CP = pso_POSITION[2]/(pso_POSITION[1]-pso_POSITION[0])
    except ZeroDivisionError:
        CP = 'inf'
    try:
        CC = (pso_POSITION[1]/pso_POSITION[0])**(-1)
    except ZeroDivisionError:
        CC = 'inf'
    try:
        CI = pso_POSITION[3]/pso_POSITION[4]
    except ZeroDivisionError:
        CI = 'inf'

    try:
        CA_SHEET = VA_SHEET/(AAST_SHEET-AAET_SHEET)
    except ZeroDivisionError:
        CA_SHEET = 'inf'
    try:
        CP_SHEET = VI_SHEET/(AAST_SHEET-AAET_SHEET)
    except ZeroDivisionError:
        CP_SHEET = 'inf'    
    try:
        CC_SHEET = AAST_SHEET/AAET_SHEET        
    except ZeroDivisionError:
        CC_SHEET = 'inf'    
    try:
        CI_SHEET = QMA_SHEET/IMAI_SHEET    
    except ZeroDivisionError:
        CI_SHEET = 'inf'
    print "Those are the selected contributor's parameters:"
    print "CA_SHEET=", CA_SHEET ,"CP_SHEET=", CP_SHEET, "CC_SHEET=", CC_SHEET, "CI_SHEET=", CI_SHEET
    print "\n"
    print "These are the selected parameters by the PSO:"
    print "AAET=", AAET, "AAST= ", AAST, "VI=", VI, "QMA=", QMA, "IMAI=", IMAI, "VA=", VA
    print "\n"    
    print "Those are the selected contributor's parameters:"
    print "AAET_SHEET=", AAET_SHEET, "AAST_SHEET= ", AAST_SHEET, "VI_SHEET=", VI_SHEET, "QMA_SHEET=", QMA_SHEET, "IMAI_SHEET=", IMAI_SHEET, "VA_SHEET=", VA_SHEET
    print "\n"
    print "Comparing..."
    print "\n"
    distance = sqrt((AAET - AAET_SHEET)**2 + (AAST - AAST_SHEET)**2\
                   +(VA - VA_SHEET)**2 + (VI - VI_SHEET)**2\
                   +(QMA - QMA_SHEET)**2 + (IMAI - IMAI_SHEET)**2)

    distance2 = sqrt((CA-CA_SHEET)**2+(CP-CP_SHEET)**2+(CI-CI_SHEET)**2+(CC-CC_SHEET)**2)
    
    return distance, distance2, ALVO_SHEET

choose_row = input("Choose a row between:")
euclidian_dist, euclidian_dist2, ALVO = compare(choose_row, pso_POSITION)

print "The Euclidian distance between the chosen contributor and the optimal profile defined by the PSO algorithm is:", euclidian_dist2
print "\n"
print "The choosen row is supposed to be:", ALVO




