'''
Created on 23.04.2015

@author: Davide Cali

File to work with the Matrices, generate diurnal profile, execute MC simulation, execute MCMC validation
'''

from __future__ import print_function
from __future__ import division

from Cython.Plex.Transitions import state_set_str

from loadData import *
import calendar
import matplotlib
import time
import threading
import os
import itertools
from ast import literal_eval
from itertools import compress

idx = pd.IndexSlice

class MCM(medati):
    '''
    Markov Chain Methods
    '''        
    fig_size_default = [10.7,8.27] # as class attribute will change the plotting default size for every instance of this class

    def __init__(self,engl = True):
        
        # get data from hdf5 file:
        # Create data from parameters
        df=medati()
        self._dfglob = df._dfglob
        self.Diurnals = pd.DataFrame()
        self.TPM3x3 = pd.DataFrame()
        self.TPM2x2 = pd.DataFrame()
        self.temperature_groups=[]
        self.recFolder=os.getcwd().split("src")[0] + '/Data'

        #todo: doublececk with Lukas!
        self.TPM = pd.DataFrame()
        self.start = pd.DataFrame()
        self.duration = float(6)
        self.simDays = float(1)
        self.val_horizon = float(1)
        self.combinations = 0
        self.wsp_start_progress = 0
        self.already_done = 0
        self.turbo_marker = 0
        self.check_tpm = 0
        self.sim_year = int(0)


    def expandWith(self,newDatas):  ###### not used !!!
        '''
        '''
        self._dfglob=self._dfglob.append(newDatas)
        self.time_vector = self._dfglob.index
        print ("Expanded")
    
    def resampleDataFrame(self, timeInterval='5Min', how='mean'):  ###### not used !!!
        print ("WARNING: for WP is not a good Idea to use mean... ")
        self._dfglob=self._dfglob.resample(timeInterval, how) 

    def assign_random_to_combination(self,array,value, infos=['no info avauilable']):
        '''
        :param array: an array, containing cumulative probabilities
        :param value: the random number
        :return: an array containing the combination code
        '''
        # print(array)
        new_array=np.array(array)-value

        try:
            m = min(i for i in new_array if i >= 0)
            p = np.where(new_array==m,1,0)

            if sum(p)>1:
                new_p=[]
                for index,el in enumerate(p):
                    if index==0:
                        new_p.append(el)
                    elif sum(new_p)==1:new_p.append(0)
                    else:new_p.append(el)
                p=new_p


        except ValueError:
            print('Exception Eraised, window(s) set to closed')
            print(infos, array, value)
            p = np.zeros(len(new_array))
            p[0]=1




        return(p)


    def assign_random_to_combination_compact(self,array,value):
        '''
        :param array: an array, containing cumulative probabilities
        :param value: the random number
        :return: an array containing the combination code
        function not yet in use
        '''
        new_array=np.array(array)-value
        m = min(i for i in new_array if i >= 0)
        p = np.where(new_array==m,1,0)
        if sum(p)>0:
            new_p=[]
            for index,el in enumerate(p):
                if index==0:
                    new_p.append(el)
                elif sum(new_p)==1:new_p.append(0)
                else:new_p.append(el)
            p=new_p
        return(p)
    
    def gen_status_combs(self, cols_windows, identical_windows=[]):
        '''
        define the combination as names 2^Number of windows (present room name means window is open)
        '''
        ### Make the cartesian product of possible combinations (open/closed)
        ### of all windows in the choosen room
        cartesian_product=(list(itertools.product([0,1], repeat=len(cols_windows))))

        status_combs=[]
        for cart in cartesian_product:
            #print cart, cols
            if np.sum(cart)==0: a=['All closed']
            else:
                a= [j for i, j in zip(cart, cols_windows) if i == 1]
            status_combs.append(a)

        new_combs, new_combs_set = self.rename_identical_windows(status_combs, identical_windows)

        return status_combs, cartesian_product, new_combs, new_combs_set

    def gen_trans_combs(self,cols_windows, identical_windows=[]):
        '''
        define the combinations of transitions: (2^Number of windows)^2
        Make the cartesian product of possible combinations of change states of all windows
        and assign a combination code
        This function will be soon implemented
        '''
        status_combs, cartesian_product, new_combs, new_combs_set = self.gen_status_combs(cols_windows, identical_windows)
        #print(status_combs)
        #print(new_combs)

        trans_combs=(list(itertools.product(status_combs, repeat=2)))
        new_trans_combs=(list(itertools.product(new_combs, repeat=2)))

        cartesian_product_state_change=(list(itertools.product(cartesian_product, repeat=2)))
        codes=np.arange(len(trans_combs))

        dict_transcarts_2_transcodes=dict(zip(cartesian_product_state_change,list(codes)))

        dict_trans_combs_inv=dict(zip(list(codes),cartesian_product_state_change)) # code to proove it's everything working correctly
        flat_trans_combs=[str(a) for a in trans_combs]
        dict_trans_combs_language_to_code=dict(zip(flat_trans_combs,list(codes))) # code to proove it's everything working correctly

        flat_newtcombs=[str(a) for a in new_trans_combs]

        dict_transcombs_newttranscombs=dict(zip(flat_trans_combs,flat_newtcombs))

        new_codes=[]
        for index,element in enumerate(codes):
            new_codes.append(dict_trans_combs_language_to_code[dict_transcombs_newttranscombs[flat_trans_combs[index]]])

        dict_trans_combs_language_to_code=dict(zip(flat_newtcombs,list(codes))) # code to proove it's everything working correctly
        dict_transcarts_2_transcodes=dict(zip(cartesian_product_state_change,list(new_codes)))

        trans_combs=new_trans_combs

        return dict_transcarts_2_transcodes, trans_combs, dict_trans_combs_language_to_code,

    def rename_identical_windows(self, status_combs, identical_windows=[]): #'WP0', 'WP1', 'WP2'
        new_combs=[]
        for comb in status_combs:
            new_elements=[]
            for element in comb:
                if element in identical_windows:
                    new_elements.append(identical_windows[0])
                else:
                    new_elements.append(element)
            new_combs.append(new_elements)

        for index_comb,comb in enumerate(new_combs):
            #print(comb.count(identical_windows[0]))
            counter_pos_iw=0
            for index_el,element in enumerate(comb):
                if element in identical_windows:
                    new_combs[index_comb][index_el]=identical_windows[counter_pos_iw]
                counter_pos_iw+=1

        new_combs_set=np.unique(new_combs)

        return new_combs, new_combs_set

    ### define a status change array "change_of_state"
    ### to have information about previous and actual state of windows
    ### in each room

    def generate_df_trans(self, identical_windows=[]):
        '''
        generate a transiction matrix
        :param identical_windows:
        :return:
        generates self.df_transiction_matrix
        '''
        self.df_transiction_matrix=pd.DataFrame(index=self._dfglob.index)
        #names=['Datatype','Trans_start','Trans_stop', 'building', 'zone', 'room']
        df_status_change=pd.DataFrame(index=self._dfglob.index)
        for building in self.cols_building:
            for zone in self.cols_zone:
                for room in self.cols_room:
                    ### finding windows in particolar room
                    cols_windows=list(set([a for a in self._dfglob.loc[idx[:],idx[building,zone,room,:]].columns.get_level_values(3).values]))
                    status_windows = []
                    dict_transcarts_2_transcodes, trans_combs, dict_trans_combs_language_to_code=self.gen_trans_combs(cols_windows, identical_windows)
                    for row in self._dfglob.loc[idx[:],idx[building,zone,room,cols_windows]].values:
                        status_windows.append([np.int(value) for value in row])
                    status_windows=np.array(status_windows)
                    change_of_state=[]
                    WPcode='WP1'+str(['+'+str(sw+1) for sw in range(len(status_windows)-1)])
                    for index, element in enumerate(status_windows):
                        if index==0:
                            change_of_state.append(dict_transcarts_2_transcodes[tuple(map(tuple,[element, element]))])
                        else:
                            change_of_state.append(dict_transcarts_2_transcodes[tuple(map(tuple,[status_windows[index-1], element]))])
                    df_status_change[building,zone,room,'window combination']=change_of_state
                    df_status_change.columns=MultiIndex.from_tuples(df_status_change.columns.values)

                    ### generate a transition combination matrix
                    for trans_comb in trans_combs:
                        code_value=dict_trans_combs_language_to_code[str(trans_comb)]
                        ### assign to each copmbination column the value of the combination code
                        self.df_transiction_matrix['TPM',str(trans_comb[0]),str(trans_comb[1]),building,zone,room#,WPcode
                                              ]=[code_value for i in range(len(self._dfglob.index))]
                        ###comparing that value with the combination value in column "window combination"
                        self.df_transiction_matrix['TPM',str(trans_comb[0]),str(trans_comb[1]), building,zone,room#,WPcode
                                              ]=np.where(self.df_transiction_matrix['TPM',str(trans_comb[0]),str(trans_comb[1]),building,zone,room#,WPcode
                                              ]==df_status_change[building,zone,room,'window combination'],1,0)

        self.df_transiction_matrix.columns=MultiIndex.from_tuples(self.df_transiction_matrix.columns.values)
        self.df_transiction_matrix.columns.names=['Datatype','TPM_start','TPM_stop', 'Field', 'Zone', 'Room']

    def genWPinterlevels(self):
        '''
        Method to generate averages of WP over room (related to WP1 and WP2),
        over an apartment (WP1, WP2, WP), over an Entrance and a building
        This method add new columns at the main DF "self._dfglob"
        WPS indicates only one window open, WPD both windows open
        This function is designed for the field test data from Germany (see WinProGen publications)
        '''
        ### getting columns names
        columns=self._dfglob.columns.values
        ### checking the length of the list, to know which level contains what
        levelOfMU=len(self._dfglob.columns[0])
        #print np.array(columns.tolist()).T
        
        ### chosing allowed names for column names, where WPs are expected
        all1=["B2E1","B2E2","B2E3","B3E1","B3E2","B3E3"]
        all2=["A01","A02","A03","A04","A05","A06","A07","A08","A09","A10"]
        all3=["Room_Children","Room_Kitchen","Room_Sleeping","Room_Living","Room_Bath"]
        all4=["WP1","WP2"]
        ### taking the interception between available columns and allowed columns
        level1=np.intersect1d(np.array(columns.tolist()).T[levelOfMU-4],all1)
        level2=np.intersect1d(np.array(columns.tolist()).T[levelOfMU-3],all2)
        level3=np.intersect1d(np.array(columns.tolist()).T[levelOfMU-2],all3)
        level4=np.intersect1d(np.array(columns.tolist()).T[levelOfMU-1],all4)
        
        print ("LEVELS choosen:", level1, level2, level3,level4)

#         if len(level1)>1: print "Building analysis", self._dfglob.iloc[:, df.columns.get_level_values(3)=='WP1'].columns.values
        for building in level1:
            # go through the buildings and get a temp DF for each
            temp=self._dfglob.iloc[:, self._dfglob.columns.get_level_values(0)==building]
            # temp1 is a DF with only WP1, temp2 with only WP2, temp3 both of them
            temp1=temp.iloc[:, temp.columns.get_level_values(levelOfMU-1)=="WP1"]
            temp2=temp.iloc[:, temp.columns.get_level_values(levelOfMU-1)=="WP2"]
            temp3=pd.concat([temp1,temp2], axis=1)
            # in the next 3 lines the mean values (per timestep, horizontal mean, axis=1) is executed  and added to the original DF
            self._dfglob[building, "-","-","WP1"]=temp1.mean(axis=1)
            self._dfglob[building, "-","-","WP2"]=temp2.mean(axis=1)
            self._dfglob[building, "-","-","WP"]=temp3.mean(axis=1)

            # go through the apartments
            for apartment in level2:
                # temp, temp1, temp2, temp3 are now only related to the apartment chosen
                temp=self._dfglob.iloc[:, self._dfglob.columns.get_level_values(0)==building]
                temp=temp.iloc[:, temp.columns.get_level_values(levelOfMU-3)==apartment]
                temp1=temp.iloc[:, temp.columns.get_level_values(levelOfMU-1)=="WP1"]
                temp2=temp.iloc[:, temp.columns.get_level_values(levelOfMU-1)=="WP2"]
                temp3=pd.concat([temp1,temp2], axis=1)
                self._dfglob[building, apartment,"-","WP1"]=temp1.mean(axis=1)
                self._dfglob[building, apartment,"-","WP2"]=temp2.mean(axis=1)
                self._dfglob[building, apartment,"-","WP"]=temp3.mean(axis=1)
                
                for room in level3:
                    # the same, but room-wise
                    if room == "Room_Children" or room == "Room_Sleeping":
                        temp=self._dfglob.iloc[:, self._dfglob.columns.get_level_values(0)==building]
                        temp=temp.iloc[:, temp.columns.get_level_values(levelOfMU-3)==apartment]
                        temp=temp.iloc[:, temp.columns.get_level_values(levelOfMU-2)==room]
                        temp1=temp.iloc[:, temp.columns.get_level_values(levelOfMU-1)=="WP1"]
                        temp2=temp.iloc[:, temp.columns.get_level_values(levelOfMU-1)=="WP2"]
                        temp3=pd.concat([temp1,temp2], axis=1)
                        self._dfglob[building, apartment,room,"WP"]=temp3.mean(axis=1)
                        self._dfglob[building, apartment,room,"WP1+2"]=temp3.sum(axis=1)


        for building in level1:
            for room in level3:
                # generate an average WP for each room with double window
                temp=self._dfglob.iloc[:, self._dfglob.columns.get_level_values(levelOfMU-2)==room]
                temp1=temp.iloc[:, temp.columns.get_level_values(levelOfMU-1)=="WP1"]
                if room == "Room_Children" or room == "Room_Sleeping":
                    temp2=temp.iloc[:, temp.columns.get_level_values(levelOfMU-1)=="WP2"]
                    temp3=pd.concat([temp1,temp2], axis=1)
                    self._dfglob[building, "-",room,"WP2"]=temp2.mean(axis=1)
                    self._dfglob[building, "-",room,"WP"]=temp3.mean(axis=1)

                self._dfglob[building, "-",room,"WP1"]=temp1.mean(axis=1)

    def genWPinterlevels_general4DAATG(self):
        '''
        Method to generate averages of WP over room (related to WPs),
        over an apartment (WP1, WP2, WPi), over an Entrance and a building
        in respect to the daily average outdoor temperature
        This method add new columns at the main DF "self._dfglob"
        This function is designed for the field test data from Germany (see WinProGen publications)
        '''
        ### getting columns names
        columns=self._dfglob.columns.values
        print(columns)
        ### checking the length of the list, to know which level contains what
        levelOfMU=len(self._dfglob.columns[0])

        ### chosing allowed names for column names, where WPs are expected
        all1=list(set([a for a in self._dfglob.columns.levels[levelOfMU-4].values if a!="Weather"]))
        all2=list(set([a for a in self._dfglob.columns.levels[levelOfMU-3].values if a!="-"]))
        all3=list(set([a for a in self._dfglob.columns.levels[levelOfMU-2].values if a!="-"]))
        all4=list(set([a for a in self._dfglob.columns.levels[levelOfMU-1].values if a!="AT"]))

        ### taking the interception between available columns and allowed columns
        level1=np.intersect1d(np.array(columns.tolist()).T[levelOfMU-4],all1)
        level2=np.intersect1d(np.array(columns.tolist()).T[levelOfMU-3],all2)
        level3=np.intersect1d(np.array(columns.tolist()).T[levelOfMU-2],all3)
        level4=np.intersect1d(np.array(columns.tolist()).T[levelOfMU-1],all4)

        level1=[a for a in level1 if a!='']
        level2=[a for a in level2 if a!='']
        level3=[a for a in level3 if a!='']
        level4=[a for a in level4 if a!='']

        print ("LEVELS choosen:", level1, level2, level3,level4)

