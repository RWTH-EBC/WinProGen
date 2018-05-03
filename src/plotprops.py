'''
Created on 18.03.2015

@author: Marco Bertinelli
'''

import pandas as pd
from pandas import Series, DataFrame, MultiIndex
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.patches import Polygon
from docutils.languages.af import labels

# import HistoQhObs as HistoQhObs
# import HistoQhObs_Together as HistoQhObs_Together
# import plotDiurnalValidateNew as plotDiurnalValidateNew
# import plotWAT as plotWAT

sizeText=10
params = {'backend': 'wxAgg', 'lines.markersize' : 6, 
          'axes.labelsize': sizeText, "mathtext.default":"regular", 
          'text.fontsize': sizeText, 'axes.titlesize':sizeText, 'legend.fontsize': sizeText, 
          'xtick.labelsize': sizeText, 'ytick.labelsize': sizeText}
plt.rcParams.update(params)

fontsize_XLabel =   14
fontsize_YLabel =   14
fontsize_title  =   14
fontsize_XTicks =   14
fontsize_YTicks =   14
fontsize_Legend =   14
WithLegendFrame =   False


def create_Standardfigure():
    """
prepares a figures    """
    fontsize_XLabel =   14
    fontsize_YLabel =   14
    fontsize_title  =   14
    fontsize_XTicks =   14
    fontsize_YTicks =   14
    fontsize_Legend =   14
    WithLegendFrame =   False
    
    
    
    fig = plt.figure(figsize=(8, 5))
    fig.subplots_adjust(left=0.15)
    gs1 = gridspec.GridSpec(1, 1)
    ax = plt.subplot(gs1[0, :])    

    ax.set_ylim(0,1.1)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.3, box.width, box.height * 0.7])
    #ax.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours=3)), 5))
    #ax.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours=3)), 25), minor=True)
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%I:%M %p'))
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),frameon=WithLegendFrame, ncol=2, fontsize=fontsize_Legend)

    
    
    return fig, ax

def Histogram_AT():

    recFolder = 'D:/ghi-mbe/Daten Auswertung/records/AT/'
    
    t_1 = 5.0
    t_2 = 11.0
    t_3 = 14.0
    t_4 = 18.0

    n_0 = "<5"      # "A"
    n_1 = "5>11"    # "B"
    n_2 = "11>14"   # "C"
    n_3 = "14>18"   # "D"
    n_4 = ">18"     # "E"
    
    n_0 = "A"
    n_1 = "B"
    n_2 = "C"
    n_3 = "D"
    n_4 = "E"
    
    def func_AT(row):
        if row["Weather","-","-","AT"] <= t_1:
            return n_0
        elif t_1 < row["Weather","-","-","AT"] <= t_2:
            return n_1
        elif t_2 < row["Weather","-","-","AT"] <= t_3:
            return n_2
        elif t_3 < row["Weather","-","-","AT"] <= t_4:
            return n_3
        else:
            return n_4
        
    def func_rAT(row):
        if row["Weather","-","-","rAT"] <= t_1:
            return n_0
        elif t_1 < row["Weather","-","-","rAT"] <= t_2:
            return n_1
        elif t_2 < row["Weather","-","-","rAT"] <= t_3:
            return n_2
        elif t_3 < row["Weather","-","-","rAT"] <= t_4:
            return n_3
        else:
            return n_4
    
    


    df1=pd.read_csv(recFolder+'AT2012.csv',index_col=0,sep=';', header=[0,1,2,3],low_memory=False,parse_dates=True)

    df1["Weather","-","-","rAT"]               = df1.apply(pd.Series.round)
    df1["Weather","-","-","Kategorie_AT"]      = df1.apply(func_AT, axis=1)
    df1["Weather","-","-","Kategorie_rAT"]     = df1.apply(func_rAT, axis=1)

    # Zaehlen der Kategorien
    Kategorie_A = df1[df1["Weather","-","-","Kategorie_AT"]=="A"]
    Kategorie_B = df1[df1["Weather","-","-","Kategorie_AT"]=="B"]
    Kategorie_C = df1[df1["Weather","-","-","Kategorie_AT"]=="C"]
    Kategorie_D = df1[df1["Weather","-","-","Kategorie_AT"]=="D"]
    Kategorie_E = df1[df1["Weather","-","-","Kategorie_AT"]=="E"]
    
    Kategorie_rA = df1[df1["Weather","-","-","Kategorie_rAT"]=="A"]
    Kategorie_rB = df1[df1["Weather","-","-","Kategorie_rAT"]=="B"]
    Kategorie_rC = df1[df1["Weather","-","-","Kategorie_rAT"]=="C"]
    Kategorie_rD = df1[df1["Weather","-","-","Kategorie_rAT"]=="D"]
    Kategorie_rE = df1[df1["Weather","-","-","Kategorie_rAT"]=="E"]
    
         
    # Zahlen der Kategoriewechsel allgemein
    print ("Kategorie A:", len(Kategorie_A), "Kategorie rA:", len(Kategorie_rA))
    print ("Kategorie B:", len(Kategorie_B), "Kategorie rB:", len(Kategorie_rB))
    print ("Kategorie C:", len(Kategorie_C), "Kategorie rC:", len(Kategorie_rC))
    print ("Kategorie D:", len(Kategorie_D), "Kategorie rD:", len(Kategorie_rD))
    print ("Kategorie E:", len(Kategorie_E), "Kategorie rE:", len(Kategorie_rE))
     
    print ("Summe Kategorie A-E:", len(Kategorie_A)+len(Kategorie_B)+len(Kategorie_C)+len(Kategorie_D)+len(Kategorie_E))
    print ("Summe Kategorie rA-rE:", len(Kategorie_rA)+len(Kategorie_rB)+len(Kategorie_rC)+len(Kategorie_rD)+len(Kategorie_rE))
    
    
    # Zaehlen der Kategoriewechsel entsprechend der Tage
    Wechsel_A_B = 0
    Wechsel_B_C = 0
    Wechsel_C_D = 0
    Wechsel_D_E = 0

    for index, line in enumerate(df1.iterrows()):
        if index == len(df1.index)-1:
            print ("no")
        else:
            if df1["Weather","-","-","Kategorie_AT"][index] == "A" and df1["Weather","-","-","Kategorie_AT"][index+1] == "B":
                Wechsel_A_B = Wechsel_A_B + 1
            if df1["Weather","-","-","Kategorie_AT"][index] == "B" and df1["Weather","-","-","Kategorie_AT"][index+1] == "C":
                Wechsel_B_C = Wechsel_B_C + 1
            if df1["Weather","-","-","Kategorie_AT"][index] == "C" and df1["Weather","-","-","Kategorie_AT"][index+1] == "D":
                Wechsel_C_D = Wechsel_C_D + 1
            if df1["Weather","-","-","Kategorie_AT"][index] == "D" and df1["Weather","-","-","Kategorie_AT"][index+1] == "E":
                Wechsel_D_E = Wechsel_D_E + 1

    
    # Erkennung von Wochentagen, Wochenende
    df1['dayNumber']    = df1.index.weekday    
    onlyWeekdays        = df1[df1['dayNumber']<5]
    onlyWeekend         = df1[df1['dayNumber']>=5] 

    print ("Histogram_AT done")
    

