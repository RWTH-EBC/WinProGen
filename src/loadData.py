'''
Created on 18.03.2015

@author: Davide Calì
'''

import pandas as pd
from pandas import DataFrame, MultiIndex
import datetime as dt
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta
import h5py
import numpy as np
import datetime



class meda(object):
    '''
    class containing the data object (a apandas DataFrame) with multicolumns
    '''
    def __init__(self,flatname=None):
        self._dfglob=DataFrame()

        
    def genLevels(self):    ###### used (but always commented)
        '''
        convertion of the columns names (in tuple format) 
        of the main dataframe to multiIndex
        '''
        cols=MultiIndex.from_tuples(self._dfglob.columns.values)
        self._dfglob.columns=cols
    
    def viewer_time_to_datetime(self,viewer_timevector, roundTo=None):
        ''' Will create a pandas-accesible datetime-time-vector instead of the time-format
        used in the hdf5-File and in the hdf5-EBC-viewer.
        '''
        def roundTime(dt=None, roundTo=60):
           """Round a datetime object to any time laps in seconds
           dt : datetime.datetime object, default now.
           roundTo : Closest number of seconds to round to, default 1 minute.
           """
           if dt == None : dt = datetime.datetime.now()
           seconds = (dt - dt.min).seconds
           # // is a floor division, not a comment on following line:
           rounding = (seconds+roundTo/2) // roundTo * roundTo
           dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)
           dt.replace(second=0, microsecond=0)
           return dt

        def to_datetime(time_value, roundTo=60):
            # NOTE: a much nicer methods, but it leaves milliseconds and I prefer a less exact rounding: http://stackoverflow.com/questions/26187139/create-a-datetime-time-object-just-from-seconds/26187347#26187347
            ''' Convert one time-value into datetime-object
            '''
            dt = datetime.datetime.min + datetime.timedelta(days=time_value - 1)
            if roundTo!=None:
                dt=roundTime(dt,roundTo)
            return dt

        time_vec = map(to_datetime,viewer_timevector)
        return time_vec
    
    def _unifyWP(self,level=3):
        '''
        to be called before using the data of the main DataFrame
        change the 10-0 signal (window open/closed) into 1-0.        
        '''
        self._dfglob.iloc[:, self._dfglob.columns.get_level_values(level)=='WP1']=self._dfglob.iloc[:, self._dfglob.columns.get_level_values(level)=='WP1']/10
        self._dfglob.iloc[:, self._dfglob.columns.get_level_values(level)=='WP2']=self._dfglob.iloc[:, self._dfglob.columns.get_level_values(level)=='WP2']/10
    
    def _loadTimeGroup(self,h5file,group2go=None,columnNames=[],limit2=[],exclude=[]):
        '''
        method to open leafs from a selected group.
        It allows for leaf inclusion or exclusion.
        intergroups should be provided separated by a slash
        as a string, in the "group2go" argument.
        columnNames useful for multiindexing is a list. 
        it will be as column name up to the level before the leaf name
        '''
        exclude=exclude+["Time"]
        keys=h5file[group2go].keys()
        try: time = np.ndarray.flatten(
                            h5file[group2go+"/Time"][:])
        except KeyError:
            print ("Oops, ", group2go, "doesn't exist!")
            adr=DataFrame()
        else:
            timeArr = self.viewer_time_to_datetime(time, 60)
            data_dict = {}
            divideWP=10
            for key in keys:
                if limit2!=[]:
                    if key in limit2:
                        data_dict[tuple(columnNames+[key])] = np.ndarray.flatten(h5file[group2go+"/"+key][:])
                else:
                    if key not in exclude:
                        data_dict[tuple(columnNames+[key])] = np.ndarray.flatten(h5file[group2go+"/"+key][:])
    
            adr=pd.DataFrame(data = data_dict,index = timeArr)
            adr["index"] = adr.index
            adr.drop_duplicates(subset='index', keep='last', inplace=True)
            del adr["index"]

        return adr

    def loadAT(self,Year=2013, Month=1):
        Year=str(Year)
        if Month<10: Month="0"+str(Month)
        else: Month=str(Month)
        FileName='D:/HDF-Archive/iiiHD_'+str(Year)+'_'+Month+'.hdf5'
        h5file = h5py.File(FileName,'r')
        time = np.ndarray.flatten(
                             h5file['Field_Test']['Weather_Station']['Time'][:])
        data_dict = {}
        data_dict[("Weather","-","-",'AT')] = np.ndarray.flatten(
                            h5file['Field_Test']['Weather_Station']['AT'][:])
        time = self.viewer_time_to_datetime(time, 60)
        df=pd.DataFrame(data = data_dict,index = time)

    def openFile(self, Year=2013, Month=1):
        '''
        Method to open a HDF File based on the asked month and year
        '''
        Year=str(Year)
        if Month<10: Month="0"+str(Month)
        else: Month=str(Month)
        FileName='D:/HDF-Archive/iiiHD_'+str(Year)+'_'+Month+'.hdf5'
        print (FileName)
        h5file = h5py.File(FileName,'r')
        return h5file
    
    def prepare4Room(self,Building=2,Entrance=1,Apartment=1,Room="Children"):
        '''
        Method to generate the column names including building (e.g. B2E1), apartment  and room
        '''
        Building=str(Building)
        Entrance=str(Entrance)
        if Apartment<10: Apartment="0"+str(Apartment)
        else: Apartment=str(Apartment)
        Room="Room"+"_"+Room
        print ("Loading ", Room)
        bdCode="B"+Building+"E"+Entrance 
        ApCode="A"+Apartment
        group2go='Field_Test/Building_'+Building+'/Entrance_B'+Building+'E'+Entrance+'/Apartment_'+Apartment+'/'+Room+'/RMU/'
        columnName=[bdCode, ApCode, Room]
        return Building, Entrance, Apartment, Room, group2go, columnName
    
    def findWiloGroup(self,Building=2,Entrance=1,Apartment=1,Room="Children"):
        
        group2go='Field_Test/Building_'+Building+'/Entrance_B'+Building+'E'+Entrance+'/Apartment_'+Apartment+'/'+Room+'/Wilo_Pump/'
        return group2go
    
        
        
    def loadRoomRMU(self, Year=2013, Month=1,Building=2,Entrance=1,Apartment=1,Room="Children",loadAmbTemp=True,limit2=[],esclude=[],df2glob=True,h5file=None, WeatherLimit2=["AT","Wind_Speed"],Wilo=False, WiloLimit2=['WRT', 'Set_Temp', 'Set_Temp_2']):
        '''
        limit2 and Exclude only refer to the RMU group
        '''
        if h5file==None: 
            h5file=self.openFile(Year,Month)
        Building, Entrance, Apartment, Room, group2go, columnName=self.prepare4Room(Building, Entrance, Apartment, Room)
        group2goWilo=self.findWiloGroup(Building, Entrance, Apartment, Room)
        temp=self._loadTimeGroup(h5file,group2go, columnName,limit2,esclude)
        if df2glob==True:
            self._dfglob=temp
            if loadAmbTemp==True:
                group2go='Field_Test/Weather_Station'
                columnName=["Weather","-","-"]
                Wlimit2=WeatherLimit2
                temp=self._loadTimeGroup(h5file,group2go, columnName,Wlimit2)

                self._dfglob=self._dfglob.join(temp)
            if Wilo==True:
                print ('load Wilo')
                temp=self._loadTimeGroup(h5file,group2goWilo, columnName,WiloLimit2)
                self._dfglob=self._dfglob.join(temp)
            self._unifyWP()
        else:
            if loadAmbTemp==True:
                print ("Warning, not including AT at this stage")
            return temp

    def loadAparRMU(self,Year=2013, Month=1,Building=2,Entrance=1,Apartment=1,loadAmbTemp=True,limit2=[],esclude=[],df2glob=True,h5file=None, WeatherLimit2=["AT","Wind_Speed"],Wilo=False, WiloLimit2=['WRT', 'Set_Temp', 'Set_Temp_2']):
        if h5file==None: h5file=self.openFile(Year,Month)
        Rooms=["Living","Kitchen","Sleeping","Children","Bath"]
        print ("Loading apartment ", Apartment)
        RL1=self.loadRoomRMU(Year, Month, Building, Entrance, Apartment, Rooms[0], False, limit2, esclude, False, h5file,Wilo, WiloLimit2)
        RK1=self.loadRoomRMU(Year, Month, Building, Entrance, Apartment, Rooms[1], False, limit2, esclude, False, h5file,Wilo, WiloLimit2)
        RS1=self.loadRoomRMU(Year, Month, Building, Entrance, Apartment, Rooms[2], False, limit2, esclude, False, h5file,Wilo, WiloLimit2)
        RC1=self.loadRoomRMU(Year, Month, Building, Entrance, Apartment, Rooms[3], False, limit2, esclude, False, h5file,Wilo, WiloLimit2)
        RB1=self.loadRoomRMU(Year, Month, Building, Entrance, Apartment, Rooms[4], False, limit2, esclude, False, h5file,Wilo, WiloLimit2)
        
        lenAr=(RL1.shape[0],RK1.shape[0],RS1.shape[0],RC1.shape[0],RB1.shape[0])
        joinAr=[lenAr[0]]
        for indexlA, size in enumerate(lenAr):
            if indexlA>0:
                if joinAr[0]!=size:
                    joinAr.append(size)
        print (joinAr)
                
        if loadAmbTemp==True:
                print ("I join all...")
                group2go='Field_Test/Weather_Station'
                columnName=["Weather","-","-"]
                Wlimit2=WeatherLimit2
                df=self._loadTimeGroup(h5file,group2go, columnName,Wlimit2)
                
                joinIt=[RK1,RS1,RC1,RB1,df]
                RL1=RL1.join(joinIt, how="outer")
                
                temp=RL1
        else:
            if len(joinAr)==1:
                print ("I concat")
                temp=pd.concat([RL1,RK1,RS1,RC1,RB1],axis=1, join="outer")
            else:
                print ("I join")
                temp=RL1.join([RK1,RS1,RC1,RB1], how="outer")        
        
        if df2glob==True:
            
            self._dfglob=temp
            self._unifyWP()
        else:
            return temp


    def loadEntrRMU(self,Year=2013, Month=1,Building=2,Entrance=1,loadAmbTemp=True,limit2=[],esclude=[],df2glob=True,h5file=None, WeatherLimit2=["AT","Wind_Speed"],Wilo=False, WiloLimit2=['WRT', 'Set_Temp', 'Set_Temp_2']):
        if h5file==None: h5file=self.openFile(Year,Month)
        
        A1=self.loadAparRMU(Year, Month, Building, Entrance, 1, False, limit2, esclude, False, h5file,Wilo, WiloLimit2)
        A2=self.loadAparRMU(Year, Month, Building, Entrance, 2, False, limit2, esclude, False, h5file,Wilo, WiloLimit2)
        A3=self.loadAparRMU(Year, Month, Building, Entrance, 3, False, limit2, esclude, False, h5file,Wilo, WiloLimit2)
        A4=self.loadAparRMU(Year, Month, Building, Entrance, 4, False, limit2, esclude, False, h5file,Wilo, WiloLimit2)
        A5=self.loadAparRMU(Year, Month, Building, Entrance, 5, False, limit2, esclude, False, h5file,Wilo, WiloLimit2)
        A6=self.loadAparRMU(Year, Month, Building, Entrance, 6, False, limit2, esclude, False, h5file,Wilo, WiloLimit2)
        A7=self.loadAparRMU(Year, Month, Building, Entrance, 7, False, limit2, esclude, False, h5file,Wilo, WiloLimit2)
        A8=self.loadAparRMU(Year, Month, Building, Entrance, 8, False, limit2, esclude, False, h5file,Wilo, WiloLimit2)
        A9=self.loadAparRMU(Year, Month, Building, Entrance, 9, False, limit2, esclude, False, h5file,Wilo, WiloLimit2)
        A10=self.loadAparRMU(Year, Month, Building, Entrance, 10, False, limit2, esclude, False, h5file,Wilo, WiloLimit2)

        lenAr=(A1.shape[0],A2.shape[0],A3.shape[0],A4.shape[0],A5.shape[0],A6.shape[0],A7.shape[0],A8.shape[0],A9.shape[0],A10.shape[0])

        joinAr=[lenAr[0]]
        for indexlA, size in enumerate(lenAr):
            if indexlA>0:
                if joinAr[0]!=size:
                    joinAr.append(size)
        print (joinAr)
        if loadAmbTemp==True:
                group2go='Field_Test/Weather_Station'
                columnName=["Weather","-","-"]
                Wlimit2=WeatherLimit2
                df=self._loadTimeGroup(h5file,group2go, columnName,Wlimit2)
                
                temp=A1.join([A2,A3,A4,A5,A6,A7,A8,A9,A10,df], how="outer")

        else:
            if len(joinAr)!=1:
                print ("I concat")
                temp=pd.concat([A1,A2,A3,A4,A5,A6,A7,A8,A9,A10],axis=1, join="outer")
            else:
                print ("I join")
                temp=A1.join([A2,A3,A4,A5,A6,A7,A8,A9,A10], how="outer")

        if df2glob==True:
            self._dfglob=temp
            self._unifyWP()
        else:
            return temp

    def loadBuilding(self,Year=2013, Month=1,Building=2,loadAmbTemp=True):
        '''
        this method is not yet up to date with the others...
        better don't use it
        '''
        Entrances=['1','2','3']
        Apartments = ['01','02','03','04','05','06','07','08','09','10']
        Rooms=["Room_Living","Room_Kitchen","Room_Sleeping","Room_Children","Room_Bath"]
        if Month<10: Month="0"+str(Month)
        else: Month=str(Month)
        Building=str(Building)
        
        FileName='D:/HDF-Archive/iiiHD_'+str(Year)+'_'+Month+'.hdf5'
        h5file = h5py.File(FileName,'r')
        for Entrance in Entrances:
            
            RL1=self._loadRMU(Rooms[0],Apartments[0],Entrance,Building,h5file)
            RK1=self._loadRMU(Rooms[1],Apartments[0],Entrance,Building,h5file)
            RS1=self._loadRMU(Rooms[2],Apartments[0],Entrance,Building,h5file)
            RC1=self._loadRMU(Rooms[3],Apartments[0],Entrance,Building,h5file)
            RB1=self._loadRMU(Rooms[4],Apartments[0],Entrance,Building,h5file)
            
            RL2=self._loadRMU(Rooms[0],Apartments[1],Entrance,Building,h5file)
            RK2=self._loadRMU(Rooms[1],Apartments[1],Entrance,Building,h5file)
            RS2=self._loadRMU(Rooms[2],Apartments[1],Entrance,Building,h5file)
            RC2=self._loadRMU(Rooms[3],Apartments[1],Entrance,Building,h5file)
            RB2=self._loadRMU(Rooms[4],Apartments[1],Entrance,Building,h5file)
            
            RL3=self._loadRMU(Rooms[0],Apartments[2],Entrance,Building,h5file)
            RK3=self._loadRMU(Rooms[1],Apartments[2],Entrance,Building,h5file)
            RS3=self._loadRMU(Rooms[2],Apartments[2],Entrance,Building,h5file)
            RC3=self._loadRMU(Rooms[3],Apartments[2],Entrance,Building,h5file)
            RB3=self._loadRMU(Rooms[4],Apartments[2],Entrance,Building,h5file)
            
            RL4=self._loadRMU(Rooms[0],Apartments[3],Entrance,Building,h5file)
            RK4=self._loadRMU(Rooms[1],Apartments[3],Entrance,Building,h5file)
            RS4=self._loadRMU(Rooms[2],Apartments[3],Entrance,Building,h5file)
            RC4=self._loadRMU(Rooms[3],Apartments[3],Entrance,Building,h5file)
            RB4=self._loadRMU(Rooms[4],Apartments[3],Entrance,Building,h5file)
            
            RL5=self._loadRMU(Rooms[0],Apartments[4],Entrance,Building,h5file)
            RK5=self._loadRMU(Rooms[1],Apartments[4],Entrance,Building,h5file)
            RS5=self._loadRMU(Rooms[2],Apartments[4],Entrance,Building,h5file)
            RC5=self._loadRMU(Rooms[3],Apartments[4],Entrance,Building,h5file)
            RB5=self._loadRMU(Rooms[4],Apartments[4],Entrance,Building,h5file)
            
            RL6=self._loadRMU(Rooms[0],Apartments[5],Entrance,Building,h5file)
            RK6=self._loadRMU(Rooms[1],Apartments[5],Entrance,Building,h5file)
            RS6=self._loadRMU(Rooms[2],Apartments[5],Entrance,Building,h5file)
            RC6=self._loadRMU(Rooms[3],Apartments[5],Entrance,Building,h5file)
            RB6=self._loadRMU(Rooms[4],Apartments[5],Entrance,Building,h5file)
            
            RL7=self._loadRMU(Rooms[0],Apartments[6],Entrance,Building,h5file)
            RK7=self._loadRMU(Rooms[1],Apartments[6],Entrance,Building,h5file)
            RS7=self._loadRMU(Rooms[2],Apartments[6],Entrance,Building,h5file)
            RC7=self._loadRMU(Rooms[3],Apartments[6],Entrance,Building,h5file)
            RB7=self._loadRMU(Rooms[4],Apartments[6],Entrance,Building,h5file)
            
            RL8=self._loadRMU(Rooms[0],Apartments[7],Entrance,Building,h5file)
            RK8=self._loadRMU(Rooms[1],Apartments[7],Entrance,Building,h5file)
            RS8=self._loadRMU(Rooms[2],Apartments[7],Entrance,Building,h5file)
            RC8=self._loadRMU(Rooms[3],Apartments[7],Entrance,Building,h5file)
            RB8=self._loadRMU(Rooms[4],Apartments[7],Entrance,Building,h5file)
            
            RL9=self._loadRMU(Rooms[0],Apartments[8],Entrance,Building,h5file)
            RK9=self._loadRMU(Rooms[1],Apartments[8],Entrance,Building,h5file)
            RS9=self._loadRMU(Rooms[2],Apartments[8],Entrance,Building,h5file)
            RC9=self._loadRMU(Rooms[3],Apartments[8],Entrance,Building,h5file)
            RB9=self._loadRMU(Rooms[4],Apartments[8],Entrance,Building,h5file)
            
            RL10=self._loadRMU(Rooms[0],Apartments[9],Entrance,Building,h5file)
            RK10=self._loadRMU(Rooms[1],Apartments[9],Entrance,Building,h5file)
            RS10=self._loadRMU(Rooms[2],Apartments[9],Entrance,Building,h5file)
            RC10=self._loadRMU(Rooms[3],Apartments[9],Entrance,Building,h5file)
            RB10=self._loadRMU(Rooms[4],Apartments[9],Entrance,Building,h5file)
            
            En1=pd.concat([RL1,RK1,RS1,RC1,RB1,RL2,RK2,RS2,RC2,RB2,RL3,RK3,RS3,RC3,RB3,RL4,RK4,RS4,RC4,RB4,RL5,RK5,RS5,RC5,RB5,RL6,RK6,RS6,RC6,RB6,RL7,RK7,RS7,RC7,RB7,RL8,RK8,RS8,RC8,RB8,RL9,RK9,RS9,RC9,RB9,RL10,RK10,RS10,RC10,RB10],axis=1, join="outer")
            En2=pd.concat([RL1,RK1,RS1,RC1,RB1,RL2,RK2,RS2,RC2,RB2,RL3,RK3,RS3,RC3,RB3,RL4,RK4,RS4,RC4,RB4,RL5,RK5,RS5,RC5,RB5,RL6,RK6,RS6,RC6,RB6,RL7,RK7,RS7,RC7,RB7,RL8,RK8,RS8,RC8,RB8,RL9,RK9,RS9,RC9,RB9,RL10,RK10,RS10,RC10,RB10],axis=1, join="outer")
            En3=pd.concat([RL1,RK1,RS1,RC1,RB1,RL2,RK2,RS2,RC2,RB2,RL3,RK3,RS3,RC3,RB3,RL4,RK4,RS4,RC4,RB4,RL5,RK5,RS5,RC5,RB5,RL6,RK6,RS6,RC6,RB6,RL7,RK7,RS7,RC7,RB7,RL8,RK8,RS8,RC8,RB8,RL9,RK9,RS9,RC9,RB9,RL10,RK10,RS10,RC10,RB10],axis=1, join="outer")

        if loadAmbTemp==True:
            df=self.loadAT(Year, Month)
            self._dfglob=self._dfglob.join(df)
            temp=En1.join([En2,En3,df],how="outer")

        else: temp=En1.join([En2,En3],how="outer")


    def viewer_time_to_datetime(self,viewer_timevector, roundTo=None):
        '''
        Will create a pandas-accesible datetime-time-vector instead of the time-format
        used in the hdf5-Viewer
        '''

        def roundTime(dt=None, roundTo=60):
            """Round a datetime object to any time laps in seconds
            dt : datetime.datetime object, default now.
            roundTo : Closest number of seconds to round to, default 1 minute.
            """
            if dt == None : dt = datetime.datetime.now()
            seconds = (dt - dt.min).seconds
            # // is a floor division, not a comment on following line:
            rounding = (seconds+roundTo/2) // roundTo * roundTo
            return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)

        def to_datetime(time_value):
            # NOTE: a much nicer methods, but it leaves milliseconds and I prefer a less exact rounding: http://stackoverflow.com/questions/26187139/create-a-datetime-time-object-just-from-seconds/26187347#26187347
            ''' Convert one time-value into datetime-object
            '''
            date = datetime.datetime.fromordinal(int(time_value))
            seconds = round((time_value - int(time_value)) * 86400)
            date_and_time = date + datetime.timedelta(seconds = seconds)
            if roundTo!=None:
                date_and_time=roundTime(date_and_time,roundTo)
            return date_and_time
        time_vec = map(to_datetime,viewer_timevector)
        return time_vec

