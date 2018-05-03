# Created: Wed Mar 15 22:08:05 2017
#      by: Lukas Schmitt

import random

from PyQt4 import QtGui, QtCore
from eva_1M import *
from eva_2M import *
from eva_3M import *

from properties.plot_properties import *
from genTMC import *


## in genTMV_05 verschoben
# mD_gen_WSP = MCM()
# mD_val = MCM()
# mD_val_2 = MCM()

class bcolors:
    DEFAULT = '\033[99m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class FFG():
    """
    Functions for GUI
    Main functions: generate, validate and visualize as functions used for executing the programm-tabs
    """

    def __init__(self):
        self.dataset_fieldtests = []
        self.weatherset = ["Field Test South-DE 2012"]
        self.files = []
        self.recFolder=os.getcwd().split("\\src")[0] + "/Data/"
        self.rand_dict2x2 = {}
        self.val_horizon = 1
        self.dataset_models = []
        self.dataset_intervals = []
        self.dataset_levels = []
        self.dataset_rooms = []
        self.dataset_WPs = []
        self.pre_wsp = 0

        filepaths_fieldtests = glob.glob(os.getcwd().split("\\src")[0]
                                         + "/Data/starts" + "/*.csv")
        for filepath in filepaths_fieldtests:
            Building_key = filepath.split("\\")[-1].split("_")[1]
            if Building_key not in self.dataset_fieldtests:
                self.dataset_fieldtests.append(Building_key)

        additional_weatherconditions = glob.glob(os.getcwd().split("\\src")[0] +
                                                 "/Data/AT/additional_AT_files" + "/*.csv")
        for file in additional_weatherconditions:
            self.weatherset.append(file.split("\\")[-1].split(".")[0])

    def get_models(self, building):
        filepaths_profiles = glob.glob(os.getcwd().split("\\src")[0] +
                                       "/Data/diurnals" + "/*.csv")
        for filepath in filepaths_profiles:
            if filepath.split("\\")[-1].split("_")[-2] == building:
                data = pd.read_csv(filepath, sep=";", nrows=7, header=None)
                self.dataset_models = np.unique(data.ix[1, :].tolist()).tolist()
                self.dataset_models = list(filter(
                    lambda x: x not in ["nan", "-"], self.dataset_models))
        return self.dataset_models

    def get_intervals(self, building):
        filepaths_profiles = glob.glob(os.getcwd().split("\\src")[0] +
                                       "/Data/diurnals" + "/*.csv")
        for filepath in filepaths_profiles:
            if filepath.split("\\")[-1].split("_")[-2] == building:
                data = pd.read_csv(filepath, sep=";", nrows=7, header=None)
                self.dataset_intervals = np.unique(data.ix[0, :].tolist()).tolist()
                self.dataset_intervals = list(filter(
                    lambda x: x not in ["nan", "-"], self.dataset_intervals))
        return self.dataset_intervals

    def get_levels(self, file="", building="B2E1"):
        if file != "":
            data = pd.read_csv(file, sep=";", nrows=7, header=None)
            self.dataset_levels = np.unique(data.ix[1, :].tolist()).tolist()
            self.dataset_levels = list(filter(
                lambda x: x not in ["nan", "-"], self.dataset_levels))
        else:
            filepaths_profiles = glob.glob(os.getcwd().split("\\src")[0] +
                                           "/Data/diurnals" + "/*.csv")
            for filepath in filepaths_profiles:
                if filepath.split("\\")[-1].split("_")[-2] == building:
                    data = pd.read_csv(filepath, sep=";", nrows=7)
                    self.dataset_levels = np.unique(data.ix[4, :].tolist()).tolist()
                    self.dataset_levels = list(filter(
                        lambda x: x not in ["nan", "-"], self.dataset_levels))
        return self.dataset_levels

    def get_rooms(self, file="", building="B2E1", level="A01"):
        if file != "":
            data = pd.read_csv(file, sep=";", nrows=7, header=None)
            df_list = zip(data.ix[1, :].tolist(), data.ix[2, :].tolist())
            levels = list(filter(lambda x: x not in ["nan", "-"],
                                 np.unique(data.ix[1, :].tolist()).tolist()))
        else:
            filepaths_profiles = glob.glob(os.getcwd().split("\\src")[0] +
                                           "/Data/diurnals" + "/*.csv")
            for filepath in filepaths_profiles:
                if building == filepath.split("\\")[-1].split("_")[-2]:
                    data = pd.read_csv(filepath, sep=";", nrows=7)
                    df_list = zip(data.ix[4, :].tolist(), data.ix[5, :].tolist())
                    levels = list(filter(lambda x: x not in ["nan", "-"],
                                         np.unique(data.ix[4, :].tolist()).tolist()))
        levels_dict = {}
        for el in levels:
            levels_dict[el] = []
        for index, el in enumerate(df_list):
            if df_list[index][0] in levels_dict and \
                            df_list[index][1] not in levels_dict[df_list[index][0]]:
                levels_dict[df_list[index][0]].append(df_list[index][1])
                levels_dict[df_list[index][0]] = list(
                    filter(lambda x: x not in ["-"], levels_dict[df_list[index][0]]))
        self.dataset_rooms = levels_dict[level]
        return self.dataset_rooms

    def get_WPs (self, file="", building="B2E1", room="Room_Living"):
        if file != "":
            data = pd.read_csv(file, sep=";", nrows=7, header=None)
            df_list = zip(data.ix[2, :].tolist(), data.ix[3, :].tolist())
            rooms = list(filter(lambda x: x not in ["nan", "-"],
                                np.unique(data.ix[2, :].tolist()).tolist()))
        else:
            filepaths_profiles = glob.glob(os.getcwd().split("\\src")[0] +
                                           "/Data/diurnals" + "/*.csv")
            for filepath in filepaths_profiles:
                if filepath.split("\\")[-1].split("_")[-2] == building:
                    data = pd.read_csv(filepath, sep=";", nrows=7)
                    df_list = zip(data.ix[5, :].tolist(), data.ix[6, :].tolist())
                    rooms = list(filter(lambda x: x not in ["nan", "-"],
                                        np.unique(data.ix[5, :].tolist()).tolist()))
        rooms_dict = {}
        for el in rooms:
            rooms_dict[el] = []
        for index, el in enumerate(df_list):
            if df_list[index][0] in rooms_dict and \
                            df_list[index][1] not in rooms_dict[df_list[index][0]]:
                rooms_dict[df_list[index][0]].append(df_list[index][1])
                rooms_dict[df_list[index][0]] = list(
                    filter(lambda x: x not in ["-"], rooms_dict[df_list[index][0]]))
        self.dataset_WPs = rooms_dict[room]
        return self.dataset_WPs

    def show(self,variables=[]):
        for variable in variables:
            if variable.isHidden() == True: variable.show()

    def hide(self, variables=[]):
        for variable in variables:
            if variable.isHidden() == False: variable.hide()

    def show_and_hide(self, variables=[], all_variables=[]):
        for variable in variables:
            if variable.isHidden() == True: variable.show()
        for element in [var for var in all_variables if var not in variables]:
            if element.isHidden() == False: element.hide()

    def fill_lists(self, list, elements):
        list.clear()
        for element in elements:
            item = QtGui.QListWidgetItem(list)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setText(str(element))

    def fill_combobox(self, box, item_list):
        box.clear()
        box.addItems(item_list)

    def return_int(self, button):
        rand = button.value()
        return rand

    def random_func(self, profile_set, random_int):
        group_of_items = profile_set  # a sequence or set will work here.
        list_of_random_items = random.sample(group_of_items, random_int)
        return list_of_random_items

    def return_activated(self, spinbox):
        combobox_activated_value = spinbox.currentText()
        return combobox_activated_value

    def return_path(self, path):
        file = path.text()
        return file

    def return_ckecked_profiles(self, profile_choice_files):
        checked_items = []
        for index in range(profile_choice_files.count()):
            if (profile_choice_files.item(index).checkState()) == 2:  # 2 means "Checked", 0 means "Unchecked"
                checked_items.append(str(profile_choice_files.item(index).text()))
        return checked_items

    def load_pic(self,pic,path):
        pic.setPixmap(QtGui.QPixmap(path))
        pic.setScaledContents(True)

    def defect_sensor_replacing2x2(self, df, level_list):
        self.replace_cols2x2 = [df[column].name for column in df if df[column].sum() == 0]
        # columns (in ATR) that have to be replaced
        self.replace_cols2x2 = [
            val for val in self.replace_cols2x2 if val[0] == "ATR" and val[3] in ["TPM_01_R","TPM_10_R"]]

        # list of appartments with defect data
        self.substitute_appartments2x2 = np.unique([el[5] for el in self.replace_cols2x2])

        # random room out of appartment with complete data
        self.rand_for_appartments2x2 = [
            random.choice([val for val in level_list if val not in self.substitute_appartments2x2])
            for el in self.substitute_appartments2x2]
        self.rand_dict2x2 = dict(zip(self.substitute_appartments2x2, self.rand_for_appartments2x2))

        for column in df:
            if df[column].name[5] in self.substitute_appartments2x2:
                df[column] = df[
                    df[column].name[0], df[column].name[1], df[column].name[2], df[column].name[3], df[column].name[4],
                    self.rand_dict2x2[df[column].name[5]], df[column].name[6], df[column].name[7]]

    def defect_sensor_replacing2x2start(self, df, rand_dict):
        # requires prior execution of defect_sensor_replacing2x2()
        for column in df:
            if df[column].name[5] in self.substitute_appartments2x2:
                df[column] = df[
                    df[column].name[0], df[column].name[1], df[column].name[2], df[column].name[3], df[column].name[4],
                    rand_dict[df[column].name[5]], df[column].name[6], df[column].name[7]]

    def defect_sensor_replacing3x3(self, df, level_list):
        self.replace_cols3x3 = [df[column].name for column in df if df[column].sum() == 0]

        # columns (in ATR) that have to be replaced
        self.replace_cols3x3 = [
            val for val in self.replace_cols3x3
            if val[0] == "ATR" and val[3] in ["TPM_01_R","TPM_10_R","TPM_12_R","TPM_21_R","TPM_20_R","TPM_02_R"]]

        # list of appartments with defect data
        self.substitute_appartments3x3 = np.unique([el[5] for el in self.replace_cols3x3])

        # random room out of appartment with complete data
        self.rand_for_appartments3x3 = [
            random.choice([val for val in level_list
                           if val not in self.substitute_appartments3x3]) for el in self.substitute_appartments3x3]
        self.rand_dict3x3 = dict(zip(self.substitute_appartments3x3, self.rand_for_appartments3x3))

        for column in df:
            if df[column].name[5] in self.substitute_appartments3x3:
                df[column] = df[
                    df[column].name[0], df[column].name[1], df[column].name[2], df[column].name[3], df[column].name[4],
                    self.rand_dict3x3[df[column].name[5]], df[column].name[6], df[column].name[7]]

    def defect_sensor_replacing3x3start(self, df):  # requires prior execution of defect_sensor_replacing3x3()
        for column in df:
            if df[column].name[5] in self.substitute_appartments3x3:
                df[column] = df[
                    df[column].name[0], df[column].name[1], df[column].name[2], df[column].name[3], df[column].name[4],
                    self.rand_dict3x3[df[column].name[5]], df[column].name[6], df[column].name[7]]


    def generate_WSP(self, combobox_dataset, profiles_set, button_spinbox_int, spinbox_int,
                     button_pc_input, button_allprofiles, from_date, to_date, output_path,
                     filename, combobox_weather, button_Select1, button_Select2, button_Select3,
                     booster_button):

        """
        Function gets the dataset, the randomly or personalized choosed profiles,
        the dates and the path to save the generated file
        """

        ## Choose a Field Test
        self.fieldtest = str(self.return_activated(combobox_dataset))

        ## get random profiles
        self.list_profiles = self.random_func(self.dataset_levels,
                                              self.return_int(spinbox_int))  # z.B. ["a","b"]

        ## get choosen profile
        self.profiles_choosen = self.return_ckecked_profiles(profiles_set)  # z.B. ["a","b"]

        ## get weather
        self.weather = self.return_activated(combobox_weather)
        if self.weather == "Field Test South-DE 2012":
            self.weather = "original"
        else:
            self.weather = str(os.getcwd().split("\\src")[0] +
                               "/Data/AT/additional_AT_files/" + self.weather + ".csv")

        ## get dates
        self.date_initial_day = from_date.date().toPyDate()
        self.date_final_day = to_date.date().toPyDate()
        self.simulation_days=(self.date_final_day - self.date_initial_day).days+1

        ## get path
        self.path_profiles = str(self.return_path(output_path)) + \
                             "/proSet_" + str(self.return_path(filename))
        self.path_diurnals = str(self.return_path(output_path)) + \
                             "/diurnals_" + str(self.return_path(filename))

        print bcolors.BOLD + bcolors.DEFAULT + "\nWSP generation started ..."
        print bcolors.DEFAULT

        ### OPTIONS for the GUI
        startDay = date(2012, self.date_initial_day.month, self.date_initial_day.day)
        simDays = self.simulation_days

        ### reading data (to be substituted later in the GUI by the user's inputs)
        if button_Select1.isChecked() == True: model = "M1"
        elif button_Select2.isChecked() == True: model = "M2"
        elif button_Select3.isChecked() == True: model = "M3"

        ### finding out temperature groups of input matrix
        temps = pd.read_csv(
            os.getcwd().split("\\src")[0] + '/Data/TPM/TPM_'+self.fieldtest+'_'+model+'.csv', index_col=0, sep=';',
            header=[0,1,2,3,4,5,6,7],skiprows=[], low_memory=False)
        temperature_ranges = np.unique(temps.loc[:, :].columns.get_level_values(0).tolist()).tolist()
        temperature_ranges = [t_range.split('<DAAT<=') for t_range in temperature_ranges if '<DAAT<=' in t_range]
        temperature_groups = np.sort(np.unique([int(item) for sublist in temperature_ranges for item in sublist]))

        mD_gen_WSP.temperature_groups = temperature_groups  # this should actually be read by the input TPM matrix!!!
        # standard values in the paper are: [5,11,14,18]

        ### for the testing activity:
        recFolder = os.getcwd().split("\\src")[0] + '/Data/'

        mD_gen_WSP.TPM = pd.read_csv(
            recFolder + 'TPM/TPM_'+self.fieldtest+'_'+model+'.csv', index_col=0, sep=';',
            header=[0, 1, 2, 3, 4, 5, 6, 7], skiprows=[], low_memory=False)
        mD_gen_WSP.start = pd.read_csv(
            recFolder + 'starts/starts_'+self.fieldtest+'_'+model+'.csv', index_col=0, sep=';',
            header=[0, 1, 2, 3, 4, 5, 6, 7], skiprows=[], low_memory=False)

        ### finding out temperature groups of input matrix
        temperature_ranges = \
            np.unique(mD_gen_WSP.start.loc[:, :].columns.get_level_values(0).tolist()).tolist()
        temperature_ranges = \
            [t_range.split('<DAAT<=') for t_range in temperature_ranges if '<DAAT<=' in t_range]
        mD_gen_WSP.temperature_groups = \
            np.sort(np.unique([int(item) for sublist in temperature_ranges for item in sublist]))

        ## here the columns that are not used are dropped
        if button_spinbox_int.isChecked() == True:
            mD_gen_WSP.TPM.drop(
                [profile for profile in self.dataset_levels if profile not in self.list_profiles],
                level=5, axis=1, inplace=True)
            mD_gen_WSP.start.drop(
                [profile for profile in self.dataset_levels if profile not in self.list_profiles],
                level=5, axis=1, inplace=True)
        elif button_pc_input.isChecked() == True:
            mD_gen_WSP.TPM.drop(
                [profile for profile in self.dataset_levels if profile not in self.profiles_choosen],
                level=5, axis=1, inplace=True)
            mD_gen_WSP.start.drop(
                [profile for profile in self.dataset_levels if profile not in self.profiles_choosen],
                level=5, axis=1, inplace=True)

        ### can we go for TURBO???
        ### "TURBO" is a faster way to solve the MC faster but is only implemented for 2x2 and 3x3 matrices
        start_positions = [a for a in mD_gen_WSP.TPM.columns.get_level_values(2).values]
        if "['WP2']" in start_positions: self.Turbo = False
        else: self.Turbo = True

        if self.Turbo == True:
            ### preparing TPM for turboboost (use only 2x2 and 3x3 TPMs/starts matrices)
            mD_gen_WSP.split_TPMs_starts()

            # data depending on booster button is checked or not
            if booster_button.isChecked() == True:
                self.defect_sensor_replacing2x2(mD_gen_WSP.TPM2x2, self.dataset_levels)
                self.defect_sensor_replacing3x3(mD_gen_WSP.TPM3x3, self.dataset_levels)
                self.defect_sensor_replacing2x2start(mD_gen_WSP.start2x2, self.rand_dict2x2)
                self.defect_sensor_replacing3x3start(mD_gen_WSP.start3x3)

            # here the columns that are not used should be dropped
            mD_gen_WSP.TPM3x3.sort_index(axis=1, inplace=True)  # .sort(axis=0)
            mD_gen_WSP.start3x3.sort_index(axis=1, inplace=True)# .sort(axis=0)
            mD_gen_WSP.TPM2x2.sort_index(axis=1, inplace=True)  # .sort(axis=0)
            mD_gen_WSP.start2x2.sort_index(axis=1, inplace=True)  # .sort(axis=0)

            ## here the profiles are generated and the status of the function is printed
            initial_day = '{:02d}'.format(from_date.date().toPyDate().day)
            initial_month =  '{:02d}'.format(from_date.date().toPyDate().month)

            if model in ["M1","M2"]:
                mD_gen_WSP.genProfiles(str(initial_day)+"/"+str(initial_month)+"/2012",
                                       simDays, distinguishWWE=False, weather_data=self.weather)
            else:
                mD_gen_WSP.genProfilesDAAT(str(initial_day)+"/"+str(initial_month)+"/2012", simDays,
                                           weather_data=self.weather)

            mD_gen_WSP.proSetDW = mD_gen_WSP.proSetDW.drop('Weather', level=2, axis=1)
            mD_gen_WSP._dfglob = pd.concat([mD_gen_WSP.proSetSW, mD_gen_WSP.proSetDW], axis=1)

            mD_gen_WSP._dfglob.sort_index(axis=1, inplace=True)
            mD_gen_WSP._dfglob = mD_gen_WSP.delColLev(mD_gen_WSP._dfglob, levels=[0, 1])
            mD_gen_WSP._dfglob.to_csv(self.path_profiles, ";")

            mD_gen_WSP.genWPinterlevels()
            mD_gen_WSP._dfglob = mD_gen_WSP.addLevel(mD_gen_WSP._dfglob, ['MD', '-'])

            mD_gen_WSP.genDiurnals(distinguishWWE=False, groups=[5, 11, 14, 18])
            mD_gen_WSP.Diurnals.sort_index(axis=1, inplace=True)
            mD_gen_WSP.Diurnals.to_csv(self.path_diurnals, ";")

        else:
            ### making the TPM ready to be used in the IFM
            ### it aggregates and cumulate the probabilities of each room
            mD_gen_WSP.aggregate_TPM(mD_gen_WSP.TPM, mD_gen_WSP.start)
            # mD_gen_WSP.agg_TPM.to_csv(recFolder+'Cum_Agg_TPM_1.csv',";")

            if self.weather == "original":
                at_df = pd.read_csv(recFolder + 'AT/AT2012.csv', index_col=0, sep=';', header=[0, 1, 2, 3])
            else:
                at_df = pd.read_csv(self.weather, index_col=0, sep=';', header=[0, 1, 2, 3])

            date_index = pd.date_range(startDay, periods=simDays, freq='D')
            mD_gen_WSP.gen_AT_groups(atdf=at_df)  # this generates the ATg, Ambient temperature groups

            if model == "M1":
                mD_gen_WSP.generate_profiles_M1(TPM=mD_gen_WSP.agg_TPM, starts=mD_gen_WSP.agg_starts,
                                                weather_data_year=mD_gen_WSP.ATg.index[0].year,
                                                startDay=startDay, simDays=simDays, Model='M1')
            if model == "M2":
                mD_gen_WSP.generate_profiles_M2(TPM=mD_gen_WSP.agg_TPM, starts=mD_gen_WSP.agg_starts,
                                                weather_data_year=mD_gen_WSP.ATg.index[0].year,
                                                startDay=startDay, simDays=simDays)
            if model == "M3":
                mD_gen_WSP.generate_profiles_M3(TPM=mD_gen_WSP.agg_TPM, starts=mD_gen_WSP.agg_starts,
                                                weather_data_year=mD_gen_WSP.ATg.index[0].year,
                                                startDay=startDay, simDays=simDays)

            ### save profiles to be used e.g. in simultaions
            mD_gen_WSP.gen_profs.sort_index(axis=1, inplace=True)

            #Davides change 31.10 solving output bug without DAT
            at_df_min=at_df.asfreq('1Min', method='pad').copy()
            at_df_min.columns.set_levels(['AT Daily Average'], 3, inplace=True)
            pd.concat([mD_gen_WSP.gen_profs, at_df_min], axis=1, join='inner').to_csv(self.path_profiles, ";")
            # mD_gen_WSP.gen_profs.to_csv(self.path_profiles, ";")


            mD_gen_WSP._dfglob = mD_gen_WSP.gen_profs

            at_df = at_df.reindex(mD_gen_WSP._dfglob.index, method='ffill')
            mD_gen_WSP._dfglob = pd.concat([mD_gen_WSP._dfglob, at_df], axis=1, join="outer")
            # mD_gen_WSP._dfglob.fillna(method='ffill')

            mD_gen_WSP.addLevel(mD_gen_WSP._dfglob, ["MD", "-"])

            ### save diurnal profiles of generated stati, to proove goodness of the profiles

            mD_gen_WSP.genDiurnals(
                distinguishWWE=False, groups=mD_gen_WSP.temperature_groups,
                column2Group=("MD", "-", "Weather", "-", "-", 'AT'))
            mD_gen_WSP.Diurnals.sort_index(axis=1, inplace=True)
            mD_gen_WSP.Diurnals.to_csv(self.path_diurnals, ";")

        print bcolors.BOLD + bcolors.DEFAULT + "\nWSP generation completed !"
        print bcolors.DEFAULT

    def generate_TPM(self, Button_SelectM1_tpm, Button_SelectM2_tpm, Button_SelectM3_tpm,
                    lineEdit_fileselect_tpm, lineEdit_name_tpm, lineEdit_temperatures_tpm, wp_choice):

        """
        Function gets data from Generate_TPM tab and generates the TPM
        """

        print bcolors.BOLD + bcolors.DEFAULT + "\nTPM generation started ..."
        print bcolors.DEFAULT

        self.file = str(lineEdit_fileselect_tpm.text())
        self.name = str(lineEdit_name_tpm.text())
        #self.temperature_ranges = list(np.fromstring(str(lineEdit_temperatures_tpm.text()), sep=","))
        #todo activate after solving problem with TPM generation by equal windows
        id_wins = [] #self.return_ckecked_profiles(wp_choice)

        if Button_SelectM1_tpm.isChecked() == True:
            self.model_TPM = 'M1'
        elif Button_SelectM2_tpm.isChecked() == True:
            self.model_TPM = 'M2'
        elif Button_SelectM3_tpm.isChecked() == True:
            self.model_TPM = 'M3'

        ### OPTIONS for the GUI
        model = self.model_TPM
        temperature_ranges = map(int, list(np.fromstring(str(lineEdit_temperatures_tpm.text()), sep=",")))
        # standard values in the paper are: [5,11,14,18]
        recFolder = os.getcwd().split("\\src")[0] + '/Data/'

        ### Initialaying two MCM classes, one to contain the original data, one to generate the TPM
        mD_measurements = MCM()
        mD_measurements._dfglob = pd.read_csv(
            self.file, index_col=0, sep=';', header=[0, 1, 2, 3],
            skiprows=[], low_memory=False)  # , nrows=14400)

        # avoid missing data problems:
        mD_measurements._dfglob = mD_measurements._dfglob.dropna(axis=0)

        ### generating PAT
        mD_gen_PAT._dfglob = mD_measurements._dfglob.copy()
        mD_gen_PAT._dfglob.index = pd.to_datetime(mD_gen_PAT._dfglob.index, dayfirst=True)

        mD_gen_PAT.genWPinterlevels_general4DAATG()

        mD_gen_PAT.genDailyAverage(round2decimals=0)
        dfAT = mD_gen_PAT.groupByCondensed()

        dfAT.sort_index(axis=1, inplace=True)
        dfAT.to_csv(recFolder + "Position_on_AT/" + self.name + '_PAT.csv', ";")

        mD_gen_TPM._dfglob = mD_measurements._dfglob
        ### ------------------------------------------------------------

        ### elaborate GUI's user's choices
        if model == 'M2':
            WWE_distinctions = True
        else:
            WWE_distinctions = False

        mD_gen_TPM.temperature_groups = temperature_ranges

        ### Transorm index in datetime object index to be able to use all the functions within the genTMC_05
        mD_gen_TPM._dfglob.index = pd.to_datetime(mD_gen_TPM._dfglob.index, dayfirst=True)

        ### generate global TPM
        ### indicating identical windows reduces
        ### the no. of combinations -> the size of the matrix
        ### this generates "df_transiction_matrix"

        mD_gen_TPM.generate_general_state_changes_mx(identical_windows=id_wins)

        ### generate a column for daily average AT
        mD_gen_TPM.genDailyAverage()

        ### add levels to main data matrix
        ### to be able to run the diurnal generation function
        ### which is based on columns in 6 levels
        mD_gen_TPM._dfglob = mD_gen_TPM.addLevel(mD_gen_TPM._dfglob, newLevels=['MD', '-'])

        ### rolling labels to make matrices' lables comparable with each other before concat
        mD_gen_TPM.df_transiction_matrix = mD_gen_TPM.addLevel(mD_gen_TPM.df_transiction_matrix, roll2=-1)

        mD_gen_TPM._dfglob = pd.concat(
            [mD_gen_TPM._dfglob['MD', '-', 'Weather', '-', '-', 'AT Daily Average'],
             mD_gen_TPM.df_transiction_matrix], axis=1, join="outer")

        if model == 'M1':
            ### fill empty rows and complete the day till the end in case a day is only in part present
            start = mD_measurements._dfglob.index.min().date()
            end = mD_measurements._dfglob.index.max().date() + pd.Timedelta(1, 'D')
            mD_measurements._dfglob = mD_measurements._dfglob.reindex(pd.date_range(start, end, freq='T', closed='left')).fillna(method='ffill')
            ### generate diurnals for field evaluatio / validation data
            mD_measurements._dfglob.index = pd.to_datetime(mD_measurements._dfglob.index, dayfirst=True)
            mD_measurements.genDailyAverage()
            mD_measurements._dfglob = mD_measurements.addLevel(mD_measurements._dfglob,
                                                               newLevels=['MD', '-'])
            mD_measurements.genDiurnals(groups=temperature_ranges, distinguishWWE=WWE_distinctions)
            mD_measurements.Diurnals.to_csv(recFolder + 'diurnals/Diurnals_Original_data_'
                                            + self.name + '_' + model + '.csv', ";")

            ### generate diurnals to compute probabilities
            mD_gen_TPM.genDiurnals_NewCode(groups=temperature_ranges, distinguishWWE=WWE_distinctions)

            ### cleaning matrix from AT Daily Average Columns
            mD_gen_TPM.Diurnals.sort_index(axis=1, inplace=True)
            mD_gen_TPM.Diurnals = mD_gen_TPM.Diurnals.loc[idx[:], idx[:, :, :, :, :, :, :, 'TPM']]

            ### Generating start probabilities stati and
            ### Normalizing probabilities
            mD_gen_TPM.compute_trans_probs()  #
            #if temperature_ranges != []:
            #    mD_gen_TPM.starts_probs = mD_gen_TPM.starts_probs.iloc[:,
            #                              mD_gen_TPM.starts_probs.columns.get_level_values(0) != "ATR"]
            mD_gen_TPM.starts_probs.to_csv(recFolder + 'starts/starts_' + self.name + '_' + model + '.csv', ";")

            ### saving into the right place
            mD_gen_TPM.Diurnals.to_csv(recFolder + 'TPM/TPM_' + self.name + '_' + model + '.csv', ";")

        if model == 'M2':
            ### fill empty rows and complete the day till the end in case a day is only in part present
            start = mD_measurements._dfglob.index.min().date()
            end = mD_measurements._dfglob.index.max().date() + pd.Timedelta(1, 'D')
            mD_measurements._dfglob = mD_measurements._dfglob.reindex(pd.date_range(start, end, freq='T', closed='left')).fillna(method='ffill')
            ### generate diurnals for field evaluatio / validation data
            mD_measurements._dfglob.index = pd.to_datetime(mD_measurements._dfglob.index, dayfirst=True)
            mD_measurements.genDailyAverage()
            mD_measurements._dfglob = mD_measurements.addLevel(mD_measurements._dfglob, newLevels=['MD', '-'])
            mD_measurements.genDiurnals(groups=temperature_ranges, distinguishWWE=WWE_distinctions)
            mD_measurements.Diurnals.to_csv(recFolder + 'diurnals/Diurnals_Original_data_' +
                                            self.name + '_'  + model + '.csv', ";")

            ### generate diurnals to compute probabilities
            mD_gen_TPM.genDiurnals_NewCode(groups=temperature_ranges, distinguishWWE=WWE_distinctions)

            ### cleaning matrix from AT Daily Average Columns
            mD_gen_TPM.Diurnals.sort_index(axis=1, inplace=True)
            mD_gen_TPM.Diurnals = mD_gen_TPM.Diurnals.loc[idx[:], idx[:, :, :, :, :, :, :, 'TPM']]

            ### Generating start probabilities stati and
            ### Normalizing probabilities
            mD_gen_TPM.compute_trans_probs()

            mD_gen_TPM.starts_probs.to_csv(recFolder + 'starts/starts_' + self.name + '_' + model + '.csv', ";")

            ### saving into the right place
            mD_gen_TPM.Diurnals.to_csv(recFolder + 'TPM/TPM_' + self.name + '_' + model + '.csv', ";")

        if model == 'M3':
            ### fill empty rows and complete the day till the end in case a day is only in part present
            start = mD_measurements._dfglob.index.min().date()
            end = mD_measurements._dfglob.index.max().date() + pd.Timedelta(1, 'D')
            mD_measurements._dfglob = mD_measurements._dfglob.reindex(pd.date_range(start, end, freq='T', closed='left')).fillna(method='ffill')
            ### generate diurnals for field evaluatio / validation data
            mD_measurements._dfglob.index = pd.to_datetime(mD_measurements._dfglob.index, dayfirst=True)
            mD_measurements.genDailyAverage()
            mD_measurements._dfglob = mD_measurements.addLevel(mD_measurements._dfglob, newLevels=['MD', '-'])
            mD_measurements.genDiurnals(groups=temperature_ranges, distinguishWWE=WWE_distinctions)
            mD_measurements.Diurnals.to_csv(recFolder + 'diurnals/Diurnals_Original_data_' +
                                            self.name + '_' + model + '.csv', ";")

            if temperature_ranges == []:
                print("No groups selected!!!! Model 3 makes no sense at all!")  # GUI give a warning
                ### GUI: Lukas, please make an error pop up if this appens!

            # generate a matrix containing, minute-wise, the temperature range
            # todo: minute wise? why? we should eventually change this later on
            mD_gen_TPM.gen_AT_groups()
            ### generate diurnals to compute probabilities
            mD_gen_TPM.genDiurnalsDAAT(mD_gen_TPM._dfglob)

            ### cleaning matrix from AT Daily Average Columns
            mD_gen_TPM.Diurnals.sort_index(axis=1, inplace=True)
            mD_gen_TPM.Diurnals = mD_gen_TPM.Diurnals.loc[idx[:], idx[:, :, :, :, :, :, :, 'TPM']]

            ### making a pure M3 TPM, deleting columns not needed
            # mD_gen_TPM.Diurnals = mD_gen_TPM.Diurnals.iloc[:,
            #                       mD_gen_TPM.Diurnals.columns.get_level_values(0) != "ATR"]

            ### Normalizing probabilities
            mD_gen_TPM.compute_trans_probs()
            #mD_gen_TPM.starts_probs = mD_gen_TPM.starts_probs.iloc[:,
            #                          mD_gen_TPM.starts_probs.columns.get_level_values(0) != "ATR"]
            mD_gen_TPM.starts_probs.to_csv(recFolder + 'starts/starts_' + self.name + '_' + model + '.csv', ";")

            mD_gen_TPM.Diurnals.to_csv(recFolder + 'TPM/TPM_' + self.name + '_' + model + '.csv', ";")


        mD_gen_TPM.check_tpm = 0
        print bcolors.BOLD + bcolors.DEFAULT + "\nTPM generation completed !"
        print bcolors.DEFAULT

    def validate(self, combobox_dataset, profiles_set, button_spinbox_int, spinbox_int,
                 button_pc_input, button_allprofiles, combobox_weather, button_Select1,
                 button_Select2, button_Select3, integer_number_horizon):

        """
        Function gets the dataset, the randomly or personalized choosed profiles,
        the number of years and the path for the validation file
        """

        ## Choose a Field Test
        self.fieldtest = str(self.return_activated(combobox_dataset))

        ## get random profiles
        self.list_profiles = self.random_func(self.dataset_levels, self.return_int(spinbox_int))  # z.B. ["a","b"]

        ## get choosen profile
        self.profiles_choosen = self.return_ckecked_profiles(profiles_set)  # z.B. ["a","b"]

        ## get weather
        self.weather = self.return_activated(combobox_weather)
        if self.weather == "Field Test South-DE 2012":
            self.weather = "original"
            year = 2012
        else:
            self.weather = str(os.getcwd().split("\\src")[0] +
                               "/Data/AT/additional_AT_files/" + self.weather + ".csv")
            year = int(self.weather.split("_")[-2].split("TRY")[1])

        ## get validation horizon (number of years)
        self.val_horizon = int(self.return_int(integer_number_horizon))
        mD_gen_VAL.val_horizon = self.val_horizon

        print bcolors.BOLD + bcolors.DEFAULT + "\nValidation started ..."
        print bcolors.DEFAULT

        ### reading data (to be substituted later in the GUI by the user's inputs)
        if button_Select1.isChecked() == True: model = "M1"
        elif button_Select2.isChecked() == True: model = "M2"
        elif button_Select3.isChecked() == True: model = "M3"

        ### OPTIONS for the GUI
        validation_duration = self.val_horizon
        if calendar.isleap(year)==True: simDays=365
        else: simDays=366

        ### finding out temperature groups of input matrix
        temps = pd.read_csv(
            os.getcwd().split("\\src")[0] + '/Data/TPM/TPM_' + self.fieldtest + '_' + model + '.csv',
            index_col=0, sep=';', header=[0, 1, 2, 3, 4, 5, 6, 7], skiprows=[], low_memory=False)
        temperature_ranges = np.unique(temps.loc[:, :].columns.get_level_values(0).tolist()).tolist()
        temperature_ranges = [t_range.split('<DAAT<=') for t_range in temperature_ranges if '<DAAT<=' in t_range]
        temperature_groups = np.sort(np.unique([int(item) for sublist in temperature_ranges for item in sublist]))

        mD_gen_VAL.temperature_groups = temperature_groups
        # standard values in the paper are: [5,11,14,18]

        ### for the testing activity:
        recFolder = os.getcwd().split("\\src")[0] + '/Data/'

        mD_gen_VAL.TPM = pd.read_csv(
            recFolder + 'TPM/TPM_' + self.fieldtest + '_' + model + '.csv', index_col=0, sep=';',
            header=[0, 1, 2, 3, 4, 5, 6, 7], skiprows=[], low_memory=False)
        mD_gen_VAL.start = pd.read_csv(
            recFolder + 'starts/starts_' + self.fieldtest + '_' + model + '.csv', index_col=0, sep=';',
            header=[0, 1, 2, 3, 4, 5, 6, 7], skiprows=[], low_memory=False)

        ### finding out temperature groups of input matrix
        temperature_ranges = np.unique(mD_gen_VAL.start.loc[:, :].columns.get_level_values(0).tolist()).tolist()
        temperature_ranges = [t_range.split('<DAAT<=') for t_range in temperature_ranges if '<DAAT<=' in t_range]
        mD_gen_VAL.temperature_groups = np.sort(
            np.unique([int(item) for sublist in temperature_ranges for item in sublist]))

        ## here the columns that are not used are dropped
        if button_spinbox_int.isChecked() == True:
            mD_gen_VAL.TPM.drop(
                [profile for profile in self.dataset_levels if profile not in self.list_profiles],
                level=5, axis=1, inplace=True)
            mD_gen_VAL.start.drop(
                [profile for profile in self.dataset_levels if profile not in self.list_profiles],
                level=5, axis=1, inplace=True)
        elif button_pc_input.isChecked() == True:
            mD_gen_VAL.TPM.drop(
                [profile for profile in self.dataset_levels if profile not in self.profiles_choosen],
                level=5, axis=1, inplace=True)
            mD_gen_VAL.start.drop(
                [profile for profile in self.dataset_levels if profile not in self.profiles_choosen],
                level=5, axis=1, inplace=True)

        ### can we go for TURBO???
        start_positions = [a for a in mD_gen_VAL.TPM.columns.get_level_values(2).values]
        if "['WP2']" in start_positions:
            self.Turbo = False
        else:
            self.Turbo = True

        if self.Turbo == True:
            ### preparing TPM for turboboost (use only 2x2 and 3x3 TPMs/starts matrices)
            mD_gen_VAL.split_TPMs_starts()

            # here the columns that are not used should be dropped
            mD_gen_VAL.TPM3x3.sort_index(axis=1, inplace=True)  # .sort(axis=0)
            mD_gen_VAL.start3x3.sort_index(axis=1, inplace=True)  # .sort(axis=0)
            mD_gen_VAL.TPM2x2.sort_index(axis=1, inplace=True)  # .sort(axis=0)
            mD_gen_VAL.start2x2.sort_index(axis=1, inplace=True)  # .sort(axis=0)

            for sim_year in xrange(validation_duration):
                if model in ["M1", "M2"]:
                    mD_gen_VAL.genProfiles("01/01/2012", simDays,
                                           distinguishWWE=False, weather_data=self.weather)
                else:
                    mD_gen_VAL.genProfilesDAAT("01/01/2012", simDays, weather_data=self.weather)
                mD_gen_VAL.proSetDW = mD_gen_VAL.proSetDW.drop('Weather', level=2, axis=1)
                mD_gen_VAL._dfglob = pd.concat([mD_gen_VAL.proSetSW, mD_gen_VAL.proSetDW], axis=1)

                mD_gen_VAL._dfglob.to_csv(
                    os.getcwd().split("\\src")[0] + "/Data/validation/profiles/validation_pro_" +
                    self.fieldtest + "_" + model + "_" + str(validation_duration) + "-" + str(sim_year+1) +
                    ".csv", ";")

                mD_gen_VAL._dfglob = mD_gen_VAL.delColLev(mD_gen_VAL._dfglob, levels=[0, 1])
                mD_gen_VAL.genWPinterlevels()
                mD_gen_VAL._dfglob = mD_gen_VAL.addLevel(mD_gen_VAL._dfglob, ['MD', '-'])

                mD_gen_VAL.genDiurnals(distinguishWWE=False, groups=[5, 11, 14, 18])
                mD_gen_VAL.Diurnals.sort_index(axis=1, inplace=True)
                mD_gen_VAL.Diurnals.to_csv(
                    os.getcwd().split("\\src")[0] + "/Data/validation/diurnals/validation_diurnals_" +
                    self.fieldtest + "_" + model + "_" + str(validation_duration) + "-" + str(sim_year+1) +
                    ".csv", ";")

        else:
            for mD_gen_VAL.sim_year in xrange(validation_duration):
                ### making the TPM ready to be used in the IFM
                ### it aggregates and cumulate the probabilities of each room
                mD_gen_VAL.aggregate_TPM(mD_gen_VAL.TPM, mD_gen_VAL.start)
                # mD_gen_VAL.agg_TPM.to_csv(recFolder+'Cum_Agg_TPM_1.csv',";")

                if self.weather == "original":
                    at_df = pd.read_csv(recFolder + 'AT/AT2012.csv', index_col=0, sep=';', header=[0, 1, 2, 3])
                else:
                    at_df = pd.read_csv(self.weather, index_col=0, sep=';', header=[0, 1, 2, 3])

                date_index = pd.date_range("01/01/2012", periods=simDays, freq='D')
                mD_gen_VAL.gen_AT_groups(atdf=at_df)  # this generates the ATg, Ambient temperature groups

                if model == "M1": mD_gen_VAL.generate_profiles_M1(
                    TPM=mD_gen_VAL.agg_TPM, starts=mD_gen_VAL.agg_starts,
                    weather_data_year=mD_gen_VAL.ATg.index[0].year, startDay="01/01/2012",
                    simDays=simDays, Model='M1')
                if model == "M2": mD_gen_VAL.generate_profiles_M2(
                    TPM=mD_gen_VAL.agg_TPM, starts=mD_gen_VAL.agg_starts,
                    weather_data_year=mD_gen_VAL.ATg.index[0].year, startDay="01/01/2012",
                    simDays=simDays)
                if model == "M3": mD_gen_VAL.generate_profiles_M3(
                    TPM=mD_gen_VAL.agg_TPM, starts=mD_gen_VAL.agg_starts,
                    weather_data_year=mD_gen_VAL.ATg.index[0].year,
                    startDay="01/01/2012", simDays=simDays)

                ### save profiles to be used e.g. in simultaions
                mD_gen_VAL.gen_profs.to_csv(
                    os.getcwd().split("\\src")[0] + "/Data/validation/profiles/validation_pro_" +
                    self.fieldtest + "_" + model + "_" + str(validation_duration) + "-" +
                    str(mD_gen_VAL.sim_year+1) + ".csv", ";")
                mD_gen_VAL._dfglob = mD_gen_VAL.gen_profs

                at_df = at_df.reindex(mD_gen_VAL._dfglob.index, method='ffill')
                mD_gen_VAL._dfglob = pd.concat([mD_gen_VAL._dfglob, at_df], axis=1, join="outer")
                # mD_gen_VAL._dfglob.fillna(method='ffill')

                mD_gen_VAL.addLevel(mD_gen_VAL._dfglob, ["MD", "-"])

                ### save diurnal profiles of generated stati, to proove goodness of the profiles
                mD_gen_VAL.genDiurnals(distinguishWWE=False, groups=mD_gen_VAL.temperature_groups,
                                       column2Group=("MD", "-", "Weather", "-", "-", 'AT'))
                mD_gen_VAL.Diurnals.sort_index(axis=1, inplace=True)
                mD_gen_VAL.Diurnals.to_csv(
                    os.getcwd().split("\\src")[0] + "/Data/validation/diurnals/validation_diurnals_" +
                    self.fieldtest + "_" + model + "_" + str(validation_duration) + "-" +
                    str(mD_gen_VAL.sim_year+1) + ".csv", ";")

        #todo: brauchen wir das noch?
        # if button_Select1.isChecked() == True:
        #     check_validation_eva1(building=self.fieldtest, recFolder=os.getcwd().split("\\src")[0]+
        # "/Data/", apartments=self.listapartments, years=self.val_horizon)
        # elif button_Select2.isChecked() == True:
        #     check_validation_eva2(building=self.fieldtest, recFolder=os.getcwd().split("\\src")[0]+
        # "/Data/", apartments=self.listapartments, years=self.val_horizon)
        # elif button_Select3.isChecked() == True:
        #     check_validation_eva3(building=self.fieldtest, recFolder=os.getcwd().split("\\src")[0]+
        # "/Data/", apartments=self.listapartments, years=self.val_horizon)

        print bcolors.BOLD + bcolors.DEFAULT + "\nValidation completed !"
        print bcolors.DEFAULT


    def visualize(self, Button_dia1, Button_dia2, Button_dia3, checkbox_std, building_comparison,
                  level_comparison, room_comparison, list_fieldtest_choice, building_combobox, allData,
                  list_levels, level_combobox, allLevels, list_rooms, allRooms, rooms_combobox,
                  WP_combobox, list_intervals, allIntervals, lineEdit_load_profile, model_combobox,
                  level_combobox_profiles, rooms_combobox_profiles, WP_combobox_profiles):
        """
        Function gets the dataset, the choosed profile and the room to visualize the data
        """

        if Button_dia1.isChecked() == True:
            ## Choose comparison
            # Building comparison
            if building_comparison.isChecked() == True:
                # get data
                if allData.isChecked() == True:
                    fieldtests = self.dataset_fieldtests
                else:
                    fieldtests = self.return_ckecked_profiles(list_fieldtest_choice)
                df_list = [
                    pd.read_csv(filepath, index_col=0, sep=';', header=[0, 1, 2, 3, 4], skiprows=[5], low_memory=False)
                    for filepath in glob.glob(os.getcwd().split("\\src")[0] + "/Data/Position_on_AT" + "/*.csv")]
                names = [filepath.split("\\")[-1].split("_")[0]
                         for filepath in glob.glob(os.getcwd().split("\\src")[0] + "/Data/Position_on_AT" + "/*.csv")]
                ft_dict = dict(zip(names, df_list))
                fieldtests = [ft_dict[el] for el in fieldtests]
                plotAll(dfs=fieldtests, level3="WP1", showplot=True, savepng=False, savepdf=False,
                        colors_set=rwth_main_colors, markers_set=wpg_markers,
                        print_std=checkbox_std.isChecked(), alphas=[])

            # level comparison
            elif level_comparison.isChecked() == True:
                # get data
                building = str(self.return_activated(building_combobox))
                df_list = [
                    pd.read_csv(filepath, index_col=0, sep=';', header=[0, 1, 2, 3, 4], skiprows=[5], low_memory=False)
                    for filepath in glob.glob(os.getcwd().split("\\src")[0] + "/Data/Position_on_AT" + "/*.csv")]
                names = [filepath.split("\\")[-1].split("_")[0]
                         for filepath in glob.glob(os.getcwd().split("\\src")[0] + "/Data/Position_on_AT" + "/*.csv")]
                ft_dict = dict(zip(names, df_list))
                building = [ft_dict[building]]
                if allLevels.isChecked() == True:
                    levels = self.dataset_levels
                else:
                    levels = self.return_ckecked_profiles(list_levels)
                plotAll(dfs=building, level1=levels, level3="WP1", showplot=True, savepng=False,
                        savepdf=False, colors_set=rwth_main_colors, markers_set=wpg_markers,
                        print_std=checkbox_std.isChecked(), alphas=[])

            # room comparison
            elif room_comparison.isChecked() == True:
                # get data
                building = str(self.return_activated(building_combobox))
                df_list = [
                    pd.read_csv(filepath, index_col=0, sep=';', header=[0, 1, 2, 3, 4], skiprows=[5], low_memory=False)
                    for filepath in glob.glob(os.getcwd().split("\\src")[0] + "/Data/Position_on_AT" + "/*.csv")]
                names = [filepath.split("\\")[-1].split("_")[0]
                         for filepath in glob.glob(os.getcwd().split("\\src")[0] + "/Data/Position_on_AT" + "/*.csv")]
                ft_dict = dict(zip(names, df_list))
                building = [ft_dict[building]]
                level = [str(self.return_activated(level_combobox))]
                if allRooms.isChecked() == True:
                    rooms = self.dataset_rooms
                else:
                    rooms = self.return_ckecked_profiles(list_rooms)
                plotAll(dfs=building, level1=level, level2=rooms, level3="WP1", showplot=True, savepng=False,
                        savepdf=False, colors_set=rwth_main_colors, markers_set=wpg_markers,
                        print_std=checkbox_std.isChecked(), alphas=[])

        elif Button_dia2.isChecked() == True:
            if allIntervals.isChecked() == True:
                intervals = self.dataset_intervals
            else:
                intervals = self.return_ckecked_profiles(list_intervals)
            plotDiurnal_RW(building=str(self.return_activated(building_combobox)), level0=intervals,
                           level1=str(self.return_activated(model_combobox)),
                           level2=str(self.return_activated(building_combobox)),
                           level3=str(self.return_activated(level_combobox)),
                           level4=str(self.return_activated(rooms_combobox)),
                           level5=str(self.return_activated(WP_combobox)),
                           savingFolder='', set_temp_range='14 < AT Daily Average <= 18', color=rwth_maygreen,
                           showplot=True, savepng=False, savepdf=False)

        elif Button_dia3.isChecked() == True:
            plot_genpro(pd.read_csv(str(lineEdit_load_profile.text()), index_col=0, sep=';',
                                    header=[0,1,2,3], skiprows=[6],  parse_dates=True,low_memory=False),
                                    # level0=str(lineEdit_load_profile.text()).split("/")[-1].split("_")[2],#BUG this was a bug
                                    level1=str(self.return_activated(level_combobox_profiles)),
                                    level2=str(self.return_activated(rooms_combobox_profiles)),
                                    level3=str(self.return_activated(WP_combobox_profiles)),
                                    savingFolder='', showplot=True, savepng=False, savepdf=False)


    def save_plot(self, Button_dia1, Button_dia2, Button_dia3, checkbox_std, building_comparison,
                  level_comparison, room_comparison, list_fieldtest_choice, building_combobox, allData,
                  list_levels, level_combobox, allLevels, list_rooms, allRooms, rooms_combobox,
                  WP_combobox, list_intervals, allIntervals, lineEdit_load_profile, lineEdit_Vis, model_combobox,
                  level_combobox_profiles, rooms_combobox_profiles, WP_combobox_profiles):

        """
        Function gets the dataset, the choosed profile and the room to save the plot
        """

        file_format = str(lineEdit_Vis.text()).split(".")[-1]

        if Button_dia1.isChecked() == True:
            ## Choose comparison
            # Building comparison
            if building_comparison.isChecked() == True:
                # get data
                if allData.isChecked() == True:
                    fieldtests = self.dataset_fieldtests
                else:
                    fieldtests = self.return_ckecked_profiles(list_fieldtest_choice)
                df_list = [
                    pd.read_csv(filepath, index_col=0, sep=';', header=[0, 1, 2, 3, 4], skiprows=[5], low_memory=False)
                    for filepath in glob.glob(os.getcwd().split("\\src")[0] + "/Data/Position_on_AT" + "/*.csv")]
                names = [filepath.split("\\")[-1].split("_")[0]
                         for filepath in glob.glob(os.getcwd().split("\\src")[0] + "/Data/Position_on_AT" + "/*.csv")]
                ft_dict = dict(zip(names, df_list))
                fieldtests = [ft_dict[el] for el in fieldtests]
                plotAll(dfs=fieldtests, level3="WP1", showplot=False, savepng=(file_format=="png"),
                        savepdf=(file_format=="pdf"), colors_set=rwth_main_colors, markers_set=wpg_markers,
                        print_std=checkbox_std.isChecked(), alphas=[], save2=str(lineEdit_Vis.text()))

            # level comparison
            elif level_comparison.isChecked() == True:
                # get data
                building = str(self.return_activated(building_combobox))
                df_list = [
                    pd.read_csv(filepath, index_col=0, sep=';', header=[0, 1, 2, 3, 4], skiprows=[5], low_memory=False)
                    for filepath in glob.glob(os.getcwd().split("\\src")[0] + "/Data/Position_on_AT" + "/*.csv")]
                names = [filepath.split("\\")[-1].split("_")[0]
                         for filepath in glob.glob(os.getcwd().split("\\src")[0] + "/Data/Position_on_AT" + "/*.csv")]
                ft_dict = dict(zip(names, df_list))
                building = [ft_dict[building]]
                if allLevels.isChecked() == True:
                    levels = self.dataset_levels
                else:
                    levels = self.return_ckecked_profiles(list_levels)
                plotAll(dfs=building, level1=levels, level3="WP1", showplot=False, savepng=(file_format=="png"),
                        savepdf=(file_format=="pdf"), colors_set=rwth_main_colors, markers_set=wpg_markers,
                        print_std=checkbox_std.isChecked(), alphas=[], save2=str(lineEdit_Vis.text()))

            # room comparison
            elif room_comparison.isChecked() == True:
                # get data
                building = str(self.return_activated(building_combobox))
                df_list = [
                    pd.read_csv(filepath, index_col=0, sep=';', header=[0, 1, 2, 3, 4], skiprows=[5], low_memory=False)
                    for filepath in glob.glob(os.getcwd().split("\\src")[0] + "/Data/Position_on_AT" + "/*.csv")]
                names = [filepath.split("\\")[-1].split("_")[0]
                         for filepath in glob.glob(os.getcwd().split("\\src")[0] + "/Data/Position_on_AT" + "/*.csv")]
                ft_dict = dict(zip(names, df_list))
                building = [ft_dict[building]]
                level = [str(self.return_activated(level_combobox))]
                if allRooms.isChecked() == True:
                    rooms = self.dataset_rooms
                else:
                    rooms = self.return_ckecked_profiles(list_rooms)
                plotAll(dfs=building, level1=level, level2=rooms, level3="WP1", showplot=False,
                        savepng=(file_format=="png"), savepdf=(file_format=="pdf"), colors_set=rwth_main_colors,
                        markers_set=wpg_markers, print_std=checkbox_std.isChecked(),
                        alphas=[], save2=str(lineEdit_Vis.text()))

        elif Button_dia2.isChecked() == True:
            if allIntervals.isChecked() == True:
                intervals = self.dataset_intervals
            else:
                intervals = self.return_ckecked_profiles(list_intervals)
            plotDiurnal_RW(building=str(self.return_activated(building_combobox)), level0=intervals,
                           level1=str(self.return_activated(model_combobox)),
                           level2=str(self.return_activated(building_combobox)),
                           level3=str(self.return_activated(level_combobox)),
                           level4=str(self.return_activated(rooms_combobox)),
                           level5=str(self.return_activated(WP_combobox)), savingFolder=str(lineEdit_Vis.text()),
                           set_temp_range='14 < AT Daily Average <= 18', color=rwth_maygreen, showplot=False,
                           savepng=(file_format == "png"), savepdf=(file_format == "pdf"))

        elif Button_dia3.isChecked() == True:
            plot_genpro(pd.read_csv(str(lineEdit_load_profile.text()), index_col=0, sep=';',
                        header=[0,1,2,3],skiprows=[6],  parse_dates=True,low_memory=False),
                        level0=str(lineEdit_load_profile.text()).split("/")[-1].split("_")[2],
                        level1=str(self.return_activated(level_combobox_profiles)),
                        level2=str(self.return_activated(rooms_combobox_profiles)),
                        level3=str(self.return_activated(WP_combobox_profiles)),
                        savingFolder=str(lineEdit_Vis.text()), showplot=False, savepng=(file_format=="png"),
                        savepdf=(file_format=="pdf"))