#         if len(level1)>1: print "Building analysis", self._dfglob.iloc[:, df.columns.get_level_values(3)=='WP1'].columns.values
        for building in level1:
            # go through the buildings and get a temp DF for each
            temp=self._dfglob.iloc[:, self._dfglob.columns.get_level_values(0)==building]

            for WP in all4:
            # temp1 is a DF with only WP1, temp2 with only WP2, temp3 both of them
                self._dfglob[building, "-","-",WP]=\
                    temp.iloc[:, temp.columns.get_level_values(levelOfMU-1)==WP].mean(axis=1)
                self._dfglob[building, "-","-",'WP']=\
                    temp.iloc[:, temp.columns.get_level_values(levelOfMU-1)!=WP].mean(axis=1)

            # go through the apartments
            for apartment in level2:
                temp=self._dfglob.iloc[:, self._dfglob.columns.get_level_values(0)==building]
                temp=temp.iloc[:, temp.columns.get_level_values(levelOfMU-3)==apartment]

                for WP in all4:
                    self._dfglob[building, apartment,"-",WP]=\
                        temp.iloc[:, temp.columns.get_level_values(levelOfMU-1)==WP].mean(axis=1)
                    self._dfglob[building, apartment,"-",'WP']=\
                        temp.iloc[:, temp.columns.get_level_values(levelOfMU-1)!=WP].mean(axis=1)

                for room in level3:
                    # the same, but room-wise
                        temp=self._dfglob.iloc[:, self._dfglob.columns.get_level_values(0)==building]
                        temp=temp.iloc[:, temp.columns.get_level_values(levelOfMU-3)==apartment]
                        temp=temp.iloc[:, temp.columns.get_level_values(levelOfMU-2)==room]

                        for WP in all4:
                            if len(temp.columns.get_level_values(levelOfMU-1))>1:
                                self._dfglob[building, apartment,room,'WP']=\
                                    temp.iloc[:, temp.columns.get_level_values(levelOfMU-1)!=WP].mean(axis=1)

        for building in level1:
            for room in level3:
                # generate an average WP for each room with double window
                temp=self._dfglob.iloc[:, self._dfglob.columns.get_level_values(levelOfMU-2)==room]
                temp1=temp.iloc[:, temp.columns.get_level_values(levelOfMU-1)=="WP1"]
                self._dfglob[building, "-",room,WP]=\
                    temp.iloc[:, temp.columns.get_level_values(levelOfMU-1)==WP].mean(axis=1)
                if len(temp.columns.get_level_values(levelOfMU-1))>1:
                    self._dfglob[building, "-", room,'WP']=\
                    temp.iloc[:, temp.columns.get_level_values(levelOfMU-1)!=WP].mean(axis=1)
        
    def elabTPM(self):
        '''
        this method
        :param
        :return:
        '''
        
        print ("START Elaborate TPM single Window")
        levelOfTPMXX=self.Diurnals.columns[0].index("MD")+1 # note that the level of measured data is the same as TPM
        newTPM=self.Diurnals.iloc[:, self.Diurnals.columns.get_level_values(levelOfTPMXX-1)=="TPM"].copy()        

        newTPM=newTPM.sort_index(axis=1)
        newTPM=newTPM.loc[idx[:],idx[:,:,:,:,['B2E1','B2E2','B2E3','B3E1','B3E2','B3E3'],['A01','A02','A03','A04','A05','A06','A07','A08','A09','A10'],:,:]]
        
        TPM00=newTPM.iloc[:, newTPM.columns.get_level_values(levelOfTPMXX)=="TPM_00"]
        TPM01=newTPM.iloc[:, newTPM.columns.get_level_values(levelOfTPMXX)=="TPM_01"]
        TPM10=newTPM.iloc[:, newTPM.columns.get_level_values(levelOfTPMXX)=="TPM_10"]
        TPM11=newTPM.iloc[:, newTPM.columns.get_level_values(levelOfTPMXX)=="TPM_11"]

        sumTPM00_TPM01=TPM00.values+TPM01.values
        sumTPM10_TPM11=TPM10.values+TPM11.values
                
        TPM00R=TPM00/sumTPM00_TPM01
        TPM01R=TPM01/sumTPM00_TPM01
        TPM10R=TPM10/sumTPM10_TPM11
        TPM11R=TPM11/sumTPM10_TPM11
        newTPM=pd.concat([TPM00R,TPM01R,TPM10R,TPM11R],axis=1).sort_index(axis=1)
        
        ls=np.array(list(newTPM.columns)).T
        ls[levelOfTPMXX-1]=np.char.add(ls[levelOfTPMXX-1], "_R")
        ls[levelOfTPMXX]=np.char.add(ls[levelOfTPMXX], "_R")