class medati(meda):
    '''
    class containing the data object with multicolumns and more months
    '''
    fig_size_default = [10.7,8.27] # as class attribute will change the plotting default size for every instance of this class

    def __init__(self):
            
        self._dfglob=DataFrame()

    def perdelta(self,start,end):
        delta=relativedelta(months=1)
        curr = start
        listFiles=[curr]
        while curr < end:
            curr+= delta
            listFiles.append(curr)
        return listFiles
        

    def loadR(self, lFrom=(2013,1), lTo=(2013,12),Building=2,Entrance=1,Apartment=1,Room="Children",loadAmbTemp=True,limit2=[],esclude=[],df2glob=True,h5file=None,WeatherLimit2=["AT","Wind_Speed"],Wilo=False, WiloLimit2=['WRT', 'Set_Temp', 'Set_Temp_2']):
        lF=self.perdelta(dt.date(lFrom[0],lFrom[1],1),dt.date(lTo[0],lTo[1],1))
        for indexlF,element in enumerate(lF):
            print (element)
            if indexlF==0:
                temp=meda()
                temp.loadRoomRMU(element.year, element.month, Building, Entrance, Apartment, Room,loadAmbTemp,limit2,esclude,df2glob,h5file,WeatherLimit2,Wilo, WiloLimit2)
                self._dfglob=temp._dfglob
            else:
                temp=meda()
                temp.loadRoomRMU(element.year, element.month, Building, Entrance, Apartment, Room,loadAmbTemp,limit2,esclude,df2glob,h5file,WeatherLimit2,Wilo, WiloLimit2)
                self._dfglob=self._dfglob.append(temp._dfglob)
                
    def loadA(self, lFrom=(2013,1), lTo=(2013,12),Building=2,Entrance=1,Apartment=1,loadAmbTemp=True,limit2=[],esclude=[],df2glob=True,h5file=None, WeatherLimit2=["AT","Wind_Speed"],Wilo=False, WiloLimit2=['WRT', 'Set_Temp', 'Set_Temp_2']):
        lF=self.perdelta(dt.date(lFrom[0],lFrom[1],1),dt.date(lTo[0],lTo[1],1))
        for indexlF,element in enumerate(lF):
            print (element)
            if indexlF==0:
                temp=meda()
                temp.loadAparRMU(element.year, element.month, Building, Entrance, Apartment, loadAmbTemp,limit2,esclude,df2glob,h5file,WeatherLimit2)
                self._dfglob=temp._dfglob
            else:
                temp=meda()
                temp.loadAparRMU(element.year, element.month, Building, Entrance, Apartment, loadAmbTemp,limit2,esclude,df2glob,h5file,WeatherLimit2)
                self._dfglob=self._dfglob.append(temp._dfglob)
                
    def loadE(self, lFrom=(2013,1), lTo=(2013,12),Building=2,Entrance=1,Apartment=1,Room="Children",loadAmbTemp=True,limit2=[],esclude=[],df2glob=True,h5file=None, WeatherLimit2=["AT","Wind_Speed"],OnlyHeatingPeriod=False):
        
        lF=self.perdelta(dt.date(lFrom[0],lFrom[1],1),dt.date(lTo[0],lTo[1],1)) 
        if OnlyHeatingPeriod==True: 
            lF=self.perdelta(dt.date(lFrom[0],1,1),dt.date(lTo[0],4,1))+self.perdelta(dt.date(lFrom[0],10,1),dt.date(lTo[0],12,1)) 
            print ("I've got it, this is the HP:",lF)

        for indexlF,element in enumerate(lF):
            print (element)
            if indexlF==0:
                temp=meda()
                temp.loadEntrRMU(element.year, element.month, Building, Entrance,loadAmbTemp,limit2,esclude,df2glob,h5file,WeatherLimit2,Wilo=False, WiloLimit2=['WRT', 'Set_Temp', 'Set_Temp_2'])
                self._dfglob=temp._dfglob
            else:
                temp=meda()
                temp.loadEntrRMU(element.year, element.month, Building, Entrance,loadAmbTemp,limit2,esclude,df2glob,h5file,WeatherLimit2,Wilo=False, WiloLimit2=['WRT', 'Set_Temp', 'Set_Temp_2'])
                self._dfglob=self._dfglob.append(temp._dfglob)
    
    def loadB(self, lFrom=(2013,1), lTo=(2013,12),Building=2,loadAmbTemp=True,limit2=[],esclude=[],df2glob=True,h5file=None, WeatherLimit2=["AT","Wind_Speed"]):
        lF=self.perdelta(dt.date(lFrom[0],lFrom[1],1),dt.date(lTo[0],lTo[1],1))
        for indexlF,element in enumerate(lF):
            print (element)
            if indexlF==0:
                temp=meda()
                temp.loadBuilding(element.year, element.month, Building,loadAmbTemp,limit2,esclude,df2glob,h5file)
                self._dfglob=temp._dfglob
            else:
                temp=meda()
                temp.loadBuilding(element.year, element.month, Building,loadAmbTemp,limit2,esclude,df2glob,h5file)
                self._dfglob=self._dfglob.append(temp._dfglob)
                
            
     
        
# if __name__ == '__main__':
#     start=time.clock()
# 
#     mD1=medati()
#     mD1.loadR((2012,1), (2012,12), 2, 1, loadAmbTemp=True)
#     print mD1._dfglob.describe()
#
#     tot=time.clock()-start
#     print "compiled in:",tot,"seconds"