def Select_ColorsAndMarkers(Level0="", Level2="",Level3="", Level4="", Level5=""):
    markEntr_Alt1 = True
    
    print ("Start SelectAnalysisFunction")
    
    # ColorList Level0
    colorsTemperature=["LimeGreen",'Indigo','RoyalBlue','DeepSkyBlue','Orange','Red']
    markersTemperature=['^','o','s','*','d','v']
    
    # ColorList Level2
    colorsEntrances=["LimeGreen","ForestGreen","DarkGreen","LightSkyBlue","CornflowerBlue","DarkSlateBlue"]
    if markEntr_Alt1:
        markersEntrances=['^','o','s','*','d','v']  # alternative 1
    else:
        markersEntrances2=['^','o','s','^','o','s'] # alternative 2
        markersEntrances = markersEntrances2
    
    # ColorList Level3
    colorsAps=["Sienna","FireBrick","Red","OrangeRed","Tomato","DeepPink","Fuchsia","Magenta","MediumVioletRed","Crimson","LimeGreen"]
    markersAps=["s",'^','o','h','+','x','s','p','*','d',None]
    
    # ColorList Level4
    colorRooms=["LimeGreen",'Crimson','GoldenRod','CornflowerBlue',"DarkGreen",'MidnightBlue']
    markersRooms=[None,'^','o','s','*','d']
    
    # Checklisten 
    CheckTemperatures   = ["T1","T2","T3","T4","T5"]
    CheckTemperatures   = ["T0","T1","T2","T3","T4","T5"]
    CheckEntrances      = ["B2E1","B2E2","B2E3","B3E1","B3E2","B3E3"]
    CheckApartments     = ["A01","A02","A03","A04","A05","A06","A07","A08","A09","A10",'-']
    CheckRooms          = ['-', "Room_Bath","Room_Children","Room_Kitchen","Room_Living","Room_Sleeping",]
    
    
    
    
    if Level0 == "T0":     
        #print "Nur eine Linie, also alle Temperaturbereiche zusammen"
        
        if Level2 == None:
            #print "Alle Eingaenge"
            
            if Level3 == "-":
                #print "mean von allen Apartments"
                    
                if Level4 == "-":
                    #print "mean von allen Rooms"
                    
                    if Level5 == "WP1":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings","meanApartments","meanRooms",Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings","meanApartments","meanRooms",Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings","meanApartments","meanRooms",Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings","meanApartments","meanRooms",Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings","meanApartments","meanRooms",Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings","meanApartments","meanRooms",Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                               
                #-----------------------------------------------------------------
                #-----------------------------------------------------------------
                elif Level4 in CheckRooms:
                    #print Level4
                    
                    if Level5 == "WP1":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings","meanApartments",Level4,Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings","meanApartments",Level4,Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings","meanApartments",Level4,Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings","meanApartments",Level4,Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings","meanApartments",Level4,Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings","meanApartments",Level4,Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                #-----------------------------------------------------------------
                #-----------------------------------------------------------------
                else:
                    print ("ERROR: Auswahl Level4 nicht korrekt")
            
            elif Level3 in CheckApartments:
                #print Level3
                
                if Level4 == "-":
                    print ("mean von allen Rooms")
                    
                    if Level5 == "WP1":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings",Level3,"meanRooms",Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings",Level3,"meanRooms",Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings",Level3,"meanRooms",Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings",Level3,"meanRooms",Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings",Level3,"meanRooms",Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings",Level3,"meanRooms",Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                                        
                #-----------------------------------------------------------------
                #-----------------------------------------------------------------
                elif Level4 in CheckRooms:
                    #print Level4
                    
                    if Level5 == "WP1":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings",Level3,Level4,Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings",Level3,Level4,Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings",Level3,Level4,Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings",Level3,Level4,Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings",Level3,Level4,Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        #print Level5
                        colorList   = colorsEntrances
                        markerList  = markersEntrances
                        title       = ["T0","allBuildings",Level3,Level4,Level5]
                        labels      = CheckEntrances
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                #-----------------------------------------------------------------
                #-----------------------------------------------------------------
                else:
                    print ("ERROR: Auswahl Level4 nicht korrekt")
            
            else:
                print ("ERROR: Auswahl Level3 nicht korrekt")
        
        elif Level2 in CheckEntrances:
            #print Level2
            
            if Level3 == "-":
                #print "mean von allen Apartments"
                
                if Level4 == "-":
                    #print "mean von allen Rooms"
                    
                    if Level5 == "WP1":
                        #print Level5
                        colorList   = colorsEntrances[CheckEntrances.index(Level2)]
                        markerList  = markersEntrances[CheckEntrances.index(Level2)]
                        title       = ["T0", Level2,"meanApartments","meanRooms",Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        #print Level5
                        colorList   = colorsEntrances[CheckEntrances.index(Level2)]
                        markerList  = markersEntrances[CheckEntrances.index(Level2)]
                        title       = ["T0", Level2,"meanApartments","meanRooms",Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        #print Level5
                        colorList   = colorsEntrances[CheckEntrances.index(Level2)]
                        markerList  = markersEntrances[CheckEntrances.index(Level2)]
                        title       = ["T0", Level2,"meanApartments","meanRooms",Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        #print Level5
                        colorList   = colorsEntrances[CheckEntrances.index(Level2)]
                        markerList  = markersEntrances[CheckEntrances.index(Level2)]
                        title       = ["T0", Level2,"meanApartments","meanRooms",Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        #print Level5
                        colorList   = colorsEntrances[CheckEntrances.index(Level2)]
                        markerList  = markersEntrances[CheckEntrances.index(Level2)]
                        title       = ["T0", Level2,"meanApartments","meanRooms",Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        #print Level5
                        colorList   = colorsEntrances[CheckEntrances.index(Level2)]
                        markerList  = markersEntrances[CheckEntrances.index(Level2)]
                        title       = ["T0", Level2,"meanApartments","meanRooms",Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                elif Level4 == None:
                    print ("Alle Rooms")
                    
                    if Level5 == "WP1":
                        #print Level5
                        colorList   = colorRooms
                        markerList  = markersRooms
                        title       = ["T0", Level2,"meanApartments","allRooms",Level5]
                        labels      = CheckRooms
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        #print Level5
                        colorList   = colorRooms
                        markerList  = markersRooms
                        title       = ["T0", Level2,"meanApartments","allRooms",Level5]
                        labels      = CheckRooms
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        #print Level5
                        colorList   = colorRooms
                        markerList  = markersRooms
                        title       = ["T0", Level2,"meanApartments","allRooms",Level5]
                        labels      = CheckRooms
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        #print Level5
                        colorList   = colorRooms
                        markerList  = markersRooms
                        title       = ["T0", Level2,"meanApartments","allRooms",Level5]
                        labels      = CheckRooms
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        #print Level5
                        colorList   = colorRooms
                        markerList  = markersRooms
                        title       = ["T0", Level2,"meanApartments","allRooms",Level5]
                        labels      = CheckRooms
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        #print Level5
                        colorList   = colorRooms
                        markerList  = markersRooms
                        title       = ["T0", Level2,"meanApartments","allRooms",Level5]
                        labels      = CheckRooms
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                elif Level4 in CheckRooms:
                    #print Level4
                    
                    if Level5 == "WP1":
                        #print Level5
                        colorList   = colorRooms[CheckRooms.index(Level4)]
                        markerList  = markersRooms[CheckRooms.index(Level4)]
                        title       = ["T0", Level2,"meanApartments",Level4,Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        #print Level5
                        colorList   = colorRooms[CheckRooms.index(Level4)]
                        markerList  = markersRooms[CheckRooms.index(Level4)]
                        title       = ["T0", Level2,"meanApartments",Level4,Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        #print Level5
                        colorList   = colorRooms[CheckRooms.index(Level4)]
                        markerList  = markersRooms[CheckRooms.index(Level4)]
                        title       = ["T0", Level2,"meanApartments",Level4,Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        #print Level5
                        colorList   = colorRooms[CheckRooms.index(Level4)]
                        markerList  = markersRooms[CheckRooms.index(Level4)]
                        title       = ["T0", Level2,"meanApartments",Level4,Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        #print Level5
                        colorList   = colorRooms[CheckRooms.index(Level4)]
                        markerList  = markersRooms[CheckRooms.index(Level4)]
                        title       = ["T0", Level2,"meanApartments",Level4,Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        #print Level5
                        colorList   = colorRooms[CheckRooms.index(Level4)]
                        markerList  = markersRooms[CheckRooms.index(Level4)]
                        title       = ["T0", Level2,"meanApartments",Level4,Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                else:
                    print ("ERROR: Auswahl Level4 nicht korrekt")
                    
                    
                
            
            elif Level3 == None:
                #print "Alle Apartments"
                
                if Level4 == "-":
                    #print "mean von allen Rooms"
                    
                    if Level5 == "WP1":
                        #print Level5
                        colorList   = colorsAps
                        markerList  = markersAps
                        title       = ["T0", Level2,"allApartments","meanRooms",Level5]
                        labels      = CheckApartments
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        #print Level5
                        colorList   = colorsAps
                        markerList  = markersAps
                        title       = ["T0", Level2,"allApartments","meanRooms",Level5]
                        labels      = CheckApartments
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        #print Level5
                        colorList   = colorsAps
                        markerList  = markersAps
                        title       = ["T0", Level2,"allApartments","meanRooms",Level5]
                        labels      = CheckApartments
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        #print Level5
                        colorList   = colorsAps
                        markerList  = markersAps
                        title       = ["T0", Level2,"allApartments","meanRooms",Level5]
                        labels      = CheckApartments
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        #print Level5
                        colorList   = colorsAps
                        markerList  = markersAps
                        title       = ["T0", Level2,"allApartments","meanRooms",Level5]
                        labels      = CheckApartments
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        #print Level5
                        colorList   = colorsAps
                        markerList  = markersAps
                        title       = ["T0", Level2,"allApartments","meanRooms",Level5]
                        labels      = CheckApartments
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                elif Level4 in CheckRooms:
                    #print Level4
                    
                    if Level5 == "WP1":
                        #print Level5
                        colorList   = colorsAps
                        markerList  = markersAps
                        title       = ["T0", Level2,"allApartments",Level4,Level5]
                        labels      = CheckApartments
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        #print Level5
                        colorList   = colorsAps
                        markerList  = markersAps
                        title       = ["T0", Level2,"allApartments",Level4,Level5]
                        labels      = CheckApartments
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        #print Level5
                        colorList   = colorsAps
                        markerList  = markersAps
                        title       = ["T0", Level2,"allApartments",Level4,Level5]
                        labels      = CheckApartments
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        #print Level5
                        colorList   = colorsAps
                        markerList  = markersAps
                        title       = ["T0", Level2,"allApartments",Level4,Level5]
                        labels      = CheckApartments
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        #print Level5
                        colorList   = colorsAps
                        markerList  = markersAps
                        title       = ["T0", Level2,"allApartments",Level4,Level5]
                        labels      = CheckApartments
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        #print Level5
                        colorList   = colorsAps
                        markerList  = markersAps
                        title       = ["T0", Level2,"allApartments",Level4,Level5]
                        labels      = CheckApartments
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                else:
                    print ("ERROR: Auswahl Level4 nicht korrekt")
                    
                    
            
            elif Level3 in CheckApartments:
                #print Level3
                
                if Level4 == "-":
                    #print "mean von allen Rooms"
                    
                    if Level5 == "WP1":
                        #print Level5
                        colorList   = colorsAps[CheckApartments.index(Level3)]
                        markerList  = markersAps[CheckApartments.index(Level3)]
                        title       = ["T0", Level2,Level3,"meanRooms",Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        #print Level5
                        colorList   = colorsAps[CheckApartments.index(Level3)]
                        markerList  = markersAps[CheckApartments.index(Level3)]
                        title       = ["T0", Level2,Level3,"meanRooms",Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        #print Level5
                        colorList   = colorsAps[CheckApartments.index(Level3)]
                        markerList  = markersAps[CheckApartments.index(Level3)]
                        title       = ["T0", Level2,Level3,"meanRooms",Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        #print Level5
                        colorList   = colorsAps[CheckApartments.index(Level3)]
                        markerList  = markersAps[CheckApartments.index(Level3)]
                        title       = ["T0", Level2,Level3,"meanRooms",Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        #print Level5
                        colorList   = colorsAps[CheckApartments.index(Level3)]
                        markerList  = markersAps[CheckApartments.index(Level3)]
                        title       = ["T0", Level2,Level3,"meanRooms",Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        #print Level5
                        colorList   = colorsAps[CheckApartments.index(Level3)]
                        markerList  = markersAps[CheckApartments.index(Level3)]
                        title       = ["T0", Level2,Level3,"meanRooms",Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                elif Level4 == None:
                    #print "Alle Rooms"
                    
                    if Level5 == "WP1":
                        #print Level5
                        colorList   = colorRooms
                        markerList  = markersRooms
                        title       = ["T0", Level2,Level3,"allRooms",Level5]
                        labels      = CheckRooms
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        #print Level5
                        colorList   = colorRooms
                        markerList  = markersRooms
                        title       = ["T0", Level2,Level3,"allRooms",Level5]
                        labels      = CheckRooms
                        return colorList, markerList, title, labels
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        #print Level5
                        colorList   = colorRooms
                        markerList  = markersRooms
                        title       = ["T0", Level2,Level3,"allRooms",Level5]
                        labels      = CheckRooms
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        #print Level5
                        colorList   = colorRooms
                        markerList  = markersRooms
                        title       = ["T0", Level2,Level3,"allRooms",Level5]
                        labels      = CheckRooms
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        #print Level5
                        colorList   = colorRooms
                        markerList  = markersRooms
                        title       = ["T0", Level2,Level3,"allRooms",Level5]
                        labels      = CheckRooms
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        #print Level5
                        colorList   = colorRooms
                        markerList  = markersRooms
                        title       = ["T0", Level2,Level3,"allRooms",Level5]
                        labels      = CheckRooms
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                elif Level4 in CheckRooms:
                    #print Level4
                    
                    if Level5 == "WP1":
                        #print Level5
                        colorList   = colorRooms[CheckRooms.index(Level4)]
                        markerList  = markersRooms[CheckRooms.index(Level4)]
                        title       = ["T0", Level2,Level3,Level4,Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        #print Level5
                        colorList   = colorRooms[CheckRooms.index(Level4)]
                        markerList  = markersRooms[CheckRooms.index(Level4)]
                        title       = ["T0", Level2,Level3,Level4,Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        #print Level5
                        colorList   = colorRooms[CheckRooms.index(Level4)]
                        markerList  = markersRooms[CheckRooms.index(Level4)]
                        title       = ["T0", Level2,Level3,Level4,Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        #print Level5
                        colorList   = colorRooms[CheckRooms.index(Level4)]
                        markerList  = markersRooms[CheckRooms.index(Level4)]
                        title       = ["T0", Level2,Level3,Level4,Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        #print Level5
                        colorList   = colorRooms[CheckRooms.index(Level4)]
                        markerList  = markersRooms[CheckRooms.index(Level4)]
                        title       = ["T0", Level2,Level3,Level4,Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        #print Level5
                        colorList   = colorRooms[CheckRooms.index(Level4)]
                        markerList  = markersRooms[CheckRooms.index(Level4)]
                        title       = ["T0", Level2,Level3,Level4,Level5]
                        labels      = [""]
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                else:
                    print ("ERROR: Auswahl Level4 nicht korrekt")
            
            else:
                print ("ERROR: Auswahl Level3 nicht korrekt")
                
        else:
            print ("ERROR: Auswahl Level2 nicht eindeutig")


    #-----------------------------------------------------------------
    #-----------------------------------------------------------------
    #-----------------------------------------------------------------
    #-----------------------------------------------------------------
    elif Level0 == None:      
        print ("Alle Linien, also T0 ..... T5")
                
        if Level2 in CheckEntrances:
            #print Level2
            
            if Level3 == "-":
                #print "mean alle Apartments"
                
                if Level4 == '-':
                    #print "mean alle Rooms"
                    
                    if Level5 == "WP1":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,"meanApartments", "meanRooms", Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,"meanApartments", "meanRooms", Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,"meanApartments", "meanRooms", Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,"meanApartments", "meanRooms", Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,"meanApartments", "meanRooms", Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,"meanApartments", "meanRooms", Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                elif Level4 in CheckRooms:
                    #print Level4
                    
                    if Level5 == "WP1":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,"meanApartments", Level4, Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,"meanApartments", Level4, Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,"meanApartments", Level4, Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,"meanApartments", Level4, Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,"meanApartments", Level4, Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings      
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,"meanApartments", Level4, Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                else:
                    print ("ERROR: Auswahl Level4 nicht korrekt")
            
            elif Level3 in CheckApartments:
                #print Level3
                
                if Level4 == '-':
                    #print "mean alle Rooms"
                    
                    if Level5 == "WP1":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,Level3, "meanRooms", Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,Level3, "meanRooms", Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,Level3, "meanRooms", Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,Level3, "meanRooms", Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,Level3, "meanRooms", Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,Level3, "meanRooms", Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                elif Level4 in CheckRooms:
                    #print Level4
                    
                    if Level5 == "WP1":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,Level3,Level4, Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,Level3,Level4, Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,Level3,Level4, Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,Level3,Level4, Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        #print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,Level3,Level4, Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        ##print Level5
                        colorList   = colorsTemperature
                        markerList  = markersTemperature
                        title       = [Level2,Level3,Level4, Level5]
                        labels      = CheckTemperatures
                        selctionStrings = [Level0,Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                else:
                    print ("ERROR: Auswahl Level4 nicht korrekt")
            
            else:
                print ("ERROR: Auswahl Level3 nicht korrekt")
        
        else:
            print ("ERROR: Auswahl Level2 nicht eindeutig")
            
    #-----------------------------------------------------------------
    #-----------------------------------------------------------------
    #-----------------------------------------------------------------
    #-----------------------------------------------------------------
    elif Level0 in ["T1","T2","T3","T4","T5"]:
        
        if Level2 in CheckEntrances:
                        
            if Level3 == "-":
                
                if Level4 == "-":
                    
                    if Level5 == "WP1":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,"meanApartments","meanRooms",Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,"meanApartments","meanRooms",Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,"meanApartments","meanRooms",Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,"meanApartments","meanRooms",Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,"meanApartments","meanRooms",Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,"meanApartments","meanRooms",Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                        
                
                elif Level4 in CheckRooms:
                    
                    if Level5 == "WP1":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,"meanApartments",Level4,Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,"meanApartments",Level4,Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,"meanApartments",Level4,Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,"meanApartments",Level4,Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,"meanApartments",Level4,Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,"meanApartments",Level4,Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                else:
                    print ("ERROR: Auswahl Level4 nicht korrekt")
                    
                
            
            elif Level3 in CheckApartments:
                
                if Level4 == "-":
                    
                    if Level5 == "WP1":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,Level3,"meanRooms",Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,Level3,"meanRooms",Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,Level3,"meanRooms",Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,Level3,"meanRooms",Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,Level3,"meanRooms",Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,Level3,"meanRooms",Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                elif Level4 in CheckRooms:
                    
                    if Level5 == "WP1":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,Level3,Level4,Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP2":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,Level3,Level4,Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP1+2":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,Level3,Level4,Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WP":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,Level3,Level4,Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPD":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,Level3,Level4,Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    elif Level5 == "WPS":
                        colorList   = [colorsTemperature[0]] + [colorsTemperature[CheckTemperatures.index(Level0)]]
                        markerList  = [markersTemperature[0]] + [markersTemperature[CheckTemperatures.index(Level0)]]
                        title       = [Level2,Level3,Level4,Level5]
                        labels      = ["T0",Level0]
                        selctionStrings = [["T0",Level0],Level2,Level3,Level4,Level5]
                        return colorList, markerList, title, labels, selctionStrings
                    #-----------------------------------------------------------------
                    else:
                        print ("ERROR: Auswahl Level5 nicht korrekt")
                
                else:
                    print ("ERROR: Auswahl Level4 nicht korrekt")
            
            else:
                print ("ERROR: Auswahl Level3 nicht korrekt")
                
        else:
            print ("ERROR: Auswahl Level2 nicht eindeutig")
            
        
        
    
    else:
        print ("ERROR: Auswahl Level0[0] nicht eindeutig")
    
    print ("Ende SelectAnalysisFunction")
        
        
    
    
    
    
     
def english2German(titleList,labelList):
    
    translateDictonary ={"B2E1":"R2E1",
                         "B2E2":"R2E2",
                         "B2E3":"R2E3",
                         "B3E1":"R3E1",
                         "B3E2":"R3E2",
                         "B3E2":"R3E3",
                         "allBuildings": "Gebaeude",
                         "meanApartment": "Durchschnitt Wohnung",
                         "allApartments": "Wohnung",
                         "Room_Sleeping":"Schlafzimmer",
                         "Room_Kitchen": u"Kueche",
                         "Room_Children": "Kinderzimmer",
                         "Room_Living": "Wohnzimmer",
                         "Room_Bath": "Badezimmer",
                         "allRooms": "Zimmer",
                         "meanRooms": "Durchschnitt Zimmer",
                         "T0": "ATR",
                         "T1": 'DAT $\leq$ 5',
                         "T2": "5 $\leq$ DAT $\leq$ 11",
                         "T3": "11 $\leq$ DAT $\leq$ 14",
                         "T4": "14 $\leq$ DAT $\leq$ 18",
                         "T5": "DAT $\geq$ 18",
                         "-":"Durschnitt"}
    
    new_titleList = []
    for titleComponent in titleList:
        pass
        if titleComponent in translateDictonary.keys():
            new_titleList.append(translateDictonary.get(titleComponent))
        else:
            new_titleList.append(titleComponent)
        
    new_labelList = []
    for labelComponent in labelList:
        if labelComponent in translateDictonary.keys():
            new_labelList.append(translateDictonary.get(labelComponent))
        else:
            new_labelList.append(labelComponent)
    
    return new_titleList, new_labelList

def codifyL1(codeList):
    if isinstance(codeList[0], type(None)):
        return codeList
    else:
        codeListZ=codeList[0]
        translateDictonary={'T0':'ATR',
                            'T1':'5 < AT Daily Average',
                            'T2':'5 < AT Daily Average <= 11',
                            'T3':'1 < AT Daily Average <= 14',
                            'T4':'14 < AT Daily Average <= 18',
                            'T5':'18 < AT Daily Average'}
        
        if isinstance(codeListZ, basestring): codeListZ=[codeListZ]
        new_codeList = []
        for titleComponent in codeListZ:
            pass
            if titleComponent in translateDictonary.keys():
                new_codeList.append(translateDictonary.get(titleComponent))
            else:
                new_codeList.append(titleComponent)
        codeList[0]=new_codeList[0]
        print (new_codeList[0])
        return codeList
            
def english2English(titleList,labelList):
    
    translateDictonary ={"B2E1":"B2E1",
                         "B2E2":"B2E2",
                         "B2E3":"B2E3",
                         "B3E1":"B3E1",
                         "B3E2":"B3E2",
                         "B3E2":"B3E3",
                         "allBuildings": "all buildings",
                         "meanApartments": "Mean Apartment",
                         "allApartments": "all Apartments",
                         "Room_Sleeping":"Sleeping room",
                         "Room_Kitchen": "Kitchen",
                         "Room_Children": "Children room",
                         "Room_Living": "Living room",
                         "Room_Bath": "Bathroom",
                         "allRooms": "all Rooms",
                         "meanRooms": "Mean roooms",
                         "T0": "ATR",
                         "T1": 'DAT $\leq$ 5',
                         "T2": "5 $\leq$ DAT $\leq$ 11",
                         "T3": "11 $\leq$ DAT $\leq$ 14",
                         "T4": "14 $\leq$ DAT $\leq$ 18",
                         "T5": "DAT $\geq$ 18",
                         "-":"Average"}
    
    new_titleList = []
    for titleComponent in titleList:
        pass
        if titleComponent in translateDictonary.keys():
            new_titleList.append(translateDictonary.get(titleComponent))
        else:
            new_titleList.append(titleComponent)
        
    new_labelList = []
    for labelComponent in labelList:
        if labelComponent in translateDictonary.keys():
            new_labelList.append(translateDictonary.get(labelComponent))
        else:
            new_labelList.append(labelComponent)
    
    return new_titleList, new_labelList

    


def readDF(df1=pd.DataFrame(),df2=pd.DataFrame(),df3=pd.DataFrame(),df4=pd.DataFrame(),df5=pd.DataFrame(),df6=pd.DataFrame(),level0='ATR',level1='Standard Diurnal',level2='MD',level3='B2E1',level4='A01',level5='Room_Living',level6="WP1"):
    levels=[level0,level1,level2,level3,level4,level5,level6]
    print (levels)
    if not df1.empty:
        for levelNr,level in enumerate(levels):
            if level!=None: df1=df1.iloc[:,df1.columns.get_level_values(levelNr)==level]
    if not df2.empty:
        for levelNr,level in enumerate(levels):
            if level!=None: df2=df2.iloc[:,df2.columns.get_level_values(levelNr)==level]
    if not df3.empty:
        for levelNr,level in enumerate(levels):
            if level!=None: df3=df3.iloc[:,df3.columns.get_level_values(levelNr)==level]
    if not df4.empty:
        for levelNr,level in enumerate(levels):
            if level!=None: df4=df4.iloc[:,df4.columns.get_level_values(levelNr)==level]
    if not df5.empty:
        for levelNr,level in enumerate(levels):
            if level!=None: df5=df5.iloc[:,df5.columns.get_level_values(levelNr)==level]
    if not df6.empty:
        for levelNr,level in enumerate(levels):
            if level!=None: df6=df6.iloc[:,df6.columns.get_level_values(levelNr)==level]
    
    print ("COls: {}".format(df1.columns))
    
    
    
#     if level0!=None: 
#         df1=df1.iloc[:,df1.columns.get_level_values(0)==level0]
#         df2=df2.iloc[:,df2.columns.get_level_values(0)==level0]
#         df3=df3.iloc[:,df3.columns.get_level_values(0)==level0]
#         df4=df4.iloc[:,df4.columns.get_level_values(0)==level0]
#         df5=df5.iloc[:,df5.columns.get_level_values(0)==level0]
#         df6=df6.iloc[:,df6.columns.get_level_values(0)==level0]
#     if level1!=None: 
#         df1=df1.iloc[:,df1.columns.get_level_values(1)==level1]
#         df2=df2.iloc[:,df2.columns.get_level_values(1)==level1]
#         df3=df3.iloc[:,df3.columns.get_level_values(1)==level1]
#         df4=df4.iloc[:,df4.columns.get_level_values(1)==level1]
#         df5=df5.iloc[:,df5.columns.get_level_values(1)==level1]
#         df6=df6.iloc[:,df6.columns.get_level_values(1)==level1]
#     if level2!=None: 
#         df1=df1.iloc[:,df1.columns.get_level_values(2)==level2]
#         df2=df2.iloc[:,df2.columns.get_level_values(2)==level2]
#         df3=df3.iloc[:,df3.columns.get_level_values(2)==level2]
#         df4=df4.iloc[:,df4.columns.get_level_values(2)==level2]
#         df5=df5.iloc[:,df5.columns.get_level_values(2)==level2]
#         df6=df6.iloc[:,df6.columns.get_level_values(2)==level2]
#     if level3!=None:
#         df1=df1.iloc[:,df1.columns.get_level_values(3)==level3]
#         df2=df2.iloc[:,df2.columns.get_level_values(3)==level3]
#         df3=df3.iloc[:,df3.columns.get_level_values(3)==level3]
#         df4=df4.iloc[:,df4.columns.get_level_values(3)==level3]
#         df5=df5.iloc[:,df5.columns.get_level_values(3)==level3]
#         df6=df6.iloc[:,df6.columns.get_level_values(3)==level3]
#     if level4!=None: 
#         df1=df1.iloc[:,df1.columns.get_level_values(4)==level4] 
#         df2=df2.iloc[:,df2.columns.get_level_values(4)==level4]
#         df3=df3.iloc[:,df3.columns.get_level_values(4)==level4]
#         df4=df4.iloc[:,df4.columns.get_level_values(4)==level4]
#         df5=df5.iloc[:,df5.columns.get_level_values(4)==level4]
#         df6=df6.iloc[:,df6.columns.get_level_values(4)==level4]    
#     if level5!=None: 
#         df1=df1.iloc[:,df1.columns.get_level_values(5)==level5] 
#         df2=df2.iloc[:,df2.columns.get_level_values(5)==level5]
#         df3=df3.iloc[:,df3.columns.get_level_values(5)==level5]
#         df4=df4.iloc[:,df4.columns.get_level_values(5)==level5]
#         df5=df5.iloc[:,df5.columns.get_level_values(5)==level5]
#         df6=df6.iloc[:,df6.columns.get_level_values(5)==level5]
#     if level6!=None: 
#         df1=df1.iloc[:,df1.columns.get_level_values(6)==level6] 
#         df2=df2.iloc[:,df2.columns.get_level_values(6)==level6]
#         df3=df3.iloc[:,df3.columns.get_level_values(6)==level6]
#         df4=df4.iloc[:,df4.columns.get_level_values(6)==level6]
#         df5=df5.iloc[:,df5.columns.get_level_values(6)==level6]
#         df6=df6.iloc[:,df6.columns.get_level_values(6)==level6]
    print ("Ende readDF")
    
def plotDiurnal(df,df2, labels=[],levels=[],timeType='Standard Diurnal',dataType='MD',title=None,colors=None):

    if levels[0]!=None: 
        df=df.iloc[:,df.columns.get_level_values(0)==levels[0]]
        df2=df2.iloc[:,df2.columns.get_level_values(0)==levels[0]]
    if timeType!=None: 
        df=df.iloc[:,df.columns.get_level_values(1)==timeType]
        df2=df2.iloc[:,df2.columns.get_level_values(1)==timeType]
    if dataType!=None: 
        df=df.iloc[:,df.columns.get_level_values(2)==dataType]
        df2=df2.iloc[:,df2.columns.get_level_values(2)==dataType]
    if levels[1]!=None: 
        df=df.iloc[:,df.columns.get_level_values(3)==levels[1]]
        df2=df2.iloc[:,df2.columns.get_level_values(3)==levels[1]]
    if levels[2]!=None: 
        df=df.iloc[:,df.columns.get_level_values(4)==levels[2]]
        df2=df2.iloc[:,df2.columns.get_level_values(4)==levels[2]]
    if levels[3]!=None: 
        df=df.iloc[:,df.columns.get_level_values(5)==levels[3]]
        df2=df2.iloc[:,df2.columns.get_level_values(5)==levels[3]]
    if levels[4]!=None: 
        df=df.iloc[:,df.columns.get_level_values(6)==levels[4]]
        df2=df2.iloc[:,df2.columns.get_level_values(6)==levels[4]]


    fig = plt.figure(figsize=(16./2.54, 10/2.54))
    fig.subplots_adjust(left=0.1)
    gs1 = gridspec.GridSpec(1, 1)
    #ax = plt.subplot(gs1[0, :])    
    ax = plt.axes([0.1, 0.1, .85, .8])
    for index,column in enumerate(df.columns.values):
        if index!=10: ax.plot(df.index, df[column], colors[index], linewidth=2.0,label=labels[index],alpha=0.4)
     
    for index,column in enumerate(df2.columns.values):
        if index!=10: ax.plot(df.index, df2[column], colors[index], marker="x", linewidth=0.7,markevery=60,mfc='None', mec=colors[index],label=labels[index]+' Sim')
     

    ax.set_ylabel("Proportion of windows open")
    ax.set_xlabel("Time of the day")
    ticks = ax.get_xticks()
    ax.set_ylim(0,1)
    plt.title(title, y=1.05)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.32,
                 box.width, box.height * 0.68])
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
    ax.legend(loc='upper center', bbox_to_anchor=(0.475, -0.2),frameon=False, ncol=3)
    plt.show()

def plotBoxes(df,df2, labels=[],levels=[],title=None,colors=None, savingFolder="", extraName=""):
        
        fig2= plt.figure(figsize=(16./2.54, 8/2.54))
        fig2.subplots_adjust(left=0.1)
        #gs2 = gridspec.GridSpec(1, 1)
        #ax2 = fig2.add_subplot(gs2[0, :])    
        ax2 = fig2.add_axes([0.13, 0.355, .85, .55])
        #plt.title(title, y=1.05)
    
        bp = ax2.boxplot(df2.values-df.values, sym='-', vert=True, whis=1.5)#, linewidth=2.0,label=labels[index],alpha=0.4)
        # Now fill the boxes with desired colors
        boxColors = colors
        bisColors = [a for a in colors for i in range(2)]
        numBoxes = 6
        medians = range(numBoxes)
        meanValues=DataFrame(df2.values-df.values).mean(axis=0).values
        meanAbsResiduals=DataFrame(abs(df2.values-df.values)).mean(axis=0).values
    
        for i in range(numBoxes):
            box = bp['boxes'][i]
            boxY = []
            boxX = []
            for j in range(5):
                boxX.append(box.get_xdata()[j])
                boxY.append(box.get_ydata()[j])
            boxCoords = zip(boxX,boxY)
            boxPolygon = Polygon(boxCoords, facecolor=boxColors[i], alpha=0.1,zorder=1)
            ax2.add_patch(boxPolygon)
            # Now draw the median lines back over what we just filled in
            med = bp['medians'][i]
            medianX = []
            medianY = []
            for j in range(2):
                medianX.append(med.get_xdata()[j])
                medianY.append(med.get_ydata()[j])
                plt.plot(medianX, medianY, boxColors[i],linewidth=2)
                medians[i] = medianY[0]
            # Finally, overplot the sample averages, with horizontal alignment
            # in the center of each box
            plt.plot([np.average(med.get_xdata())], meanValues[i],
                  color='None', marker='o', markeredgecolor=boxColors[i], markersize=7,zorder=0)
            plt.plot([np.average(med.get_xdata())], meanValues[i],
                  color=boxColors[i], marker='o', markeredgecolor=boxColors[i], markersize=7,alpha=0.2,zorder=3)
            plt.setp(bp['medians'][i], color=colors[i]) # DarkSlateGray 
            plt.setp(bp['boxes'][i], color='DarkSlateGray')
    
        for i in range(len(bisColors)):
            plt.setp(bp['whiskers'][i], color='DarkSlateGray')
            plt.setp(bp['caps'][i], color='DarkSlateGray')
        plt.setp(bp['fliers'], color='Gainsboro')
        plt.setp(bp['whiskers'], linestyle='solid')   
        
        ax2.set_ylabel("Simulated-Observed WP profile")
#        ax2.set_ylabel("Simulated-Observed WS")
        ax2.yaxis.set_label_coords(-0.09, 0.5)
        ax2.set_ylim(-0.02,0.02)
        #ax2.set_yticks([0.2, 0.6, 0.8], minor=False)
        ax2.yaxis.set_ticks_position('left')
        ax2.xaxis.set_ticks_position('bottom')
        #newLabels= ["ATR",'DAT $\leq$ 5'," 5 $\leq$ \nDAT\n $\leq$ 11", "11 $\leq$ \nDAT\n $\leq$ 14","14 $\leq$ \nDAT\n $\leq$ 18","DAT $\geq$ 18"]
        xtickNames = plt.setp(ax2, xticklabels=labels) 
        plt.setp(xtickNames,rotation=30)#, fontsize=8
        ax2.yaxis.grid(True,zorder=0, color="Gainsboro", ls="-")
        ax2.xaxis.grid(False)
        ax2.set_axisbelow(True)
        title=str(np.char.replace(title," ", '_'))
        title=str(np.char.replace(title,"Apartment", 'Ap'))

        plt.savefig(savingFolder+title+'_BP.png',figure=fig2,  format='png')
        plt.savefig(savingFolder+title+'_BP.pdf',figure=fig2,  format='pdf')
        #plt.show()
        


def plotDiurnalandBoxes(df,df2, labels=[],levels=[],timeType='Standard Diurnal',dataType='MD',title=None,colors=None, savingFolder="", extraName=""):
    
    print (levels)
    if levels[1]== "B2E3" and levels[2]=='A03'and levels[3]=='Room_Kitchen':
        return np.empty(6) * np.nan, str(levels)
    else:
        oldtitle=title
        title=desmountTitle(title, extraName)
        name=buildName(oldtitle, extraName)
        if timeType!='Standard Diurnal':
            title=timeType+' - '+ title
            name=timeType+' - '+ name
        if levels[0]!=None: 
            df=df.iloc[:,df.columns.get_level_values(0)==levels[0]]
            df2=df2.iloc[:,df2.columns.get_level_values(0)==levels[0]]
        if timeType!=None: 
            df=df.iloc[:,df.columns.get_level_values(1)==timeType]
            df2=df2.iloc[:,df2.columns.get_level_values(1)==timeType]
        if dataType!=None: 
            df=df.iloc[:,df.columns.get_level_values(2)==dataType]
            df2=df2.iloc[:,df2.columns.get_level_values(2)==dataType]
        if levels[1]!=None: 
            df=df.iloc[:,df.columns.get_level_values(3)==levels[1]]
            df2=df2.iloc[:,df2.columns.get_level_values(3)==levels[1]]
        if levels[2]!=None: 
            df=df.iloc[:,df.columns.get_level_values(4)==levels[2]]
            df2=df2.iloc[:,df2.columns.get_level_values(4)==levels[2]]
        if levels[3]!=None: 
            df=df.iloc[:,df.columns.get_level_values(5)==levels[3]]
            df2=df2.iloc[:,df2.columns.get_level_values(5)==levels[3]]
        if levels[4]!=None: 
            df=df.iloc[:,df.columns.get_level_values(6)==levels[4]]
            df2=df2.iloc[:,df2.columns.get_level_values(6)==levels[4]]
    
        print ("WE", df.columns)
        print ('We', df2.columns)
    
        fig = plt.figure(figsize=(16./2.54, 10/2.54))
        fig.subplots_adjust(left=0.1)
        # gs1 = gridspec.GridSpec(1, 1)
        # ax = plt.subplot(gs1[0, :])    
        #ax = fig.add_axes([0.13, 0.1, .85, .8])
        ax = fig.add_axes([0.13, 0.355, .85, .55])
        for index,column in enumerate(df.columns.values):
            if index!=10: ax.plot(df.index, df[column], colors[index], linewidth=2.0,label=labels[index],alpha=0.4)
         
        for index,column in enumerate(df2.columns.values):
            if index!=10: ax.plot(df.index, df2[column], colors[index], marker="x", linewidth=0.7,markevery=60,mfc='None', mec=colors[index],label=labels[index]+' Sim')   

        ax.set_ylabel("Proportion of window open")        
        ax.yaxis.set_label_coords(-0.09, 0.5)
        ax.set_xlabel("Time of the day")
        ticks = ax.get_xticks()
        ax.set_ylim(0,1)
        plt.title(title, y=1.05)
        box = ax.get_position()
        #ax.set_position([box.x0, box.y0 + box.height * 0.32,
        #             box.width, box.height * 0.68])
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
        ax.legend(loc='upper center', bbox_to_anchor=(0.475, -0.2),frameon=False, ncol=3)
        #ax.yaxis.grid(True,zorder=0, color="Gainsboro", ls="-")
        #ax.xaxis.grid(False)
        plt.savefig(savingFolder+name+'.pdf',figure=fig,  format='pdf')
        fig2= plt.figure(figsize=(16./2.54, 10/2.54))
        fig2.subplots_adjust(left=0.1)
        #gs2 = gridspec.GridSpec(1, 1)
        #ax2 = fig2.add_subplot(gs2[0, :])    
        ax2 = fig2.add_axes([0.13, 0.355, .85, .55])
        plt.title(title, y=1.05)
    
        bp = ax2.boxplot(df2.values-df.values, sym='-', vert=True, whis=1.5)#, linewidth=2.0,label=labels[index],alpha=0.4)
        # Now fill the boxes with desired colors
        boxColors = colors
        bisColors = [a for a in colors for i in range(2)]
        numBoxes = 6
        medians = range(numBoxes)
        meanValues=DataFrame(df2.values-df.values).mean(axis=0).values
        meanAbsResiduals=DataFrame(abs(df2.values-df.values)).mean(axis=0).values
    
        for i in range(numBoxes):
            box = bp['boxes'][i]
            boxY = []
            boxX = []
            for j in range(5):
                boxX.append(box.get_xdata()[j])
                boxY.append(box.get_ydata()[j])
            boxCoords = zip(boxX,boxY)
            boxPolygon = Polygon(boxCoords, facecolor=boxColors[i], alpha=0.1,zorder=1)
            ax2.add_patch(boxPolygon)
            # Now draw the median lines back over what we just filled in
            med = bp['medians'][i]
            medianX = []
            medianY = []
            for j in range(2):
                medianX.append(med.get_xdata()[j])
                medianY.append(med.get_ydata()[j])
                plt.plot(medianX, medianY, boxColors[i],linewidth=2)
                medians[i] = medianY[0]
            # Finally, overplot the sample averages, with horizontal alignment
            # in the center of each box
            plt.plot([np.average(med.get_xdata())], meanValues[i],
                  color='None', marker='o', markeredgecolor=boxColors[i], markersize=7,zorder=0)
            plt.plot([np.average(med.get_xdata())], meanValues[i],
                  color=boxColors[i], marker='o', markeredgecolor=boxColors[i], markersize=7,alpha=0.2,zorder=3)
            plt.setp(bp['medians'][i], color=colors[i]) # DarkSlateGray 
            plt.setp(bp['boxes'][i], color='DarkSlateGray')
    
        for i in range(len(bisColors)):
            plt.setp(bp['whiskers'][i], color='DarkSlateGray')
            plt.setp(bp['caps'][i], color='DarkSlateGray')
        plt.setp(bp['fliers'], color='Gainsboro')
        plt.setp(bp['whiskers'], linestyle='solid')   
        
        ax2.set_ylabel("Simulated-Observed WP profile")
        ax2.yaxis.set_label_coords(-0.09, 0.5)
        ax2.set_ylim(-0.1,0.1)
        #ax2.set_yticks([0.2, 0.6, 0.8], minor=False)
        ax2.yaxis.set_ticks_position('left')
        ax2.xaxis.set_ticks_position('bottom')
        #newLabels= ["ATR",'DAT $\leq$ 5'," 5 $\leq$ \nDAT\n $\leq$ 11", "11 $\leq$ \nDAT\n $\leq$ 14","14 $\leq$ \nDAT\n $\leq$ 18","DAT $\geq$ 18"]
        xtickNames = plt.setp(ax2, xticklabels=labels) 
        plt.setp(xtickNames,rotation=30)#, fontsize=8
        ax2.yaxis.grid(True,zorder=0, color="Gainsboro", ls="-")
        ax2.xaxis.grid(False)
        ax2.set_axisbelow(True)

        plt.savefig(savingFolder+title+'_BP.pdf',figure=fig2,  format='pdf')
        #plt.show()
        return meanValues, str(levels), meanAbsResiduals

def plotDiurnalandBoxesBeta(df,df2, labels=[],levels=[],timeType='Standard Diurnal',dataType='MD',title=None,colors=None, savingFolder="", extraName=""):
    
    print (levels)
    if levels[1]== "B2E3" and levels[2]=='A03'and levels[3]=='Room_Kitchen':
        return np.empty(6) * np.nan, str(levels)
    else:
        oldtitle=title
        title=desmountTitle(title, extraName)
        name=buildName(oldtitle, extraName)
        if timeType!='Standard Diurnal':
            title=timeType+' - '+ title
            name=timeType+' - '+ name
        if levels[0]!=None: 
            df=df.iloc[:,df.columns.get_level_values(0)==levels[0]]
            df2=df2.iloc[:,df2.columns.get_level_values(0)==levels[0]]
        if timeType!=None: 
            df=df.iloc[:,df.columns.get_level_values(1)==timeType]
            df2=df2.iloc[:,df2.columns.get_level_values(1)==timeType]
        if dataType!=None: 
            df=df.iloc[:,df.columns.get_level_values(2)==dataType]
            df2=df2.iloc[:,df2.columns.get_level_values(2)==dataType]
        if levels[1]!=None: 
            df=df.iloc[:,df.columns.get_level_values(3)==levels[1]]
            df2=df2.iloc[:,df2.columns.get_level_values(3)==levels[1]]
        if levels[2]!=None: 
            df=df.iloc[:,df.columns.get_level_values(4)==levels[2]]
            df2=df2.iloc[:,df2.columns.get_level_values(4)==levels[2]]
        if levels[3]!=None: 
            df=df.iloc[:,df.columns.get_level_values(5)==levels[3]]
            df2=df2.iloc[:,df2.columns.get_level_values(5)==levels[3]]
        if levels[4]!=None: 
            df=df.iloc[:,df.columns.get_level_values(6)==levels[4]]
            df2=df2.iloc[:,df2.columns.get_level_values(6)==levels[4]]
    

    
        fig = plt.figure(figsize=(16./2.54, 9/2.54))
        fig.subplots_adjust(left=0.1)
        # gs1 = gridspec.GridSpec(1, 1)
        # ax = plt.subplot(gs1[0, :])    
        #ax = fig.add_axes([0.13, 0.1, .85, .8])
        ax = fig.add_axes([0.13, 0.4, .85, .5])
        for index,column in enumerate(df.columns.values):
            if index!=10: ax.plot(df.index, df[column], colors[index], linewidth=2.0,label=labels[index],alpha=0.4)
         
        for index,column in enumerate(df2.columns.values):
            if index!=10: ax.plot(df.index, df2[column], colors[index], marker="x", linewidth=0.7,markevery=60,mfc='None', mec=colors[index],label=labels[index]+' Sim')   
        
        if timeType=='Standard Diurnal': ax.set_ylabel("SD - Aver. WS, "+str(title.split(", ")[1]))        
        if timeType=='Week End': ax.set_ylabel("WE - Aver. WS, "+str(title.split(", ")[1]))        
        if timeType=='Week': ax.set_ylabel("WD - Aver. WS, "+str(title.split(", ")[1]))        
        ax.yaxis.set_label_coords(-0.09, 0.5)
        ax.set_xlabel("Time of the day")
        ticks = ax.get_xticks()
        ax.set_ylim(0,1)
        #plt.title(title, y=1.05)
        box = ax.get_position()
        #ax.set_position([box.x0, box.y0 + box.height * 0.32,
        #             box.width, box.height * 0.68])
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
        ax.legend(loc='upper center', bbox_to_anchor=(0.475, -0.25),frameon=False, ncol=3)
        #ax.yaxis.grid(True,zorder=0, color="Gainsboro", ls="-")
        #ax.xaxis.grid(False)
        titleb=str(np.char.replace(title," ", ''))
        titleb=str(np.char.replace(titleb,",", '_'))
        plt.savefig(savingFolder+titleb+'.pdf',figure=fig,  format='pdf')
        fig2= plt.figure(figsize=(16./2.54, 9/2.54))
        fig2.subplots_adjust(left=0.1)
        #gs2 = gridspec.GridSpec(1, 1)
        #ax2 = fig2.add_subplot(gs2[0, :])    
        ax2 = fig2.add_axes([0.13, 0.4, .85, .5])
        #plt.title(title, y=1.05)
        print('start')
        print (df2.head(1))
        print('break')
        #print (df.head(1))
        print('stop')
        bp = ax2.boxplot(df2.values-df.values, sym='-', vert=True, whis=1.5)#, linewidth=2.0,label=labels[index],alpha=0.4)
        # Now fill the boxes with desired colors
        boxColors = colors
        bisColors = [a for a in colors for i in range(2)]
        numBoxes = 6
        medians = range(numBoxes)
        meanValues=DataFrame(df2.values-df.values).mean(axis=0).values
        meanAbsResiduals=DataFrame(abs(df2.values-df.values)).mean(axis=0).values
    
        for i in range(numBoxes):
            box = bp['boxes'][i]
            boxY = []
            boxX = []
            for j in range(5):
                boxX.append(box.get_xdata()[j])
                boxY.append(box.get_ydata()[j])
            boxCoords = zip(boxX,boxY)
            boxPolygon = Polygon(boxCoords, facecolor=boxColors[i], alpha=0.1,zorder=1)
            ax2.add_patch(boxPolygon)
            # Now draw the median lines back over what we just filled in
            med = bp['medians'][i]
            medianX = []
            medianY = []
            for j in range(2):
                medianX.append(med.get_xdata()[j])
                medianY.append(med.get_ydata()[j])
                plt.plot(medianX, medianY, boxColors[i],linewidth=2)
                medians[i] = medianY[0]
            # Finally, overplot the sample averages, with horizontal alignment
            # in the center of each box
            plt.plot([np.average(med.get_xdata())], meanValues[i],
                  color='None', marker='o', markeredgecolor=boxColors[i], markersize=7,zorder=0)
            plt.plot([np.average(med.get_xdata())], meanValues[i],
                  color=boxColors[i], marker='o', markeredgecolor=boxColors[i], markersize=7,alpha=0.2,zorder=3)
            plt.setp(bp['medians'][i], color=colors[i]) # DarkSlateGray 
            plt.setp(bp['boxes'][i], color='DarkSlateGray')
    
        for i in range(len(bisColors)):
            plt.setp(bp['whiskers'][i], color='DarkSlateGray')
            plt.setp(bp['caps'][i], color='DarkSlateGray')
        plt.setp(bp['fliers'], color='Gainsboro')
        plt.setp(bp['whiskers'], linestyle='solid')   
        
        if timeType=='Standard Diurnal': ax2.set_ylabel("SD - Sim.-Obs. WS, "+str(title.split(", ")[1]))        
        if timeType=='Week End': ax2.set_ylabel("WE - Sim.-Obs. WS, "+str(title.split(", ")[1]))        
        if timeType=='Week': ax2.set_ylabel("WD - Sim.-Obs. WS, "+str(title.split(", ")[1]))           
        ax2.set_ylabel("Sim.-Obs. WS, "+str(title.split(", ")[1]))
        ax2.yaxis.set_label_coords(-0.09, 0.5)
        ax2.set_ylim(-0.1,0.1)
        #ax2.set_yticks([0.2, 0.6, 0.8], minor=False)
        ax2.yaxis.set_ticks_position('left')
        ax2.xaxis.set_ticks_position('bottom')
        #newLabels= ["ATR",'DAT $\leq$ 5'," 5 $\leq$ \nDAT\n $\leq$ 11", "11 $\leq$ \nDAT\n $\leq$ 14","14 $\leq$ \nDAT\n $\leq$ 18","DAT $\geq$ 18"]
        xtickNames = plt.setp(ax2, xticklabels=labels) 
        plt.setp(xtickNames,rotation=30)#, fontsize=8
        ax2.yaxis.grid(True,zorder=0, color="Gainsboro", ls="-")
        ax2.xaxis.grid(False)
        ax2.set_axisbelow(True)
        title=str(np.char.replace(title," ", ''))
        title=str(np.char.replace(title,",", '_'))
        #plt.show()
        plt.savefig(savingFolder+title+'_BP.pdf',figure=fig2,  format='pdf')
        
        return meanValues, str(levels), meanAbsResiduals

def desmountTitle(title,startTitle):
    newTitle=startTitle
    for i, word in enumerate(title):
        if i== len(title)-1: newTitle=newTitle+str(word)
        else:
            if i==0: 
                newTitle=startTitle+' - '
            else:
                newTitle=newTitle+str(word)+', '
                
    return newTitle

def buildName(title,startTitle):
    newTitle=startTitle
    for i, word in enumerate(title):
        if i== len(title)-1: newTitle=newTitle+str(word)
        else:
            if i==0: 
                newTitle=startTitle+'_'
            else:
                newTitle=newTitle+str(word)+'_'
                
    return newTitle


if __name__ == '__main__':
    print ("Start main")
    recordFolder='D:/dc224615_Ddiss/Documento/Pictures/MCValidation/B2E1/'
    recFolder='D:/EBC0018_PTJ_Volkswohnung_tos/HDF-Programming/pd4hdf/MarkovChain/MC4Windows/records/'
    df1=pd.read_csv(recFolder+'diurnals/B2E1_20121_201212diurnals.csv', index_col=0, sep=';', header=[0,1,2,4,5,6,7],skiprows=[8],  parse_dates=True,low_memory=False)
#    df1=pd.read_csv(recFolder+'diurnals3/B2E1_20121_201212diurnals_MD.csv', index_col=0, sep=';', header=[0,1,2,4,5,6,7],skiprows=[8],  parse_dates=True,low_memory=False)
    df2=pd.read_csv(recFolder+'validationM3_B2E1/proSet_100_B2E1_CDPL.csv', index_col=0, sep=';', header=[0,1,2,4,5,6,7],skiprows=[8],  parse_dates=True,low_memory=False)
    
    roomsWP1        = ['Room_Kitchen','Room_Bath','Room_Living']
    roomsWP         = ['Room_Children','Room_Sleeping']
    entrances       = ["B2E1"]#,"B2E2","B2E3","B3E1","B3E2","B3E3"]
    apartments      = ["A01","A02","A03","A04","A05","A06","A07","A08","A09","A10"]
    #apartmentsPlus  = ["A01","A02","A03","A04","A05","A06","A07","A08","A09","A10",'-']
    results=[]
    indicis=[]
    columns4Results=[]
    for entrance in entrances:
        for apartment in apartments:
            for room in roomsWP1:
                colors,markers,title,labels,keys = Select_ColorsAndMarkers(Level0 = None , Level2=entrance, Level3 = apartment,Level4 = room,Level5 = "WP1")
                title,labels = english2English(title,labels)
                keys = codifyL1(keys)
                values,indice=plotDiurnalandBoxes(df1,df2,levels=keys,labels=labels,title=title,colors=colors,savingFolder=recordFolder,extraName='2012')
                results.append(values)
                indicis.append(indice)
            for room in roomsWP:
                print (entrance, apartment, room)
                colors,markers,title,labels,keys = Select_ColorsAndMarkers(Level0 = None , Level2=entrance, Level3 = apartment,Level4 = room,Level5 = "WP")
                title,labels = english2English(title,labels)
                keys = codifyL1(keys)
                values,indice=plotDiurnalandBoxes(df1,df2,levels=keys,labels=labels,title=title,colors=colors,savingFolder=recordFolder,extraName='2012')
                results.append(values)
                indicis.append(indice)
    columns4Results=labels
    print (results)
    resultDF=DataFrame(results, index=indicis,columns=columns4Results)
    resultDF.to_csv(recordFolder+"results.csv", ';')
    print ("end main")