#         newTPM.describe().to_csv("D:/scriptTest/prima.csv",";")
#         newTPM.describe().to_csv("D:/scriptTest/dopo.csv",";")
        newTPM.columns=MultiIndex.from_arrays(ls)

        #generate 2x2 start values DataFrame
        startTPM00=TPM00.iloc[0,:].copy()
        startTPM01=TPM01.iloc[0,:].copy()
        startTPM10=TPM10.iloc[0,:].copy()
        startTPM11=TPM11.iloc[0,:].copy()
        
        startIs0=startTPM00.values+startTPM01.values
        startIs1=startTPM10.values+startTPM11.values

        startIs0R=pd.DataFrame(startIs0/(startIs0+startIs1)).transpose()#, columns=TPM00.columns)
        startIs1R=pd.DataFrame(startIs1/(startIs0+startIs1)).transpose()#, columns=TPM11.columns)
        startIs0R.columns=TPM00.columns
        startIs1R.columns=TPM11.columns
        start2x2=pd.concat([startIs0R,startIs1R], axis=1)
        start2x2copy=start2x2.copy()
        
        self.start2x2=pd.concat([start2x2copy.iloc[:,start2x2copy.columns.get_level_values(levelOfTPMXX+3)=="Room_Bath"],start2x2copy.iloc[:,start2x2copy.columns.get_level_values(levelOfTPMXX+3)=="Room_Kitchen"],start2x2copy.iloc[:,start2x2copy.columns.get_level_values(levelOfTPMXX+3)=="Room_Living"]],axis=1).sort_index(axis=1)

        # starts operation for 3x3 TPM
            
        levelOfTPMXX=self.Diurnals.columns[0].index("MD")+1 # note that the level of measured data is the same as TPM
        newTPM2=self.Diurnals.iloc[:, self.Diurnals.columns.get_level_values(levelOfTPMXX-1)=="TPMd"].copy()        
        
        TPM00=newTPM2.iloc[:, newTPM2.columns.get_level_values(levelOfTPMXX)=="TPMd_00"]
        TPM01=newTPM2.iloc[:, newTPM2.columns.get_level_values(levelOfTPMXX)=="TPMd_01"]
        TPM02=newTPM2.iloc[:, newTPM2.columns.get_level_values(levelOfTPMXX)=="TPMd_02"]
        
        TPM10=newTPM2.iloc[:, newTPM2.columns.get_level_values(levelOfTPMXX)=="TPMd_10"]
        TPM11=newTPM2.iloc[:, newTPM2.columns.get_level_values(levelOfTPMXX)=="TPMd_11"]
        TPM12=newTPM2.iloc[:, newTPM2.columns.get_level_values(levelOfTPMXX)=="TPMd_12"]
        
        TPM20=newTPM2.iloc[:, newTPM2.columns.get_level_values(levelOfTPMXX)=="TPMd_20"]
        TPM21=newTPM2.iloc[:, newTPM2.columns.get_level_values(levelOfTPMXX)=="TPMd_21"]
        TPM22=newTPM2.iloc[:, newTPM2.columns.get_level_values(levelOfTPMXX)=="TPMd_22"]

        sumTPM0=TPM00.values+TPM01.values+TPM02.values
        sumTPM1=TPM10.values+TPM11.values+TPM12.values
        sumTPM2=TPM20.values+TPM21.values+TPM22.values
                
        TPM00R=TPM00/sumTPM0
        TPM01R=TPM01/sumTPM0
        TPM02R=TPM02/sumTPM0
        TPM10R=TPM10/sumTPM1
        TPM11R=TPM11/sumTPM1
        TPM12R=TPM12/sumTPM1        
        TPM20R=TPM20/sumTPM2
        TPM21R=TPM21/sumTPM2
        TPM22R=TPM22/sumTPM2
        
        newTPM2=pd.concat([TPM00R,TPM01R,TPM02R,TPM10R,TPM11R,TPM12R,TPM20R,TPM21R,TPM22R],axis=1)
        
        ls=np.array(list(newTPM2.columns)).T
        ls[levelOfTPMXX-1]=np.char.add(ls[levelOfTPMXX-1], "_R")
        ls[levelOfTPMXX]=np.char.add(ls[levelOfTPMXX], "_R")
        
        newTPM2.columns=MultiIndex.from_arrays(ls)
        
        #generate 3x3 start values DataFrame
                
        startTPM00=TPM00.iloc[0,:].copy()
        startTPM01=TPM01.iloc[0,:].copy()
        startTPM02=TPM02.iloc[0,:].copy()
        startTPM10=TPM10.iloc[0,:].copy()
        startTPM11=TPM11.iloc[0,:].copy()
        startTPM12=TPM12.iloc[0,:].copy()
        startTPM20=TPM20.iloc[0,:].copy()
        startTPM21=TPM21.iloc[0,:].copy()
        startTPM22=TPM22.iloc[0,:].copy()
        
        startIs0=startTPM00.values+startTPM01.values+startTPM02.values
        startIs1=startTPM10.values+startTPM11.values+startTPM12.values
        startIs2=startTPM20.values+startTPM21.values+startTPM22.values
        
        startIs0R=pd.DataFrame(startIs0/(startIs0+startIs1+startIs2)).transpose()#, columns=TPM00.columns)
        startIs1R=pd.DataFrame(startIs1/(startIs0+startIs1+startIs2)).transpose()#, columns=TPM11.columns)
        startIs2R=pd.DataFrame(startIs2/(startIs0+startIs1+startIs2)).transpose()#, columns=TPM11.columns)
        
        startIs0R.columns=TPM00.columns
        startIs1R.columns=TPM11.columns
        startIs2R.columns=TPM22.columns
        start3x3=pd.concat([startIs0R,startIs1R,startIs2R], axis=1)
        self.start3x3=start3x3
        

        self.TPM2x2=newTPM.loc[idx[:],idx[:,:,:,:,:,:,["Room_Bath","Room_Kitchen","Room_Living"],:]]
        self.TPM3x3=newTPM2
        self.TPM=pd.concat([newTPM,newTPM2],axis=1)
        self.Diurnals=pd.concat([self.Diurnals,self.TPM],axis=1) 

        
    def genGlobalTPMBasic(self,limit2=["WP1","WP2","WP"],level=3,inglobeIn_dfglob=True, saveTPMs2csv=False):    ###### not used !!!
        '''
        OLD FUNCTION NOT USED !!
        Method to generate a global TPM of one Windows' positions
        '''
        # fill NaN in dfGlob
        self._dfglob.fillna(method="ffill", limit=10, inplace=True)
        # take only relevant part of the DataFrame
        for index, leaf in enumerate(limit2):
            if index==0: temp=self._dfglob.iloc[:, self._dfglob.columns.get_level_values(level)==leaf]
            else: temp=pd.concat([temp,self._dfglob.iloc[:, self._dfglob.columns.get_level_values(level)==leaf]], axis=1)
        
        # generate an identical DF rolled backwards of 1 value, to check the situation one timestep later 
        tempRolled=DataFrame(np.roll(temp.values.T,-1, axis=1).T,index=temp.index,columns=temp.columns)
        tempRolled.iloc[[-1],:]=temp.iloc[[-1],:]
        #generate the four TPMs with top level "TPM", second level "TPM_XX" anmd the standard 4 levels of the input matrix 
        TPM00=self.addLevel(DataFrame(np.where((temp+tempRolled)==0,1,0),index=temp.index,columns=temp.columns).sort_index(axis=1), ["TPM","TPM_00"])      
        TPM01=self.addLevel(DataFrame(np.where((temp<tempRolled)==True,1,0),index=temp.index,columns=temp.columns).sort_index(axis=1), ["TPM","TPM_01"])
        TPM10=self.addLevel(DataFrame(np.where((temp>tempRolled)==True,1,0),index=temp.index,columns=temp.columns).sort_index(axis=1), ["TPM","TPM_10"])
        TPM11=self.addLevel(DataFrame(temp*tempRolled,index=temp.index,columns=temp.columns).sort_index(axis=1), ["TPM","TPM_11"])
        TPM=pd.concat([TPM00,TPM01,TPM10,TPM11],axis=1, join="outer")
        if saveTPMs2csv==True:
            TPM00.to_csv(folder+'TPM00.csv',";")
            TPM01.to_csv(folder+'TPM01.csv',";")
            TPM10.to_csv(folder+'TPM10.csv',";")
            TPM11.to_csv(folder+'TPM11.csv',";")
        
        if inglobeIn_dfglob==True: 
            self._dfglob=self.addLevel(self._dfglob,["MD", "-"])
            self._dfglob=pd.concat([self._dfglob,TPM],axis=1, join="outer")
        else:
            self.TPMdf=TPM

    def aggregate_TPM(self, TPM_df, starts_df):

        '''
        method used to aggregate the probabilities depending on ONE state into one array
        and to further cumulate the probability, as needed by the IFM
        :return: new TPM
        '''

        c_T_ranges=list(set([a for a in TPM_df.columns.get_level_values(0).values]))
        c_day_type=list(set([a for a in TPM_df.columns.get_level_values(1).values]))

        # c_next_status=list(set([a for a in TPM_df.columns.get_level_values(3).values]))
        c_zone=list(set([a for a in TPM_df.columns.get_level_values(5).values]))
        c_room=list(set([a for a in TPM_df.columns.get_level_values(6).values]))
        c_field=list(set([a for a in TPM_df.columns.get_level_values(4).values]))

        self.agg_TPM=pd.DataFrame(index=TPM_df.index)
        self.agg_starts=pd.DataFrame(index=starts_df.index)

        for T_range in c_T_ranges:
            for day_type in c_day_type:
                for field in c_field:
                    for zone in c_zone:
                        for room in c_room:
                                c_actual_status=list(set([a for a in TPM_df.loc[idx[:],idx[T_range,day_type,:,
                                                "['All closed']",field,zone,room,'TPM']].columns.get_level_values(2).values]))
                                for actual_status in c_actual_status:

                                    col_next_status=str([a for a in TPM_df.loc[idx[:],
                                            idx[T_range,day_type,actual_status,
                                            :,field,zone,room,'TPM']].columns.get_level_values(3).values])

                                    data_array=(TPM_df.loc[idx[:],
                                                     idx[T_range, day_type, actual_status,
                                                     :, field, zone, room, 'TPM']].cumsum(axis=1).apply(tuple,axis=1))
                                    self.agg_TPM[T_range,day_type,actual_status,col_next_status,field,zone,room,'TPM']=data_array
        self.agg_TPM.columns=MultiIndex.from_tuples(self.agg_TPM.columns)
        self.agg_TPM.sort_index(axis=1,inplace=True)

        starts_df=self.delColLev(starts_df, [3])
        c_T_ranges=list(set([a for a in starts_df.columns.get_level_values(0).values]))
        c_day_type=list(set([a for a in starts_df.columns.get_level_values(1).values]))
        c_actual_status=list(set([a for a in starts_df.columns.get_level_values(2).values]))
        c_field=list(set([a for a in starts_df.columns.get_level_values(3).values]))
        c_zone=list(set([a for a in starts_df.columns.get_level_values(4).values]))
        c_room=list(set([a for a in starts_df.columns.get_level_values(5).values]))

        for T_range in c_T_ranges:
            for day_type in c_day_type:
                        for field in c_field:
                            for zone in c_zone:
                                for room in c_room:

                                    actual_status=str([a for a in starts_df.loc[idx[:],
                                            idx[T_range,day_type,:,
                                            field,zone,room,'TPM']].columns.get_level_values(2).values])


                                    '''data_array=zip(starts_df.loc[idx[:],
                                            idx[T_range,day_type,:,
                                            field,zone,room,'TPM']].values.cumsum(axis=1))[0]
                                    '''
                                    data_array=(starts_df.loc[idx[:],
                                            idx[T_range,day_type,:,
                                            field,zone,room,'TPM']].cumsum(axis=1).apply(tuple,axis=1))
                                    self.agg_starts[T_range,day_type,actual_status,'-',field,zone,room,'TPM']=data_array


        self.agg_starts.columns=MultiIndex.from_tuples(self.agg_starts.columns)
        self.agg_starts.sort_index(axis=1,inplace=True)


    def split_TPMs_starts(self):
        '''
        function to split TPMs into 2x2 3x3 TPM to use in fast simulation engine (shortly "TURBO")
        from old method PhD Thesis Cali
        :return: new TPMs and starts
        '''

        self.TPM3x3 = pd.DataFrame()
        self.TPM2x2 = pd.DataFrame()
        self.start2x2 = pd.DataFrame()
        self.start3x3 = pd.DataFrame()

        L0 = [a for a in self.TPM.columns.get_level_values(0).values]
        L1 = [a for a in self.TPM.columns.get_level_values(1).values]
        start_positions = [a for a in self.TPM.columns.get_level_values(2).values]
        end_positions = [a for a in self.TPM.columns.get_level_values(3).values]
        L4 = [a for a in self.TPM.columns.get_level_values(4).values]
        L5 = [a for a in self.TPM.columns.get_level_values(5).values]
        L6 = [a for a in self.TPM.columns.get_level_values(6).values]
        L7 = [a for a in self.TPM.columns.get_level_values(7).values]

        ren_dict={"['All closed']":'0',"['WP1']":'1',"['WP2']":'1',"['WP1', 'WP2']":'2'}

        dw_rooms = list(set([a for a in self.TPM.loc[idx[:],idx[:,:,"['WP1', 'WP2']",:,:,:,:,:]].columns.get_level_values(6).values]))

        for index,s_p in enumerate(start_positions):
            if L6[index] in dw_rooms:
                code='TPMd_'+ren_dict[s_p]+ren_dict[end_positions[index]]+'_R'
                self.TPM3x3[L0[index],L1[index],'TPMd_R', code,L4[index],L5[index],L6[index],L7[index]]=self.TPM[L0[index],L1[index],s_p,end_positions[index],L4[index],L5[index],L6[index],L7[index]]
            else:
                code='TPM_'+ren_dict[s_p]+ren_dict[end_positions[index]]+'_R'
                self.TPM2x2[L0[index],L1[index],'TPMd_R', code,L4[index],L5[index],L6[index],L7[index]]=self.TPM[L0[index],L1[index],s_p,end_positions[index],L4[index],L5[index],L6[index],L7[index]]

        L0 = [a for a in self.start.columns.get_level_values(0).values]
        L1 = [a for a in self.start.columns.get_level_values(1).values]
        is_positions = [a for a in self.start.columns.get_level_values(2).values]
        L3 = [a for a in self.start.columns.get_level_values(3).values]
        L4 = [a for a in self.start.columns.get_level_values(4).values]
        L5 = [a for a in self.start.columns.get_level_values(5).values]
        L6 = [a for a in self.start.columns.get_level_values(6).values]
        L7 = [a for a in self.start.columns.get_level_values(7).values]

        dw_rooms = list(set([a for a in self.start.loc[idx[:],idx[:,:,"['WP1', 'WP2']",:,:,:,:,:]].columns.get_level_values(6).values]))

        for index,i_p in enumerate(is_positions):
            code='TPMd_'+ren_dict[i_p]+ren_dict[i_p]
            if L6[index] in dw_rooms:
                code='TPMd_'+ren_dict[i_p]+ren_dict[i_p]
                self.start3x3[L0[index],L1[index],'TPM', code,L4[index],L5[index],L6[index],L7[index]]=self.start[L0[index],L1[index],i_p,L3[index],L4[index],L5[index],L6[index],L7[index]]
            else:
                code='TPM_'+ren_dict[i_p]+ren_dict[i_p]
                self.start2x2[L0[index],L1[index],'TPM', code,L4[index],L5[index],L6[index],L7[index]]=self.start[L0[index],L1[index],i_p,L3[index],L4[index],L5[index],L6[index],L7[index]]

        self.start2x2.columns=MultiIndex.from_tuples(self.start2x2.columns)
        self.start3x3.columns=MultiIndex.from_tuples(self.start3x3.columns)
        self.TPM3x3.columns=MultiIndex.from_tuples(self.TPM3x3.columns)
        self.TPM2x2.columns=MultiIndex.from_tuples(self.TPM2x2.columns)


    def compute_trans_probs(self):
        '''
        Method to compute each probability of a change,
        normalizing this probability in respect to the actual change
        New method, realised for a variable no. of windows
        This method is slower the the TURBO mode, but is flexible since can have windows with variable number of panels
        '''
        ### dropping not needed columns
        self.Diurnals.drop('ATR', axis=1, level=0)

        ### getting all columns except Ambient Temperature values
        c_T_ranges=list(set([a for a in self.Diurnals.columns.get_level_values(0).values]))
        c_day_type=list(set([a for a in self.Diurnals.columns.get_level_values(1).values]))

        ### dropping not needed columns for M2
        if 'Week' in c_day_type:
            self.Diurnals.drop('Standard Diurnal', axis=1, level=1)
            c_day_type=list(set([a for a in self.Diurnals.columns.get_level_values(1).values]))


        c_next_status=list(set([a for a in self.Diurnals.columns.get_level_values(3).values]))
        c_field=list(set([a for a in self.Diurnals.columns.get_level_values(4).values]))
        c_zone=list(set([a for a in self.Diurnals.columns.get_level_values(5).values]))
        c_room=list(set([a for a in self.Diurnals.columns.get_level_values(6).values]))

        match_timestamp = "00:00:00"
        self.starts_probs=pd.DataFrame()

        for T_range in c_T_ranges:
            for day_type in c_day_type:
                c_field=list(set([a for a in self.Diurnals.loc[idx[:],idx[T_range,day_type,:,
                                                        :,:,:,:,'TPM']].columns.get_level_values(4).values]))
                for field in c_field:
                    c_zone=list(set([a for a in self.Diurnals.loc[idx[:],idx[T_range,day_type,:,
                                    :,field,:,:,'TPM']].columns.get_level_values(5).values]))
                    for zone in c_zone:
                        c_room=list(set([a for a in self.Diurnals.loc[idx[:],idx[T_range,day_type,:,
                                    :,field,zone,:,'TPM']].columns.get_level_values(6).values]))
                        for room in c_room:
                            c_actual_status=list(set([a for a in self.Diurnals.loc[idx[:],idx[T_range,day_type,:,
                                            :,field,zone,room,'TPM']].columns.get_level_values(2).values]))
                            for actual_status in c_actual_status:
                                c_next_status=list(set([a for a in self.Diurnals.loc[idx[:],idx[T_range,day_type,actual_status,
                                                        :,field,zone,room,'TPM']].columns.get_level_values(3).values]))
                                for next_status in c_next_status:

                                    df=self.Diurnals.loc[idx[:],
                                            idx[T_range,day_type,actual_status,
                                            :,field,zone,room,'TPM']]

                                    self.starts_probs[T_range,day_type,actual_status,'-',field,zone,room,'TPM']=(df.loc[df.index.strftime("%H:%M:%S") ==
                                                                               match_timestamp]).sum(axis=1)

        self.starts_probs.columns=MultiIndex.from_tuples(self.starts_probs.columns)
        self.starts_probs.sort_index(axis=1,inplace=True)


        for T_range in c_T_ranges:
            for day_type in c_day_type:
                c_field=list(set([a for a in self.Diurnals.loc[idx[:],idx[T_range,day_type,:,
                                                        :,:,:,:,'TPM']].columns.get_level_values(4).values]))
                for field in c_field:
                    c_zone=list(set([a for a in self.Diurnals.loc[idx[:],idx[T_range,day_type,:,
                                    :,field,:,:,'TPM']].columns.get_level_values(5).values]))
                    for zone in c_zone:
                        c_room=list(set([a for a in self.Diurnals.loc[idx[:],idx[T_range,day_type,:,
                                    :,field,zone,:,'TPM']].columns.get_level_values(6).values]))
                        for room in c_room:
                            c_actual_status=list(set([a for a in self.Diurnals.loc[idx[:],idx[T_range,day_type,:,
                                            :,field,zone,room,'TPM']].columns.get_level_values(2).values]))
                            for actual_status in c_actual_status:
                                c_next_status=list(set([a for a in self.Diurnals.loc[idx[:],idx[T_range,day_type,actual_status,
                                                        :,field,zone,room,'TPM']].columns.get_level_values(3).values]))
                                sum_of_row=self.Diurnals.loc[idx[:],idx[T_range,day_type,actual_status,:,field,zone,room,'TPM']].sum(axis=1)
                                row=self.Diurnals.loc[idx[:],idx[T_range,day_type,actual_status,:,field,zone,room,'TPM']]
                                for next_status in c_next_status:


                                    self.Diurnals.loc[idx[:],
                                    idx[T_range,day_type,actual_status,
                                    next_status,field,zone,room,'TPM']] = self.Diurnals.loc[idx[:],
                                                                        idx[T_range,day_type,actual_status,
                                    next_status,field,zone,room,'TPM']] / sum_of_row

    def generate_general_state_changes_mx(self,level=3,inglobeIn_dfglob=True, saveTPMs2csv=False, identical_windows=[]):
        '''
        Method to generate a general TPM of the Windows' positions
        Done for a variable no. of windows: open or closed.
        After calling it, you should run genDiurnals to condensate the TPM into one single day
        since this method actually do not compute probability,
        just checks state change of windows position in each timestep
        '''

        ### getting all columns except Ambient Temperature values
        self.cols_building=list(set([a for a in self._dfglob.columns.levels[0].values if a!="Weather"]))
        self.cols_zone=list(set([a for a in self._dfglob.columns.levels[1].values if a!="-"]))
        self.cols_room=list(set([a for a in self._dfglob.columns.levels[2].values if a!="-"]))
        self.cols_windows=list(set([a for a in self._dfglob.columns.levels[3].values if a!="AT"]))
        ### Cleaning nan and sort indexes
        self._dfglob=self._dfglob.fillna(method='pad', limit=3)
        self._dfglob=self._dfglob.dropna()
        self._dfglob.reindex_axis(sorted(self._dfglob.columns), axis=1)
        self._dfglob.sort_index(axis=1,inplace=True)

        ### making all values to integer except for the AT
        for col in self.cols_windows:
            self._dfglob.loc[idx[:],idx[:,:,:,col]]=self._dfglob.loc[idx[:],idx[:,:,:,col]].astype(int)

        self.generate_df_trans(identical_windows)
        self.df_transiction_matrix.columns=MultiIndex.from_tuples(self.df_transiction_matrix.columns.values)

    def genGlobalTPM(self,level=3,inglobeIn_dfglob=True, saveTPMs2csv=False):
        '''
        Method to generate a global TPM of the Windows' positions
        Done for one and two states of windows: One open or closed / one or two open or closed.
        After calling it, you should run genDiurnals to condensate the TPM into one single day
        since this method actually do not compute probability, just checks state change of windows position in each timestep
        '''
        # fill NaN with forward number in dfGlob: it affects directly _dfglob!!!
        self._dfglob.fillna(method="ffill", limit=10, inplace=True)
        # take only relevant part of the DataFrame and split it in mono and double windows
        temp=self._dfglob.iloc[:, self._dfglob.columns.get_level_values(level)=="WP1"]
        temp12=self._dfglob.iloc[:, self._dfglob.columns.get_level_values(level)=="WP1+2"]
        # generate an identical DF rolled backwards of 1 value, to check the situation one timestep later 
        tempRolled=DataFrame(np.roll(temp.values.T,-1, axis=1).T,index=temp.index,columns=temp.columns)
        tempRolled.iloc[[-1],:]=temp.iloc[[-1],:]        
        # generate an identical DF rolled backwards of 1 value, to check the situation one timestep later 
        tempRolled12=DataFrame(np.roll(temp12.values.T,-1, axis=1).T,index=temp12.index,columns=temp12.columns)
        tempRolled12.iloc[[-1],:]=temp12.iloc[[-1],:]
        #generate the four TPMs with columns top level "TPM", second level "TPM_XX" and the standard 4 levels of the input matrix 
        TPM00=self.addLevel(DataFrame(np.where((temp+tempRolled)==0,1,0),index=temp.index,columns=temp.columns).sort_index(axis=1), ["TPM","TPM_00"])      
        TPM01=self.addLevel(DataFrame(np.where((temp<tempRolled)==True,1,0),index=temp.index,columns=temp.columns).sort_index(axis=1), ["TPM","TPM_01"])
        TPM10=self.addLevel(DataFrame(np.where((temp>tempRolled)==True,1,0),index=temp.index,columns=temp.columns).sort_index(axis=1), ["TPM","TPM_10"])
        TPM11=self.addLevel(DataFrame(temp*tempRolled,index=temp.index,columns=temp.columns).sort_index(axis=1), ["TPM","TPM_11"])
        #generate the 9 TPMs with columns top level "TPM", second level "TPM_XX" and the standard 4 levels of the input matrix 
        TPM00d=self.addLevel(DataFrame(np.where((temp12==0) & (tempRolled12==0),1,0),index=temp12.index,columns=temp12.columns).sort_index(axis=1), ["TPMd","TPMd_00"])
        TPM01d=self.addLevel(DataFrame(np.where((temp12==0) & (tempRolled12==1),1,0),index=temp12.index,columns=temp12.columns).sort_index(axis=1), ["TPMd","TPMd_01"])
        TPM02d=self.addLevel(DataFrame(np.where((temp12==0) & (tempRolled12==2),1,0),index=temp12.index,columns=temp12.columns).sort_index(axis=1), ["TPMd","TPMd_02"])
        TPM10d=self.addLevel(DataFrame(np.where((temp12==1) & (tempRolled12==0),1,0),index=temp12.index,columns=temp12.columns).sort_index(axis=1), ["TPMd","TPMd_10"])
        TPM11d=self.addLevel(DataFrame(np.where((temp12==1) & (tempRolled12==1),1,0),index=temp12.index,columns=temp12.columns).sort_index(axis=1), ["TPMd","TPMd_11"])
        TPM12d=self.addLevel(DataFrame(np.where((temp12==1) & (tempRolled12==2),1,0),index=temp12.index,columns=temp12.columns).sort_index(axis=1), ["TPMd","TPMd_12"])
        TPM20d=self.addLevel(DataFrame(np.where((temp12==2) & (tempRolled12==0),1,0),index=temp12.index,columns=temp12.columns).sort_index(axis=1), ["TPMd","TPMd_20"])
        TPM21d=self.addLevel(DataFrame(np.where((temp12==2) & (tempRolled12==1),1,0),index=temp12.index,columns=temp12.columns).sort_index(axis=1), ["TPMd","TPMd_21"])
        TPM22d=self.addLevel(DataFrame(np.where((temp12==2) & (tempRolled12==2),1,0),index=temp12.index,columns=temp12.columns).sort_index(axis=1), ["TPMd","TPMd_22"])
        TPM=pd.concat([TPM00,TPM01,TPM10,TPM11,TPM00d,TPM01d,TPM02d,TPM10d,TPM11d,TPM12d,TPM20d,TPM21d,TPM22d],axis=1, join="outer")

        if saveTPMs2csv==True:
            TPM00.to_csv(folder+'TPM00.csv',";")
            TPM01.to_csv(folder+'TPM01.csv',";")
            TPM10.to_csv(folder+'TPM10.csv',";")
            TPM11.to_csv(folder+'TPM11.csv',";")
        
        if inglobeIn_dfglob==True: 
            self._dfglob=self.addLevel(self._dfglob,["MD", "-"])
            self._dfglob=pd.concat([self._dfglob,TPM],axis=1, join="outer")
        else:
            self.TPMdf=TPM
        #add new level to df

    
    def groupByCondensed(self,col2Condense=("Weather","-","-",'AT Daily Average')):    ###### not used !!!

        # print(        self._dfglob.groupby(self._dfglob.loc[:,col2Condense]).describe().unstack())
        dfCondensed = self._dfglob.groupby(self._dfglob.loc[:,col2Condense]).describe()#.unstack()
        # print(dfCondensed)
        return dfCondensed
    
    
    def groupByCondensedBeta(self,col2Condense=('Weather', '-', '-', 'AT Daily Average')):    ###### not used !!!

        dfCondensed = self._dfglob.groupby(self._dfglob.loc[:,col2Condense]).mean().unstack()
        return dfCondensed

    def groupByCondensedMean(self,col2Condense=("Weather","-","-",'AT Daily Average')):

        dfCondensed = self._dfglob.groupby(self._dfglob.loc[:,col2Condense]).mean().unstack()
        return dfCondensed
    
    def addLevel(self,DataFrame, newLevels=[], addLeft=True, roll2=0):
        '''
        adding new levels into the DataFrame Object
        newLevels Labels should be provided as a list
        '''
        cols=DataFrame.columns.values
        newCols=[]
        for columnName in cols:
            newCN=[]
            lst=list(columnName)
            if addLeft==True:
                newCN=np.roll(np.array(newLevels+lst), roll2)
            else:
                newCN=lst+newLevels
            newCols.append(tuple(newCN))
        cols=MultiIndex.from_tuples(tuple(newCols))
        DataFrame.columns=cols
        return DataFrame
    
    def delColLev(self,DataFrameIn, levels=[]):
        cols=DataFrameIn.columns.values
        cols=np.array(list(cols)).T
        counts=0
        for level in range(len(cols)):
            if level not in levels:
                counts+=1
                if counts==1: 
                    newCols=np.array([cols[level]])
                else: 
                    newCols=np.concatenate((newCols,[cols[level]]))
        DataFrameIn.columns=MultiIndex.from_arrays(newCols)
        return DataFrameIn
            
    def tupleIt(self,lst):
        Tuples=[]
        for i in range(len(lst)):
            if i>0: Tuples.append((lst[i-1],lst[i]))
        return Tuples
    
    def loadDAATDayAfter(self, year=2012):    ###### not used !!!
        YEAR=str(year)
        atdf=pd.read_csv(self.recFolder+'AT/AT'+YEAR+'.csv', index_col=0, sep=';', header=[0,1,2,3])
        
    def simpleDiurnal(self, df, newLevels=[], addLeft=True, level4keepOnly=6, roll2=0, returnDF=True):
        print ("Start diurnal count...")
        start=time.clock()
        # generating a time column in datetime format in df
        if ("Time") not in df:
            df[("Time")] = df.index.map(lambda x: x.strftime("%H:%M"))
            print ("Column Time has been generated")
        # generate a global diurnal matrix (without conditions)


        dfTimeAll = df.groupby(df.loc[:,("Time")]).mean()

        dfTimeAll.index = pd.to_datetime(dfTimeAll.index.astype(str))
        newLevel= newLevels+["Standard Diurnal"]
        dfTimeAll=self.addLevel(dfTimeAll,newLevel, addLeft, roll2)
        print ("compiled in:",time.clock()-start,"seconds")
        if returnDF==True: 
            return dfTimeAll
        else:
            self.diurnalsdf=dfTimeAll
            
    def simpleDiurnalBiLevel(self, df, newLevels=[], addLeft=True, roll2=0, returnDF=True):
        print ("Start diurnal count...")
        start=time.clock()
        # generating a time column in datetime format in df
        if ("Time") not in df:
            df[("Time")] = df.index.map(lambda x: x.strftime("%H:%M"))
            print ("Column Time has been generated")
        # generate a global diurnal matrix (without conditions)

        dfTimeAll = df.groupby(df.loc[:,("Time")]).mean()#.unstack()

        dfTimeAll.index = pd.to_datetime(dfTimeAll.index.astype(str))
        dfTimeAll=self.addLevel(dfTimeAll,newLevels, addLeft, roll2)
        print ("compiled in:",time.clock()-start,"seconds")
        if returnDF==True: 
            return dfTimeAll
        else:
            self.diurnalsdf=dfTimeAll
            
    def wweDiurnal(self, df, newLevels=[], addLeft=True, level4keepOnly=6, roll2=0, returnDF=True):
        print ("Start diurnal count...")
        start=time.clock()
        if ("weekday") not in df:
            temp = pd.DatetimeIndex(df.index).copy()
            df[('weekday')] = temp.weekday
        if ("Time") not in df: df[("Time")] = df.index.map(lambda x: x.strftime("%H:%M"))
        weekdays_only = df[df[('weekday')] < 5 ]
        weekenddays_only = df[df[('weekday')] > 4 ]
        weekdays_only = weekdays_only.groupby(weekdays_only.loc[:,("Time")]).mean()
        weekenddays_only = weekenddays_only.groupby(weekenddays_only.loc[:,("Time")]).mean()#.unstack()
        weekdays_only.index = pd.to_datetime(weekdays_only.index.astype(str))
        try: weekenddays_only.index = pd.to_datetime(weekenddays_only.index.astype(str))
        except TypeError:
            print ("here it is the mistake... it means the groups are not buildable! change ranges for AT average or increase the range of data: ", type(weekenddays_only))
        newLevelsW=newLevels[:]
        newLevelsW+=["Week"]    
        newLevelsWE=newLevels[:]
        newLevelsWE+=["Week End"]
        weekdays_only=self.addLevel(weekdays_only,newLevelsW, addLeft, roll2)
        weekenddays_only=self.addLevel(weekenddays_only,newLevelsWE, addLeft, roll2)
        diurnalsdf=weekdays_only.join(weekenddays_only, how="outer")
        print ("compiled in:",time.clock()-start,"seconds")
        if returnDF==True: 
            return diurnalsdf
        else:
            self.diurnalswwedf=diurnalsdf
    
    def genDailyAverage(self,col2averageDaily=("Weather","-","-",'AT'), dailyAveNameLevel=3, round2decimals=1):
        print ("generating daily averages")
        start=time.clock()
        # 1. Generate a Daily average ambient temperature column
        daily_mean = pd.DataFrame(self._dfglob[col2averageDaily]).resample('D').mean()
        lst = list(col2averageDaily)
        lst[dailyAveNameLevel]=str(lst[dailyAveNameLevel])+" Daily Average"
        newColumnName = tuple(lst)
        print(daily_mean)
        daily_mean.columns=MultiIndex.from_tuples([newColumnName])
        print(daily_mean)
        self._dfglob=self._dfglob.join(daily_mean, how="outer")
        self._dfglob[newColumnName]=self._dfglob[newColumnName].fillna(method="ffill")
        self._dfglob[newColumnName]=self._dfglob[newColumnName].round(round2decimals)
        print ("compiled in:",time.clock()-start,"seconds")

    
    def genDiurnals(self, newLevels=[], addLeft=True, roll2=0, column2Group=("MD","-","Weather","-","-",'AT Daily Average'), groups=[],distinguishWWE=True):
        mainLev=["ATR"]
        Diurnals=self.simpleDiurnal(self._dfglob, mainLev + newLevels, addLeft, roll2)
        print ("diurnals have been generated")
        if distinguishWWE==True:
            Diurnals=Diurnals.join(self.wweDiurnal(self._dfglob, mainLev + newLevels, addLeft, roll2))
            print ("diurnals wwe have been generated")
        if len(groups)==0:
            print ("zero groups, work done!")
        else:
            print(groups)
            print(column2Group)
            newLevelStart=[np.array(column2Group)[5]+" <="+str(groups[0])] + newLevels[:]
            newLevelEnd=[np.array(column2Group)[5]+" >"+str(groups[-1])] + newLevels[:]

            left=self._dfglob[self._dfglob[column2Group] <= groups[0]]
            right=self._dfglob[self._dfglob[column2Group] > groups[-1]]
            Diurnals=Diurnals.join(self.simpleDiurnal(left, newLevelStart, addLeft, roll2))
            if distinguishWWE==True: Diurnals=Diurnals.join(self.wweDiurnal(left, newLevelStart, addLeft, roll2))
            tuplesOfGroups=self.tupleIt(groups)

            for element in tuplesOfGroups:
                midledf=self._dfglob[(self._dfglob[column2Group]>element[0]) & (self._dfglob[column2Group]<=element[1])]
                newLevelMidle=[str(element[0])+" < "+column2Group[5]+" <="+str(element[1])] + newLevels[:]
                Diurnals=Diurnals.join(self.simpleDiurnal(midledf, newLevelMidle, addLeft, roll2))
                if distinguishWWE==True: Diurnals=Diurnals.join(self.wweDiurnal(midledf, newLevelMidle, addLeft, roll2))

            Diurnals=Diurnals.join(self.simpleDiurnal(right, newLevelEnd, addLeft, roll2))
            if distinguishWWE==True: Diurnals=Diurnals.join(self.wweDiurnal(right, newLevelEnd, addLeft, roll2))
        
        self.Diurnals=Diurnals

    def genDiurnals_NewCode(self, newLevels=[], addLeft=True, roll2=0, column2Group=("MD","-","Weather","-","-",'AT Daily Average'), groups=[],distinguishWWE=True):

        mainLev=["ATR"]
        Diurnals=self.simpleDiurnal(self._dfglob, mainLev + newLevels, addLeft, roll2)
        print ("diurnals have been generated")
        if distinguishWWE==True: Diurnals=Diurnals.join(self.wweDiurnal(self._dfglob, mainLev + newLevels, addLeft, roll2))
        print ("diurnals wwe have been generated")
        if groups==[]: print ("zero groups, work done!")
        else:
            print(column2Group)
            newLevelStart=["DAAT<="+str(groups[0])] + newLevels[:]
            newLevelEnd=["DAAT>"+str(groups[-1])] + newLevels[:]

            left=self._dfglob[self._dfglob[column2Group] <= groups[0]]
            right=self._dfglob[self._dfglob[column2Group] > groups[-1]]
            Diurnals=Diurnals.join(self.simpleDiurnal(left, newLevelStart, addLeft, roll2))
            if distinguishWWE==True: Diurnals=Diurnals.join(self.wweDiurnal(left, newLevelStart, addLeft, roll2))
            tuplesOfGroups=self.tupleIt(groups)

            for element in tuplesOfGroups:
                midledf=self._dfglob[(self._dfglob[column2Group]>element[0]) & (self._dfglob[column2Group]<=element[1])]
                newLevelMidle=[str(element[0])+"<DAAT<="+str(element[1])] + newLevels[:]
                Diurnals=Diurnals.join(self.simpleDiurnal(midledf, newLevelMidle, addLeft, roll2))
                if distinguishWWE==True: Diurnals=Diurnals.join(self.wweDiurnal(midledf, newLevelMidle, addLeft, roll2))

            Diurnals=Diurnals.join(self.simpleDiurnal(right, newLevelEnd, addLeft, roll2))
            if distinguishWWE==True: Diurnals=Diurnals.join(self.wweDiurnal(right, newLevelEnd, addLeft, roll2))

        self.Diurnals=Diurnals
        
    def genDiurnalsDAAT(self,inputDF, column2Group=("MD","-","Weather","-","-",'AT Daily Average'),start='20120101'):
        recFolder='D:/EBC0018_PTJ_Volkswohnung_tos/HDF-Programming/pd4hdf/MarkovChain/MC4Windows/records/'
        print ("start Joining with Group-matrix")
        inputDF=inputDF.join(self.ATg,how='left')
        print ("Joining succeeded")
        uniqDA=np.unique(self.ATg.iloc[:,0])
        uniqPDDA=np.unique(self.ATg.iloc[:,1])
        print(uniqDA)
        diurnals=pd.DataFrame()
        for DA in uniqDA:
            for PDDA in uniqPDDA:
                print (DA, PDDA)
                if diurnals.empty:
                    matrix=inputDF[inputDF[("MD","-","Weather","-","-",'GDAAT')]==DA][inputDF[inputDF[("MD","-","Weather","-","-",'GDAAT')]==DA][("MD","-","Weather","-","-",'GPDAAT')]==PDDA]
                    matrix=matrix.iloc[:,matrix.columns.get_level_values(5)!="GDAAT"]
                    matrix=matrix.iloc[:,matrix.columns.get_level_values(5)!="GPDAAT"]
                    diurnals=self.simpleDiurnalBiLevel(matrix, [str(DA),str(PDDA)])
                else:
                    matrix=inputDF[inputDF[("MD","-","Weather","-","-",'GDAAT')]==DA][inputDF[inputDF[("MD","-","Weather","-","-",'GDAAT')]==DA][("MD","-","Weather","-","-",'GPDAAT')]==PDDA]
                    matrix=matrix.iloc[:,matrix.columns.get_level_values(5)!="GDAAT"]
                    matrix=matrix.iloc[:,matrix.columns.get_level_values(5)!="GPDAAT"]
                    diurnals=diurnals.join(self.simpleDiurnalBiLevel(matrix, [str(DA),str(PDDA)]),how='left')


        diurnals=diurnals.join(self.simpleDiurnal(self._dfglob, ["ATR"]),how='left')
        self.Diurnals=diurnals
        return diurnals #todo return is needed????

    def checkAvailableDataSW(self,fileName='B2E1_20121_201212.csv'):    ###### not used !!!
        recFolder='D:/EBC0018_PTJ_Volkswohnung_tos/HDF-Programming/pd4hdf/MarkovChain/MC4Windows/records/'
        self.Original=pd.read_csv(recFolder+'/dfGlob/'+fileName, index_col=0, sep=';', header=[0,1,2,3],skiprows=[4], parse_dates=True, low_memory=True)
        self.Original=self.Original.iloc[:, self.Original.columns.get_level_values(2)!="Room_Children"]
        self.Original=self.Original.iloc[:, self.Original.columns.get_level_values(2)!="Room_Sleeping"]
        self.Original=self.Original.iloc[:, self.Original.columns.get_level_values(3)!="Wind_Speed"]
        self.Original=self.Original.sort_index(axis=1)
        self.proSetSWBeta=self.delColLev(self.proSetSW,[0,1])
        self.Or=self.Original.iloc[:, self.Original.columns.get_level_values(0)!="Weather"]
        self.Or=self.Or.dropna(0, "all")
        self.proSetSWBeta=self.proSetSWBeta.reindex(self.Or.index)
        self.proSetSWBeta=self.addLevel(self.proSetSWBeta,["MD","-"])
    
    def checkAvailableDataDW(self,fileName='B2E1_20121_201212.csv'):    ###### not used !!!
        recFolder='D:/EBC0018_PTJ_Volkswohnung_tos/HDF-Programming/pd4hdf/MarkovChain/MC4Windows/records/'
        self.proSetDWBeta=self.delColLev(self.proSetDW.copy(),[0,1])
        self.Original=pd.read_csv(recFolder+'/dfGlob/'+fileName, index_col=0, sep=';', header=[0,1,2,3],skiprows=[4], parse_dates=True, low_memory=True)
        self.Original=self.Original.iloc[:, self.Original.columns.get_level_values(2)!="Room_Living"]
        self.Original=self.Original.iloc[:, self.Original.columns.get_level_values(2)!="Room_Kitchen"]
        self.Original=self.Original.iloc[:, self.Original.columns.get_level_values(2)!="Room_Bath"]
        self.Original=self.Original.iloc[:, self.Original.columns.get_level_values(3)!="Wind_Speed"]
        self.Original=self.Original.sort_index(axis=1)
        toJoin=self.proSetDWBeta.iloc[:,0]
        self.Or=self.Original.iloc[:, self.Original.columns.get_level_values(0)!="Weather"]
        self.Or=self.Or.dropna(0, "all")
        self.proSetDWBeta=self.proSetDWBeta.reindex(self.Or.index)
        self.proSetDWBeta=self.addLevel(self.proSetDWBeta,["MD","-"])

        
    def findUniqueNr(self,df,string4splitting="< AT Daily Average <="):  
        cols=df.columns.values
        cols=np.array(list(cols)).T
        uniques= np.unique(cols[0])
        groups=[]
        for stringC0 in uniques:
            # print stringC0
            if string4splitting in stringC0: 
                groups.append(int(stringC0.split(string4splitting)[0]))
                groups.append(int(stringC0.split(string4splitting)[1]))
        return np.unique(groups)
    
    def findATrange(self, ATvalue, ranges):
        if len(ranges)==0: return "ATR"
        else:
            if ATvalue<ranges[0]: levelName='AT Daily Average <='+str(ranges[0])
            for index in range(len(ranges)-1):
                if ATvalue>ranges[0+index] and ATvalue<=ranges[1+index]: levelName=str(ranges[0+index])+'< AT Daily Average <='+str(ranges[1+index])
            if ATvalue>ranges[-1]: levelName='AT Daily Average >'+str(ranges[-1])
            return levelName
    
    def findATrangeDAAT(self, ATvalue, ranges):
        if len(ranges)==0: return "ATR"
        else:
            if ATvalue<ranges[0]: levelName='DAAT<='+str(ranges[0])
            for index in range(len(ranges)-1):
                if ATvalue>ranges[0+index] and ATvalue<=ranges[1+index]: levelName=str(ranges[0+index])+'<DAAT<='+str(ranges[1+index])
            if ATvalue>ranges[-1]: levelName='DAAT>'+str(ranges[-1])
            return levelName
        
    def findShortATrange(self, ATvalue, ranges):
        '''
        used when generating new profiles
        :param ATvalue:
        :param ranges:
        :return:
        '''
        if len(ranges)==0: return "ATR"
        else:
            if ATvalue<=ranges[0]: levelName='DAAT<='+str(ranges[0])
            for index in range(len(ranges)-1):
                if ATvalue>ranges[0+index] and ATvalue<=ranges[1+index]: levelName=str(ranges[0+index])+'<DAAT<='+str(ranges[1+index])
            if ATvalue>ranges[-1]: levelName='DAAT>'+str(ranges[-1])
            return levelName

    def findShortATrange_NEW(self, ATvalue):
        '''
        new version based on WinProGen
        '''
        ranges=self.temperature_groups
        if len(ranges)==0: return "ATR"
        else:
            if ATvalue<=ranges[0]: levelName='DAAT<='+str(ranges[0])
            for index in range(len(ranges)-1):
                if ATvalue>ranges[0+index] and ATvalue<=ranges[1+index]: levelName=str(ranges[0+index])+'<DAAT<='+str(ranges[1+index])
            if ATvalue>ranges[-1]: levelName='DAAT>'+str(ranges[-1])
            return levelName
          
    def genProfilesDAAT(self, startDay='01/01/2015', simDays=1, weather_data="original", val_horizon=1):
        self.turbo_marker = 1
        # getting the TPMs
        sTPM=self.TPM2x2
        dTPM=self.TPM3x3

        casesSW = int(sTPM.shape[1]/4)
        casesDW = int(dTPM.shape[1]/9)

        if isinstance(startDay, str)==True:
            startDay=datetime.date(int(startDay.split("/")[2]),int(startDay.split("/")[1]),int(startDay.split("/")[0]))
        YEAR=str(startDay.year)
        if weather_data == "original":
            atdf=pd.read_csv(self.recFolder+'/AT/AT'+YEAR+'.csv', index_col=0, sep=';', header=[0,1,2,3])
        else:
            atdf = pd.read_csv(weather_data, index_col=0, sep=';', header=[0, 1, 2, 3])
        day0=date(startDay.year,1,1)
        deltaDayStartDay1=startDay-day0
        uniqueATR=self.findUniqueNr(sTPM,string4splitting="<DAAT<=")
        # df containing later on the mean values of AT, to be used in the diurnal-profile generation grouping on AT
        atdfDiurnal=pd.DataFrame() 
        for index, day in enumerate(range(simDays)):
            start = time.clock()
            if calendar.isleap(startDay.year)==True: 
                daysperyear=365
            else: 
                daysperyear=366
            if day+deltaDayStartDay1.days>daysperyear:
                dayIndex=(day+deltaDayStartDay1.days)%daysperyear+1
                startDay=date(startDay.year,1,1)
            else: dayIndex=day
            print (startDay+timedelta(days=dayIndex))
            dtSerie = pd.date_range(startDay+timedelta(days=dayIndex),periods=1440, freq="min")
            Atemp=atdf.loc[str(dtSerie[dayIndex].date()),:][0]
            
            dayAfter=startDay+timedelta(days=dayIndex+1)
            dayAfter=dayAfter.replace(startDay.year)
            
            AtempDayAfter=atdf.loc[str(dayAfter),:][0]
            atdfDiurnal = atdfDiurnal.append(DataFrame(Atemp,index=dtSerie,columns=MultiIndex.from_tuples([("MD","-","Weather","-","-",'AT Daily Average')])))

            ATinterval=self.findATrangeDAAT(Atemp, uniqueATR)
            ATintervalDayAfter=self.findATrangeDAAT(AtempDayAfter, uniqueATR)
            weekDay=dtSerie[0].weekday()
            if weekDay<5: dayOfTheWeek="Week"
            else: dayOfTheWeek="Week End"
            print (day, Atemp, uniqueATR)
            levels=[ATinterval, ATintervalDayAfter]
            print (levels)
            if day==0:
                
                # generate start values for single windows rooms
                rNSW=np.random.uniform(0,1,casesSW)
                starts2x2=self.start2x2.iloc[:, self.start2x2.columns.get_level_values(3)=="TPM_00"]
                self.startValuesSW=pd.DataFrame(np.where(rNSW>starts2x2, 1, 0), columns=starts2x2.columns)
                # generate start values for double windows rooms
                rNDW=np.random.uniform(0,1,casesDW)
                starts3x3_0=self.start3x3.iloc[:, self.start3x3.columns.get_level_values(3)=="TPMd_00"]
                starts3x3_1=self.start3x3.iloc[:, self.start3x3.columns.get_level_values(3)=="TPMd_11"]
                self.startValuesDW=pd.DataFrame(np.where(rNDW>starts3x3_0, np.where(rNDW>starts3x3_0.values+starts3x3_1.values, 2, 1), 0),index=starts3x3_0.index, columns=starts3x3_0.columns)
                
                self.proSetSW=self.genProfileSW(levels=levels,timeIndex=dtSerie,day=day)
                self.proSetDW=self.genProfileDW(levels=levels,timeIndex=dtSerie,day=day)

            else:

                self.startValuesSW=pd.DataFrame([self.proSetSW.iloc[-1,:].values], columns=self.proSetSW.columns)
                self.startValuesDW=pd.DataFrame([self.proSetDW.iloc[-1,:].values], columns=self.proSetDW.columns)
                self.proSetSW=self.proSetSW.append(self.genProfileSW(levels=levels,timeIndex=dtSerie,day=day))
                self.proSetDW=self.proSetDW.append(self.genProfileDW(levels=levels,timeIndex=dtSerie,day=day))

            diff = time.clock() - start
            self.duration = (index * self.duration + diff) / (index + 1)  # moving average for duration of one loop

        self.proSetSW=pd.concat([self.delColLev(self.proSetSW,[2,3,8]), atdfDiurnal], axis=1)
        self.proSetDW_S=self.addLevel(self.delColLev(pd.DataFrame(np.where(self.proSetDW.values==1,1,0),index= self.proSetDW.index,columns= self.proSetDW.columns),[2,3,7]),["WP1"], addLeft=False)
        self.proSetDW_AtLeastOne=self.addLevel(self.delColLev(pd.DataFrame(np.where(self.proSetDW.values>=1,1,0),index= self.proSetDW.index,columns= self.proSetDW.columns),[2,3,7]),["WP1"], addLeft=False)
        self.proSetDW_D=self.addLevel(self.delColLev(pd.DataFrame(np.where(self.proSetDW.values==2,1,0),index= self.proSetDW.index,columns= self.proSetDW.columns),[2,3,7]),["WP2"], addLeft=False)
        self.proSetDW_Sum=pd.concat([self.delColLev(self.proSetDW,[2,3,8]), atdfDiurnal], axis=1)
        self.proSetDW=pd.concat([self.proSetDW_AtLeastOne,self.proSetDW_D, atdfDiurnal], axis=1).sort_index(axis=1)
        self.turbo_marker = 0

    def generate_profiles_M1(self, TPM, starts, weather_data_year, startDay='01/01/2015', simDays=31, Model='M1', mode="pro"):
        
        if isinstance(startDay, str)==True:
            startDay=datetime.date(weather_data_year,int(startDay.split("/")[1]),int(startDay.split("/")[0]))
        YEAR=str(startDay.year)
        timestep=1 # in minutes
        duration=int(simDays*24*60/timestep)
        dtSerie = pd.date_range(startDay,periods=duration, freq="min")

        # Model='M1'
        if Model=='M2':
            criterium_2_start=dtSerie[0].weekday()
            if criterium_2_start<5: criterium_2_start="Week"
            else: criterium_2_start="Week End"
            #print(criterium_2_start)
        elif Model=='M1':
            criterium_2_start='Standard Diurnal'
            criterium_2='Standard Diurnal'
        elif Model=='M3':
            criterium_2_start=self.ATg.ix[0,1]
            criterium_2=self.ATg.ix[0,1]


        fields=list(set([a for a in TPM.columns.get_level_values(4).values]))
        zones=list(set([a for a in TPM.columns.get_level_values(5).values]))
        rooms=list(set([a for a in TPM.columns.get_level_values(6).values]))
        print(rooms)
        gen_profs=pd.DataFrame(index=dtSerie)

        for field in fields:
            for zone in zones:
                for room in rooms:
                    binarycodes = (literal_eval(TPM.loc[:,
                                                idx[self.ATg.iloc[0, 0], criterium_2_start, "['All closed']", :, field,
                                                zone, room, 'TPM']].columns.get_level_values(3)[0]))
                    self.combinations += len(binarycodes)
        self.combinations = self.combinations*len(dtSerie)

        for field in fields:
            for zone in zones:
                for room in rooms:
                    states_container=[]
                    binarycodes=(literal_eval(TPM.loc[:,idx[self.ATg.iloc[0,0],criterium_2_start,"['All closed']",:,field,zone,room,'TPM']].columns.get_level_values(3)[0]))



                    for t_s_index, t_s in enumerate(dtSerie):
                        start = time.clock()
                        if t_s_index==0:
                            probability_array=starts.loc[idx[starts.index[0]],idx[self.ATg.ix[t_s,0],criterium_2_start,:,:,field,zone,room,:]]
                            is_state_binary=self.assign_random_to_combination(probability_array[0],np.random.uniform(0,1))
                            states_container.append(is_state_binary)
                        else:
                            if Model=='M2':
                                criterium_2=dtSerie[t_s_index].weekday()
                                if criterium_2<5: criterium_2="Week"
                                else: criterium_2="Week End"
                            if Model=='M3':
                                criterium_2=self.ATg.ix[t_s,1]



                            day_counter=int(t_s_index/1440)
                            if t_s_index%1440==0:
                                print(t_s_index/1440)

                            past_state=([i for (i, v) in zip(binarycodes, states_container[t_s_index-1]) if v==1][0])

                            probability_array=TPM.loc[idx[TPM.index[t_s_index-day_counter*1440]],idx[self.ATg.ix[t_s,0],criterium_2,past_state,:,field,zone,room,:]]
                            is_state_binary=self.assign_random_to_combination(probability_array[0],np.random.uniform(0,1), infos=[t_s,self.ATg.ix[t_s,0],criterium_2,past_state, field,zone,room])
                            states_container.append(is_state_binary)
                        self.already_done += len(binarycodes)
                        mD_gen_WSP.wsp_start_progress = 1

                    states_container=np.array(states_container).T
                    for index, element in enumerate(binarycodes):
                        gen_profs[field, zone, room, element]=states_container[index]

        gen_profs.columns=MultiIndex.from_tuples(gen_profs.columns)
        fields=list(set([a for a in gen_profs.columns.get_level_values(0).values]))
        zones=list(set([a for a in gen_profs.columns.get_level_values(1).values]))
        rooms=list(set([a for a in gen_profs.columns.get_level_values(2).values]))
        gen_profs.sort_index(axis=1,inplace=True)

        self.gen_profs_original=gen_profs.copy()

        gen_profs.drop("['All closed']", axis=1, level=3, inplace=True)
        combs2drops=[]

        for field in fields:
            zones=list(set([a for a in TPM.loc[:, idx[self.ATg.iloc[0,0], criterium_2_start, "['All closed']",:, field,:,:,'TPM']].columns.get_level_values(5).values]))
            for zone in zones:
                rooms=list(set([a for a in TPM.loc[:, idx[self.ATg.iloc[0,0], criterium_2_start, "['All closed']",:, field,zone,:,'TPM']].columns.get_level_values(6).values]))
                for room in rooms:

                    windows_state_combs=list(set([a for a in gen_profs.loc[idx[:], idx[field, zone, room, :]].columns.get_level_values(3).values]))
                    if len(windows_state_combs)>1:
                        for state_comb in windows_state_combs:
                            state_comb_array=literal_eval(str(state_comb).replace('[','').replace(']',''))
                            if str(state_comb_array).count("'")>2: # exclude redundancies                                combs2drops.append(state_comb)
                                for window in state_comb_array:
                                    window="['"+window+"']"
                                    gen_profs.loc[idx[:], idx[field, zone, room, window]]=np.where(gen_profs.loc[idx[:],
                                    idx[field, zone, room, state_comb]]==1, 1, gen_profs.loc[idx[:], idx[field, zone, room, window]])


        for combs2drop in combs2drops:
            gen_profs.drop(combs2drop, axis=1, level=3, inplace=True)

        self.gen_profs=gen_profs


    def generate_profiles_M2(self, TPM, starts, weather_data_year, startDay='01/01/2015', simDays=31, mode="pro"):

        if isinstance(startDay, str)==True:
            startDay=datetime.date(weather_data_year,int(startDay.split("/")[1]),int(startDay.split("/")[0]))
        YEAR=str(startDay.year)
        timestep=1 # in minutes
        duration=int(simDays*24*60/timestep)
        dtSerie = pd.date_range(startDay,periods=duration, freq="min")
        criterium_2_start=dtSerie[0].weekday()
        if criterium_2_start<5: criterium_2_start="Week"
        else: criterium_2_start="Week End"

        fields=list(set([a for a in TPM.columns.get_level_values(4).values]))
        zones=list(set([a for a in TPM.columns.get_level_values(5).values]))
        rooms=list(set([a for a in TPM.columns.get_level_values(6).values]))

        gen_profs=pd.DataFrame(index=dtSerie)

        for field in fields:
            for zone in zones:
                for room in rooms:
                    binarycodes = (literal_eval(TPM.loc[:,
                                                idx[self.ATg.iloc[0, 0], criterium_2_start, "['All closed']", :, field,
                                                zone, room, 'TPM']].columns.get_level_values(3)[0]))
                    self.combinations += len(binarycodes)
        self.combinations = self.combinations*len(dtSerie)

        for field in fields:
            zones=list(set([a for a in TPM.loc[:, idx[self.ATg.iloc[0,0], criterium_2_start, "['All closed']",:, field,:,:,'TPM']].columns.get_level_values(5).values]))
            for zone in zones:
                rooms=list(set([a for a in TPM.loc[:, idx[self.ATg.iloc[0,0], criterium_2_start, "['All closed']",:, field,zone,:,'TPM']].columns.get_level_values(6).values]))
                for room in rooms:
                    states_container=[]
                    print(criterium_2_start)
                    binarycodes=(literal_eval(TPM.loc[:,idx[self.ATg.iloc[0,0],criterium_2_start,"['All closed']",:,field,zone,room,'TPM']].columns.get_level_values(3)[0]))

                    for t_s_index, t_s in enumerate(dtSerie):
                        if t_s_index==0:
                            probability_array=starts.loc[idx[starts.index[0]],idx[self.ATg.ix[t_s,0],criterium_2_start,:,:,field,zone,room,:]]
                            is_state_binary=self.assign_random_to_combination(probability_array[0],np.random.uniform(0,1))
                            states_container.append(is_state_binary)
                        else:
                            criterium_2=dtSerie[t_s_index].weekday()
                            if criterium_2<5: criterium_2="Week"
                            else: criterium_2="Week End"

                            day_counter=int(t_s_index/1440)
                            if t_s_index%1440==0:
                                print(t_s_index/1440)

                            past_state=([i for (i, v) in zip(binarycodes, states_container[t_s_index-1]) if v==1][0])

                            probability_array=TPM.loc[idx[TPM.index[t_s_index-day_counter*1440]],idx[self.ATg.ix[t_s,0],criterium_2,past_state,:,field,zone,room,:]]
                            is_state_binary=self.assign_random_to_combination(probability_array[0],np.random.uniform(0,1), infos=[t_s,self.ATg.ix[t_s,0],criterium_2,past_state, field,zone,room])
                            states_container.append(is_state_binary)
                        self.already_done += len(binarycodes)
                        mD_gen_WSP.wsp_start_progress = 1

                    states_container=np.array(states_container).T
                    for index, element in enumerate(binarycodes):
                        gen_profs[field, zone, room, element]=states_container[index]

        gen_profs.columns=MultiIndex.from_tuples(gen_profs.columns)
        fields=list(set([a for a in gen_profs.columns.get_level_values(0).values]))
        zones=list(set([a for a in gen_profs.columns.get_level_values(1).values]))
        rooms=list(set([a for a in gen_profs.columns.get_level_values(2).values]))
        gen_profs.sort_index(axis=1,inplace=True)

        self.gen_profs_original=gen_profs.copy()

        gen_profs.drop("['All closed']", axis=1, level=3, inplace=True)
        combs2drops=[]
        for field in fields:
            for zone in zones:
                for room in rooms:
                    windows_state_combs=list(set([a for a in gen_profs.loc[idx[:], idx[field, zone, room, :]].columns.get_level_values(3).values]))
                    if len(windows_state_combs)>1:
                        for state_comb in windows_state_combs:
                            state_comb_array=literal_eval(str(state_comb).replace('[','').replace(']',''))
                            if str(state_comb_array).count("'")>2:
                                combs2drops.append(state_comb)
                                for window in state_comb_array:
                                    window="['"+window+"']"
                                    gen_profs.loc[idx[:], idx[field, zone, room, window]]=np.where(gen_profs.loc[idx[:],
                                    idx[field, zone, room, state_comb]]==1, 1, gen_profs.loc[idx[:], idx[field, zone, room, window]])


        for combs2drop in combs2drops:
            gen_profs.drop(combs2drop, axis=1, level=3, inplace=True)
        self.gen_profs=gen_profs

    def generate_profiles_M3(self, TPM, starts, weather_data_year, startDay='01/01/2015', simDays=31, mode="pro"):

        if isinstance(startDay, str)==True:
            #startDay=datetime.date(int(startDay.split("/")[2]),int(startDay.split("/")[1]),int(startDay.split("/")[0]))
            startDay=datetime.date(weather_data_year,int(startDay.split("/")[1]),int(startDay.split("/")[0]))
        YEAR=str(startDay.year)
        timestep=1 # in minutes
        duration=int(simDays*24*60/timestep)
        dtSerie = pd.date_range(startDay,periods=duration, freq="min")



        criterium_2_start=self.ATg.ix[0,1]
        criterium_2=self.ATg.ix[0,1]


        fields=list(set([a for a in TPM.columns.get_level_values(4).values]))
        zones=list(set([a for a in TPM.columns.get_level_values(5).values]))
        rooms=list(set([a for a in TPM.columns.get_level_values(6).values]))

        gen_profs=pd.DataFrame(index=dtSerie)

        for field in fields:
            for zone in zones:
                for room in rooms:
                    binarycodes = (literal_eval(TPM.loc[:,
                                                idx[self.ATg.iloc[0, 0], criterium_2_start, "['All closed']", :, field,
                                                zone, room, 'TPM']].columns.get_level_values(3)[0]))
                    self.combinations += len(binarycodes)
        self.combinations = self.combinations*len(dtSerie)

        for field in fields:
            zones=list(set([a for a in TPM.loc[:, idx[self.ATg.iloc[0,0], criterium_2_start, "['All closed']",:, field,:,:,'TPM']].columns.get_level_values(5).values]))
            for zone in zones:
                rooms=list(set([a for a in TPM.loc[:, idx[self.ATg.iloc[0,0], criterium_2_start, "['All closed']",:, field,zone,:,'TPM']].columns.get_level_values(6).values]))
                for room in rooms:
                    states_container=[]
                    binarycodes=(literal_eval(TPM.loc[:,idx[self.ATg.iloc[0,0],criterium_2_start,"['All closed']",:,field,zone,room,'TPM']].columns.get_level_values(3)[0]))

                    for t_s_index, t_s in enumerate(dtSerie):
                        if t_s_index==0:
                            probability_array=starts.loc[idx[starts.index[0]],idx[self.ATg.ix[t_s,0],criterium_2_start,:,:,field,zone,room,:]]
                            is_state_binary=self.assign_random_to_combination(probability_array[0],np.random.uniform(0,1))
                            states_container.append(is_state_binary)
                            #temperature_array=weather_data[0]
                        else:
                            criterium_2=self.ATg.ix[t_s,1]
                            day_counter=int(t_s_index/1440)
                            if t_s_index%1440==0:
                                print(t_s_index/1440)
                                #print(TPM.index[t_s_index-day_counter*1440])

                            past_state=([i for (i, v) in zip(binarycodes, states_container[t_s_index-1]) if v==1][0])
                            # if past_state != "['All closed']":
                            #     print(past_state, t_s_index)
                            probability_array=TPM.loc[idx[TPM.index[t_s_index-day_counter*1440]],idx[self.ATg.ix[t_s,0],criterium_2,past_state,:,field,zone,room,:]]
                            is_state_binary=self.assign_random_to_combination(probability_array[0],np.random.uniform(0,1), infos=[t_s,self.ATg.ix[t_s,0],criterium_2,past_state, field,zone,room])
                            states_container.append(is_state_binary)
                        self.already_done += len(binarycodes)
                        # print ("%.2f" % (self.already_done/self.combinations*100))
                        mD_gen_WSP.wsp_start_progress = 1

                    states_container=np.array(states_container).T
                    for index, element in enumerate(binarycodes):
                        gen_profs[field, zone, room, element]=states_container[index]

        gen_profs.columns=MultiIndex.from_tuples(gen_profs.columns)
        fields=list(set([a for a in gen_profs.columns.get_level_values(0).values]))
        zones=list(set([a for a in gen_profs.columns.get_level_values(1).values]))
        rooms=list(set([a for a in gen_profs.columns.get_level_values(2).values]))
        gen_profs.sort_index(axis=1,inplace=True)

        self.gen_profs_original=gen_profs.copy()

        gen_profs.drop("['All closed']", axis=1, level=3, inplace=True)
        combs2drops=[]
        for field in fields:
            for zone in zones:
                for room in rooms:
                    windows_state_combs=list(set([a for a in gen_profs.loc[idx[:], idx[field, zone, room, :]].columns.get_level_values(3).values]))
                    if len(windows_state_combs)>1:
                        for state_comb in windows_state_combs:
                            state_comb_array=literal_eval(str(state_comb).replace('[','').replace(']',''))
                            if str(state_comb_array).count("'")>2:
                                combs2drops.append(state_comb)
                                for window in state_comb_array:
                                    window="['"+window+"']"

                                    gen_profs.loc[idx[:], idx[field, zone, room, window]]=np.where(gen_profs.loc[idx[:],
                                    idx[field, zone, room, state_comb]]==1, 1, gen_profs.loc[idx[:], idx[field, zone, room, window]])

        for combs2drop in combs2drops:
            gen_profs.drop(combs2drop, axis=1, level=3, inplace=True)
        self.gen_profs=gen_profs


    def genProfiles(self, startDay='01/01/2015', simDays=1, distinguishWWE=True, weather_data="original", val_horizon=1):
        self.turbo_marker = 1
        # getting the TPMs
        sTPM=self.TPM2x2
        dTPM=self.TPM3x3
        casesSW = int(sTPM.shape[1]/4)
        casesDW = int(dTPM.shape[1]/9)
        if isinstance(startDay, str)==True:
            startDay=datetime.date(int(startDay.split("/")[2]),int(startDay.split("/")[1]),int(startDay.split("/")[0]))
        YEAR=str(startDay.year)
        if weather_data=="original":
            atdf=pd.read_csv(self.recFolder+'/AT/AT'+YEAR+'.csv', index_col=0, sep=';', header=[0,1,2,3])
        else:
            atdf=pd.read_csv(weather_data, index_col=0, sep=';', header=[0,1,2,3])
        day0=date(startDay.year,1,1)
        deltaDayStartDay1=startDay-day0
        uniqueATR=self.findUniqueNr(sTPM)
        # df containing later on the mean values of AT, to be used in the diurnal-profile generation grouping on AT
        atdfDiurnal=pd.DataFrame()
        for index, day in enumerate(range(simDays)):
            start = time.clock()
            if calendar.isleap(startDay.year)==True:
                daysperyear=365
            else:
                daysperyear=366
            if day+deltaDayStartDay1.days>daysperyear:
                dayIndex=(day+deltaDayStartDay1.days)%daysperyear+1
                startDay=date(startDay.year,1,1)
            else: dayIndex=day
            print (startDay+timedelta(days=dayIndex))
            dtSerie = pd.date_range(startDay+timedelta(days=dayIndex),periods=1440, freq="min")
            Atemp=atdf.loc[str(dtSerie[dayIndex].date()),:][0]
            atdfDiurnal = atdfDiurnal.append(DataFrame(Atemp,index=dtSerie,columns=MultiIndex.from_tuples([("MD","-","Weather","-","-",'AT Daily Average')])))
            ATinterval=self.findATrange(Atemp, uniqueATR)
            weekDay=dtSerie[0].weekday()
            if weekDay<5: dayOfTheWeek="Week"
            else: dayOfTheWeek="Week End"
            if distinguishWWE==False: dayOfTheWeek="Standard Diurnal"
            levels=[ATinterval, dayOfTheWeek]
            print (day)
            if day==0:

                # generate start values for single windows rooms
                rNSW=np.random.uniform(0,1,casesSW)
                starts2x2=self.start2x2.iloc[:, self.start2x2.columns.get_level_values(3)=="TPM_00"]
                self.startValuesSW=pd.DataFrame(np.where(rNSW>starts2x2, 1, 0), columns=starts2x2.columns)
                # generate start values for double windows rooms
                rNDW=np.random.uniform(0,1,casesDW)
                starts3x3_0=self.start3x3.iloc[:, self.start3x3.columns.get_level_values(3)=="TPMd_00"]
                starts3x3_1=self.start3x3.iloc[:, self.start3x3.columns.get_level_values(3)=="TPMd_11"]
                self.startValuesDW=pd.DataFrame(np.where(rNDW>starts3x3_0, np.where(rNDW>starts3x3_0.values+starts3x3_1.values, 2, 1), 0),index=starts3x3_0.index, columns=starts3x3_0.columns)

                self.proSetSW=self.genProfileSW(levels=levels,timeIndex=dtSerie,day=day)
                self.proSetDW=self.genProfileDW(levels=levels,timeIndex=dtSerie,day=day)
            else:
                self.startValuesSW=pd.DataFrame([self.proSetSW.iloc[-1,:].values], columns=self.proSetSW.columns)
                self.startValuesDW=pd.DataFrame([self.proSetDW.iloc[-1,:].values], columns=self.proSetDW.columns)
                self.proSetSW=self.proSetSW.append(self.genProfileSW(levels=levels,timeIndex=dtSerie,day=day))
                self.proSetDW=self.proSetDW.append(self.genProfileDW(levels=levels,timeIndex=dtSerie,day=day))

            diff = time.clock() - start
            self.duration = (index * self.duration + diff) / (index + 1)  # moving average for duration of one loop

        self.proSetSW=pd.concat([self.addLevel(self.delColLev(self.proSetSW,[2,3,7,8]),["WP1"], addLeft=False), atdfDiurnal], axis=1)
        self.proSetDW_S=self.addLevel(self.delColLev(pd.DataFrame(np.where(self.proSetDW.values==1,1,0),index= self.proSetDW.index,columns= self.proSetDW.columns),[2,3,7]),["WP1"], addLeft=False)
        self.proSetDW_AtLeastOne=self.addLevel(self.delColLev(pd.DataFrame(np.where(self.proSetDW.values>=1,1,0),index= self.proSetDW.index,columns= self.proSetDW.columns),[2,3,7]),["WP1"], addLeft=False)
        self.proSetDW_D=self.addLevel(self.delColLev(pd.DataFrame(np.where(self.proSetDW.values==2,1,0),index= self.proSetDW.index,columns= self.proSetDW.columns),[2,3,7]),["WP2"], addLeft=False)
        self.proSetDW_Sum=pd.concat([self.delColLev(self.proSetDW,[2,3,8]), atdfDiurnal], axis=1)        
        self.proSetDW=pd.concat([self.proSetDW_AtLeastOne,self.proSetDW_D, atdfDiurnal], axis=1).sort_index(axis=1)
        self.turbo_marker = 0


    def genProfileSW(self, levels=["ATR", "Standard Diurnal"],timeIndex=[], day=0):

        # get the single matrix components
        newCols=self.TPM2x2.loc[idx[:],idx["ATR", "Standard Diurnal",:,'TPM_00_R',:,:,:,:]].columns

        if day==0: 
            startValuesSW=self.startValuesSW.loc[idx[:],idx[levels[0],levels[1],:,:,:,:,:,:]].values
        else: startValuesSW=self.startValuesSW.loc[idx[:],idx["ATR", "Standard Diurnal",:,:,:,:,:,:]].values

        TPM00=self.TPM2x2.loc[idx[:],idx[levels[0],levels[1],:,'TPM_00_R',:,:,:,:]].copy()
        TPM11=self.TPM2x2.loc[idx[:],idx[levels[0],levels[1],:,'TPM_11_R',:,:,:,:]].copy()
        TPM00.columns=newCols
        TPM11.columns=newCols
        
        proSet=pd.DataFrame(np.random.uniform(0,1,TPM00.shape))
        dfTOP=pd.DataFrame(startValuesSW)
        proSet=dfTOP.append(proSet, ignore_index=True)
        dfTOP=pd.DataFrame(startValuesSW, columns=newCols)
        TPM00=dfTOP.append(TPM00, ignore_index=True)
        dfTOP=pd.DataFrame(startValuesSW, columns=newCols)
        TPM11=dfTOP.append(TPM11, ignore_index=True)
        proSet.columns=TPM11.columns

        for index in range(1441):
            if index>0:
                proSet.iloc[index]=np.where(proSet.iloc[index-1]==0,np.where(proSet.iloc[index]>TPM00.iloc[index],1,0),np.where(proSet.iloc[index]>TPM11.iloc[index],0,1))
        
        proSet.columns=newCols
        proSet=proSet.iloc[0:-1,:].copy()
        proSet.index=timeIndex

        plotting=False
        if plotting==True:
            fig = plt.figure(figsize=(16,9), dpi=80)
            ax = fig.add_subplot(111)
            proSet.plot(ax=ax)
            # Hide the right and top spines
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            fig.subplots_adjust(left=0.1,bottom=0.24, top=0.9)
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),frameon=False, ncol=1)#, fontsize=font['size'])
            plt.show()
        return proSet
    
    def genProfileDW(self, levels=["ATR", "Standard Diurnal"],timeIndex=[], day=0):
        
        # get the single matrix components
        newCols=self.TPM3x3.loc[idx[:],idx["ATR", "Standard Diurnal",:,'TPMd_00_R',:,:,:,:]].columns
        
        if day==0: 
            startValuesDW=self.startValuesDW.loc[idx[:],idx[levels[0],levels[1],:,:,:,:,:,:]].values
        else: 
            startValuesDW=self.startValuesDW.loc[idx[:],idx["ATR", "Standard Diurnal",:,:,:,:,:,:]].values
            # NOTE: "ATR", "Standard Diurnal" are just the name of the columns in the proSet matrix, 
            # and do not provide real information about temperature and day
            # it has been done this way to allow for merging different columns inputs into the final proSet matrix  
        TPM00=self.TPM3x3.loc[idx[:],idx[levels[0],levels[1],:,'TPMd_00_R',:,:,:,:]].copy()
        TPM01=self.TPM3x3.loc[idx[:],idx[levels[0],levels[1],:,'TPMd_01_R',:,:,:,:]].copy()
        TPM10=self.TPM3x3.loc[idx[:],idx[levels[0],levels[1],:,'TPMd_10_R',:,:,:,:]].copy()
        TPM11=self.TPM3x3.loc[idx[:],idx[levels[0],levels[1],:,'TPMd_11_R',:,:,:,:]].copy()
        TPM20=self.TPM3x3.loc[idx[:],idx[levels[0],levels[1],:,'TPMd_20_R',:,:,:,:]].copy()
        TPM21=self.TPM3x3.loc[idx[:],idx[levels[0],levels[1],:,'TPMd_21_R',:,:,:,:]].copy()
        TPM22=self.TPM3x3.loc[idx[:],idx[levels[0],levels[1],:,'TPMd_22_R',:,:,:,:]].copy()
        # assign same column names to make them comparable and appendable to proSet
        TPM00.columns=newCols
        TPM01.columns=newCols
        TPM10.columns=newCols
        TPM11.columns=newCols
        TPM20.columns=newCols
        TPM21.columns=newCols
        TPM22.columns=newCols
        
        # generate the random DataFrame to be used also as output , called proSet
        proSet=pd.DataFrame(np.random.uniform(0,1,TPM00.shape))
        dfTOP=pd.DataFrame(startValuesDW)
        proSet=dfTOP.append(proSet, ignore_index=True)
        dfTOP=pd.DataFrame(startValuesDW, columns=newCols)
        TPM00=dfTOP.append(TPM00, ignore_index=True)
        dfTOP=pd.DataFrame(startValuesDW, columns=newCols)
        TPM01=dfTOP.append(TPM01, ignore_index=True)
        dfTOP=pd.DataFrame(startValuesDW, columns=newCols)
        TPM10=dfTOP.append(TPM10, ignore_index=True)
        dfTOP=pd.DataFrame(startValuesDW, columns=newCols)
        TPM11=dfTOP.append(TPM11, ignore_index=True)
        dfTOP=pd.DataFrame(startValuesDW, columns=newCols)
        TPM20=dfTOP.append(TPM20, ignore_index=True)
        dfTOP=pd.DataFrame(startValuesDW, columns=newCols)
        TPM21=dfTOP.append(TPM21, ignore_index=True)
        dfTOP=pd.DataFrame(startValuesDW, columns=newCols)
        TPM22=dfTOP.append(TPM22, ignore_index=True)
        proSet.columns=TPM22.columns
        for index in range(1441):
            if index>0:
                proSet.iloc[index]=np.where(proSet.iloc[index-1]==0,
                                            np.where(proSet.iloc[index]>TPM00.iloc[index],np.where(proSet.iloc[index]>(TPM00.iloc[index]+TPM01.iloc[index]),2,1),0),
                                            
                                            np.where(proSet.iloc[index-1]==1,
                                            
                                                     np.where(proSet.iloc[index]>TPM11.iloc[index],np.where(proSet.iloc[index]>(TPM10.iloc[index]+TPM11.iloc[index]),2,0),1),
                                                     
                                                     np.where(proSet.iloc[index]>TPM22.iloc[index],np.where(proSet.iloc[index]>TPM22.iloc[index]+TPM21.iloc[index],0,1),2)))#,np.where(proSet.iloc[index-1]==1;np.where(proSet.iloc[index]>TPM11.iloc[index],0,1))

                                                                                                                                                                                                                                                          
        proSet.columns=newCols
        proSet=proSet.iloc[0:-1,:].copy()
        proSet.index=timeIndex
        return proSet
       
    def genATgroupsAdv(self, startDay='01/01/2012', simDays=1):    ###### not used !!!
        sTPM=self.TPM2x2
        daysofWeek=[]
        ATactual=[]
        indexDay=[]
        if isinstance(startDay, basestring)==True: 
            startDay=datetime.date(int(startDay.split("/")[2]),int(startDay.split("/")[1]),int(startDay.split("/")[0]))
        YEAR=str(startDay.year)
        atdf=pd.read_csv(self.recFolder+'AT/AT'+YEAR+'.csv', index_col=0, sep=';', header=[0,1,2,3])
        day0=date(startDay.year,1,1)
        deltaDayStartDay1=startDay-day0
        uniqueATR=self.findUniqueNr(sTPM)
        # df containing later on the mean values of AT, to be used in the diurnal-profile generation grouping on AT
        atdfDiurnal=pd.DataFrame() 
        for dayIndex in range(simDays):
            
            print (startDay+timedelta(days=dayIndex))
            dtSerie = pd.date_range(startDay+timedelta(days=dayIndex),periods=2, freq="min")

            Atemp=atdf.loc[str(dtSerie[0].date()),:][0]
            if dayIndex==0:
                Atemp_Before=atdf.loc[str(dtSerie[0].date()),:][0]
            else: Atemp_Before=atdf.loc[str((dtSerie[0]-timedelta(days=1)).date()),:][0]
            
            ATinterval=self.findShortATrange(Atemp, uniqueATR)
            ATinterval1stepbefore=self.findShortATrange(Atemp_Before, uniqueATR)
            print (ATinterval, ATinterval1stepbefore)
            
            weekDay=dtSerie[0].weekday()
            if weekDay<4 and weekDay>0: 
                dayOfTheWeek="Week"
                daysofWeek.append(dayOfTheWeek)
            if weekDay==4: 
                dayOfTheWeek="Friday"
                daysofWeek.append(dayOfTheWeek)
            if weekDay==5: 
                dayOfTheWeek="Saturday"
                daysofWeek.append(dayOfTheWeek)
            if weekDay==6: 
                dayOfTheWeek="Sunday"
                daysofWeek.append(dayOfTheWeek)
            if weekDay==0: 
                dayOfTheWeek="Monday"
                daysofWeek.append(dayOfTheWeek)
            ATactual.append(ATinterval)
            indexDay.append(startDay+timedelta(days=dayIndex))
        data=np.array([ATactual,np.roll(ATactual,1),daysofWeek]).T
        data[0,1]=data[0,0]
        ATgroups=pd.DataFrame(data,index=indexDay,columns=["ATactual","ATpast","daysofWeek"])
        return ATgroups

    def genATgroups(self, startDay='01/01/2015', simDays=1):
        '''OLD'''

        sTPM=self.TPM2x2
        daysofWeek=[]
        ATactual=[]
        indexDay=[]
        if isinstance(startDay, basestring)==True:
            startDay=datetime.date(int(startDay.split("/")[2]),int(startDay.split("/")[1]),int(startDay.split("/")[0]))
        YEAR=str(startDay.year)
        atdf=pd.read_csv(self.recFolder+'AT/AT'+YEAR+'.csv', index_col=0, sep=';', header=[0,1,2,3])
        day0=date(startDay.year,1,1)
        deltaDayStartDay1=startDay-day0
        uniqueATR=self.findUniqueNr(sTPM)
        # df containing later on the mean values of AT, to be used in the diurnal-profile generation grouping on AT
        atdfDiurnal=pd.DataFrame()
        for dayIndex in range(simDays):

            dtSerie = pd.date_range(startDay+timedelta(days=dayIndex),periods=2, freq="min")

            Atemp=atdf.loc[str(dtSerie[0].date()),:][0]
            if dayIndex==0:
                Atemp_Before=atdf.loc[str(dtSerie[0].date()),:][0]
            else: Atemp_Before=atdf.loc[str((dtSerie[0]-timedelta(days=1)).date()),:][0]

            ATinterval=self.findShortATrange(Atemp, uniqueATR)
            ATinterval1stepbefore=self.findShortATrange(Atemp_Before, uniqueATR)

            weekDay=dtSerie[0].weekday()
            if weekDay<5:
                dayOfTheWeek="Week"
                daysofWeek.append("Week")
            else:
                dayOfTheWeek="Week End"
                daysofWeek.append("Week End")
            ATactual.append(ATinterval)
            indexDay.append(startDay+timedelta(days=dayIndex))
        data=np.array([ATactual,np.roll(ATactual,-1),daysofWeek]).T
        ATgroups=pd.DataFrame(data,index=indexDay,columns=["ATactual","ATpast","daysofWeek"])
        return ATgroups

    def gen_AT_groups(self, atdf=pd.DataFrame()):
        '''
        NEW!!!
        Used to generate AT average groups
        atdf: is taken by the original data into account when building the TPM (atdf=[])

        :return:
        '''

        if atdf.empty:
            atdf=self._dfglob['MD','-','Weather','-','-','AT Daily Average'].resample('D', how = 'mean')
            startDay = self._dfglob.index[0].date()
            endDay   = self._dfglob.index[-1].date()
        else:
            atdf.index = pd.to_datetime(atdf.index.astype(str))
            atdf=atdf['Weather','-','-','AT'].resample('D', how = 'mean')
            startDay = atdf.index[0].date()
            endDay   = atdf.index[-1].date()
        simDays=(endDay - startDay).days + 1

        daysofWeek=[]
        ATactual=[]
        indexDay=[]

        if isinstance(startDay, str)==True:
            startDay=datetime.date(int(startDay.split("/")[2]),int(startDay.split("/")[1]),int(startDay.split("/")[0]))

        YEAR=str(startDay.year)

        day0=date(startDay.year,startDay.month,startDay.day)
        # df containing later on the mean values of AT, to be used in the diurnal-profile generation grouping on AT

        for dayIndex in range(simDays):

            # print startDay+timedelta(days=dayIndex)
            dtSerie = pd.date_range(startDay+timedelta(days=dayIndex),periods=1, freq="min")
            Atemp=atdf.loc[str(dtSerie[0].date())]

            ATinterval=self.findShortATrange_NEW(Atemp)

            weekDay=dtSerie[0].weekday()
            if weekDay<5: 
                daysofWeek.append("Week")
            else: 
                daysofWeek.append("Week End")

            ATactual.append(ATinterval)
            indexDay.append(startDay+timedelta(days=dayIndex))
        data=np.array([ATactual,np.roll(ATactual,1),daysofWeek]).T #todo
        ATgroups=pd.DataFrame(data,index=indexDay,columns=["ATactual","ATpast","daysofWeek"])
        ATgroups.loc[startDay]["ATpast"]=ATgroups.loc[startDay]["ATactual"]
        dates = pd.date_range(day0,periods=60*24*simDays, freq="min")
        self.ATg=ATgroups.reindex(dates,method='nearest')
        self.ATg=self.ATg.iloc[:,:2].copy()
        cols = MultiIndex.from_tuples([("MD","-","Weather","-","-",'GDAAT'),("MD","-","Weather","-","-",'GPDAAT')])
        self.ATg.columns=cols

    def plotDiurnal(self,columns2Plot=idx["ATR", "Standard Diurnal",:,'TPM_00_R',:,:,:,:,:]):    ###### not used !!!
        df=self.Diurnals
        print ("Start diurnal plot...")
        start=time.clock()
        fig, ax = plt.subplots(1, figsize=(16,9))
        tot=time.clock()-start
        df2plot=df.loc[idx[:],columns2Plot]
        ax.plot(df.index, df[columnName], 'g', linewidth=2.0)

        ticks = ax.get_xticks()
        ax.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours=3)), 5))
        ax.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours=3)), 25), minor=True)
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%I:%M %p'))
        ax.legend(frameon=False)
        plt.tight_layout()
        plt.show()
    
    def plotDiurnalNew(self,Building,Entrance,Apartment,Room,columnName, distWWE=True):    ###### not used !!!
        print ("Start diurnal plot...")
        start=time.clock()
        if Apartment<10: df=DataFrame(self._dfglob["MD"]["-"]["B"+str(Building)+"E"+str(Entrance)]["A0"+str(Apartment)]["Room_"+str(Room)][columnName])
        else: df=DataFrame(self._dfglob["MD"]["-"]["B"+str(Building)+"E"+str(Entrance)]["A"+str(Apartment)]["Room_"+str(Room)][columnName])
        df['Time'] = df.index.map(lambda x: x.strftime("%H:%M"))
        df['Time'] = df.index.map(lambda x: x.strftime("%H:%M"))
        self.dataTime = df.groupby('Time').mean()
        self.dataTime.index = pd.to_datetime(self.dataTime.index.astype(str))
        
        fig, ax = plt.subplots(1, figsize=(16,9))
        tot=time.clock()-start
        print ("compiled in:",tot,"seconds")
        
        if  distWWE==False:
            ax.plot(self.dataTime.index, self.dataTime[columnName]['mean'], 'g', linewidth=2.0)
        else:
            temp = pd.DatetimeIndex(df.index)
            df['weekday'] = temp.weekday
            weekdays_only = df[df['weekday'] < 5 ]
            weekenddays_only = df[df['weekday'] > 4 ]
            dataTime = df.groupby('Time').describe().unstack()
            weekdays_only = weekdays_only.groupby('Time').describe().unstack()
            weekenddays_only = weekenddays_only.groupby('Time').describe().unstack()


            dataTime.index = pd.to_datetime(dataTime.index.astype(str))
            weekdays_only.index = pd.to_datetime(weekdays_only.index.astype(str))
            weekenddays_only.index = pd.to_datetime(weekenddays_only.index.astype(str))

            ax.plot(weekdays_only.index, weekdays_only[columnName]['mean'], 'b', label=str(columnName)+" Weekend", linewidth=2.0)
            ax.plot(weekenddays_only.index, weekenddays_only[columnName]['mean'], 'r', label=str(columnName)+" Week",linewidth=2.0)
        
        ticks = ax.get_xticks()
        ax.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours=3)), 5))
        ax.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours=3)), 25), minor=True)
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%I:%M %p'))
        ax.legend(frameon=False)
        plt.tight_layout()
        plt.show()
    
    def plotDiurnalKeys(self,Keys=["B2E1","A01","Room_Children","WP1"], distWWE=True):    ###### not used !!!
        start=time.clock()
        print ("Start diurnal plot...")
        columnName=Keys[3]
        #df=DataFrame(self._dfglob["B"+str(Building)+"E"+str(Entrance)]["A0"+str(Apartment)]["Room_"+str(Room)][columnName])
        df=DataFrame(self._dfglob[Keys[0]][Keys[1]][Keys[2]][Keys[3]])
        df['Time'] = df.index.map(lambda x: x.strftime("%H:%M"))
        #df['Time'] = df.index.map(lambda x: x.strftime("%H:%M"))
        self.dataTime = df.groupby('Time').describe().unstack()
        self.dataTime.index = pd.to_datetime(self.dataTime.index.astype(str))
        
        fig, ax = plt.subplots(1, figsize=(16,9))
        
        
        if  distWWE==False:
            tot=time.clock()-start
            print ("compiled in:",tot,"seconds")
            ax.plot(self.dataTime.index, self.dataTime[columnName]['mean'], 'g', linewidth=2.0)
        else:
            temp = pd.DatetimeIndex(df.index)
            df['weekday'] = temp.weekday
            weekdays_only = df[df['weekday'] < 5 ]
            weekenddays_only = df[df['weekday'] > 4 ]
            dataTime = df.groupby('Time').describe().unstack()
            weekdays_only = weekdays_only.groupby('Time').describe().unstack()
            weekenddays_only = weekenddays_only.groupby('Time').describe().unstack()


            dataTime.index = pd.to_datetime(dataTime.index.astype(str))
            weekdays_only.index = pd.to_datetime(weekdays_only.index.astype(str))
            weekenddays_only.index = pd.to_datetime(weekenddays_only.index.astype(str))
            tot=time.clock()-start
            print ("compiled in:",tot,"seconds")
            ax.plot(weekdays_only.index, weekdays_only[columnName]['mean'], 'b', label=Keys[0]+Keys[1]+Keys[2]+Keys[3]+" Weekend", linewidth=2.0)
            ax.plot(weekenddays_only.index, weekenddays_only[columnName]['mean'], 'r', label=Keys[0]+Keys[1]+Keys[2]+Keys[3]+" Week",linewidth=2.0)
        
        ticks = ax.get_xticks()
        ax.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours=3)), 5))
        ax.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours=3)), 25), minor=True)
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%I:%M %p'))
        ax.legend(frameon=False)
        plt.tight_layout()
        plt.show()
        
        
    def plotDiurnalOld(self,columnName, distWWE=True):    ###### not used !!!
        
        start=time.clock()
        self._dfglob['Time'] = self._dfglob.index.map(lambda x: x.strftime("%H:%M"))
        self.dataTime = self._dfglob.groupby('Time').describe().unstack()
        self.dataTime.index = pd.to_datetime(self.dataTime.index.astype(str))
        
        fig, ax = plt.subplots(1, figsize=(16,9))
        tot=time.clock()-start
        print ("compiled in:",tot,"seconds")
        if  distWWE==False:
            ax.plot(self.dataTime.index, self.dataTime[columnName]['mean'], 'g', linewidth=2.0)
        else:
            temp = pd.DatetimeIndex(self._dfglob.index)
            self._dfglob['weekday'] = temp.weekday
            weekdays_only = self._dfglob[self._dfglob['weekday'] < 5 ]
            weekenddays_only = self._dfglob[self._dfglob['weekday'] > 4 ]
            dataTime = self._dfglob.groupby('Time').describe().unstack()
            weekdays_only = weekdays_only.groupby('Time').describe().unstack()
            weekenddays_only = weekenddays_only.groupby('Time').describe().unstack()


            dataTime.index = pd.to_datetime(dataTime.index.astype(str))
            weekdays_only.index = pd.to_datetime(weekdays_only.index.astype(str))
            weekenddays_only.index = pd.to_datetime(weekenddays_only.index.astype(str))

            ax.plot(weekdays_only.index, weekdays_only[columnName]['mean'], 'b', label=str(columnName)+" Weekend", linewidth=2.0)
            ax.plot(weekenddays_only.index, weekenddays_only[columnName]['mean'], 'r', label=str(columnName)+" Week",linewidth=2.0)
        
        ticks = ax.get_xticks()
        ax.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours=3)), 5))
        ax.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours=3)), 25), minor=True)
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%I:%M %p'))
        plt.tight_layout()
        plt.show()
        
    def _verify_start_and_stop_date(self,date,stepwidth = 1, max_iterations = 120):    ###### not used !!!
        '''
        If the date-Timevector is not in index, the next possible available Index will be used, it will be checked every second for max_iterations
        If no index found, an IndexError is raised.
        
        stop-date will be determined from startdate + stepwidth
        
        input:
            date:    datetime.date[time]object to start from
            [stepwidth]:    In how many days is enddate expected
            [max_iterations]:    How many seconds to look forward before rasing in IndexError
            
        output:
            Two datetime-objects, start and end date that exist in the index
        '''
        if type(date) is datetime.date:
            date = datetime.combine(date,datetime.time(0,0))
        if date in self._dfglob.index:
            start = date
            start_found = True
        else:
            i = 0
            start_found = False
            while i < max_iterations:
                i += 1
                if date + datetime.timedelta(seconds = i) in self._dfglob.index:
                    start = date + datetime.timedelta(seconds = i)
                    start_found = True
                    break
        if start_found is False:
            raise IndexError ('Could not find start-date-Value for %s within %i seconds'%(date.strftime('%Y-%m-%d %H:%M'),max_iterations))
        else:
            end_found = False
            if date + datetime.timedelta(days = stepwidth) in self._dfglob.index:
                end = date + datetime.timedelta(days = stepwidth)
                end_found = True
            else:
                i = 0
                while i < max_iterations:
                    i += 1
                    if date + datetime.timedelta(days = stepwidth,seconds = i) in self._dfglob.index:
                        end = date + datetime.timedelta(days = stepwidth, seconds = i)
                        end_found = True
                        break
        if end_found is False:
            error_out = eval('Could not find end-date-Value for %s within %i seconds'%((start+datetime.timedelta(days = stepwidth)).strftime('%Y-%m-%-d %H:%M'),max_iterations))
            raise IndexError (error_out)
        return start,end   
            
        
    def __calc_rows(self,nop,cols):    ###### not used !!!
        ''' Calculate number of rows necessary to show all plots given the number of columns
        
            Input:  number of plots (int)
                    number of columns (int)
                    
            Output: number of rows (int)
        '''
        assert type(nop) == int and type(cols) == int, 'Expected Input are Integer for nop and cols'
        if nop%cols == 0:
            rows = nop/cols
        else:
            rows = nop/cols + 1
        return rows

    def _get_min_and_max_dates(self):    ###### not used !!!
        ''' Get the Minimum and the maximum Date of the data included
        '''        
        min_date = self._dfglob.index.min().date()
        max_date = self._dfglob.index.max().date()
        return min_date,max_date

mD_gen_WSP = MCM()
mD_gen_TPM = MCM()
mD_gen_VAL = MCM()
mD_gen_PAT = MCM()
mD_val = MCM()
mD_val_2 = MCM()