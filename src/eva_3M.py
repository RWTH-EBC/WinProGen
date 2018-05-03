'''
Created on 23.04.2015

@author: Davide Cali

File to make validation of generated WSP based on model 3
'''

from plotprops import *
import os

def check_validation_eva3(building="B2E1",
                          apartments = ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09", "A10"],
                          recFolder='D:/WinProGen/Data/',
                          years=2):
    recordFolder = 'D:/WinProGen/Data/validation/pictures/' + building + '_3M/'
    if not os.path.exists(recordFolder):
        os.makedirs(recordFolder)

    df1=pd.read_csv(recFolder+'diurnals/'+building+'_20121_201212diurnals.csv', index_col=0, sep=';', header=[0,1,2,4,5,6,7],skiprows=[8],  parse_dates=True,low_memory=False)
    #    df1=pd.read_csv(recFolder+'diurnals3/B2E1_20121_201212diurnals_MD.csv', index_col=0, sep=';', header=[0,1,2,4,5,6,7],skiprows=[8],  parse_dates=True,low_memory=False)
    df2=pd.read_csv(recFolder+'validation/temp/M3_' + str(years) + '_'+ building + '_' + '_'.join(apartments) + '.csv', index_col=0, sep=';', header=[0,1,2,4,5,6,7],skiprows=[8],  parse_dates=True,low_memory=False)

    roomsSW        = ['Room_Kitchen','Room_Bath','Room_Living']
    roomsDW         = ['Room_Children','Room_Sleeping']
    entrances       = [building]#,"B2E2","B2E3","B3E1","B3E2","B3E3"]

    #apartmentsPlus  = ["A01","A02","A03","A04","A05","A06","A07","A08","A09","A10",'-']
    results=[]
    indicis=[]
    resultsMeanAbsRes=[]
    columns4Results=[]
    for entrance in entrances:
        for apartment in apartments:
            for room in roomsSW:
                colors,markers,title,labels,keys = Select_ColorsAndMarkers(Level0 = None , Level2=entrance, Level3 = apartment,Level4 = room,Level5 = "WP1")
                title,labels = english2English(title,labels)
                keys = codifyL1(keys)
                values,indice,meanAbsResiduals=plotDiurnalandBoxesBeta(df1,df2,levels=keys,labels=labels,title=title,colors=colors,savingFolder=recordFolder,extraName='2012')
                results.append(values)
                resultsMeanAbsRes.append(meanAbsResiduals)
                indicis.append(indice)
            for room in roomsDW:
                print (entrance, apartment, room)
                colors,markers,title,labels,keys = Select_ColorsAndMarkers(Level0 = None , Level2=entrance, Level3 = apartment,Level4 = room,Level5 = "WP")
                title,labels = english2English(title,labels)
                keys = codifyL1(keys)
                values,indice,meanAbsResiduals=plotDiurnalandBoxesBeta(df1,df2,levels=keys,labels=labels,title=title,colors=colors,savingFolder=recordFolder,extraName='2012')
                results.append(values)
                resultsMeanAbsRes.append(meanAbsResiduals)
                indicis.append(indice)
    columns4Results=labels
    #print results
    resultDF=DataFrame(results, index=indicis,columns=columns4Results)
    resultDF.to_csv(recordFolder+"results.csv", ';')
    resultDFAbs=DataFrame(resultsMeanAbsRes, index=indicis,columns=columns4Results)
    resultDFAbs.to_csv(recordFolder+"resultsMeanAbsRes.csv", ';')