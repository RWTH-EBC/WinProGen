'''
WinProGen GUI
Created: Wed Mar 15 22:08:05 2017
GUI created by: Lukas Schmitt
WinProGen software created by Davide Cali
'''
import pandas
import shutil
import FileDialog
from PyQt4.Qt import *
from src.gui_functions import *

MC = FFG()

### stylesheets
#QToolTip
style_tooltip = """QToolTip {
                   background-color: #003a66; 
                   color: white;
                   border: black solid 1px
                   }
                   """
#QPushButton and QToolTip
style_button_and_tooltip = """QToolTip {
                               background-color: #003a66; 
                               color: white; 
                               border: black solid 1px
                               }
                               QPushButton {
                               background-color: #0063b1;
                               color: white
                               }
                               """

class CheckableComboBox(QtGui.QComboBox):
    """
    Checkable Combobox widget
    """
    def __init__(self):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)

class Worker_Generate_WSP(QtCore.QRunnable):
    """
    Outsourcing the generate WSP function, after started
    """
    def __init__(self, Data_Choice_combobox, profile_choice_files, Button_RandomChoice, int_random_files,
                 Button_ProfileChoice, Button_allProfiles, startDate, finalDate,lineEdit_path, lineEdit_filename,
                 TRY_Choice_combobox, Button_SelectM1, Button_SelectM2, Button_SelectM3, substitute_button):
        super(Worker_Generate_WSP, self).__init__()
        self.Data_Choice_combobox = Data_Choice_combobox
        self.profile_choice_files = profile_choice_files
        self.Button_RandomChoice = Button_RandomChoice
        self.int_random_files = int_random_files
        self.Button_ProfileChoice = Button_ProfileChoice
        self.Button_allProfiles = Button_allProfiles
        self.startDate = startDate
        self.finalDate = finalDate
        self.lineEdit_path = lineEdit_path
        self.lineEdit_filename = lineEdit_filename
        self.TRY_Choice_combobox = TRY_Choice_combobox
        self.Button_SelectM1 = Button_SelectM1
        self.Button_SelectM2 = Button_SelectM2
        self.Button_SelectM3 = Button_SelectM3
        self.substitute_button = substitute_button

    def run(self):
        MC.generate_WSP(self.Data_Choice_combobox,
                        self.profile_choice_files,
                        self.Button_RandomChoice,
                        self.int_random_files,
                        self.Button_ProfileChoice,
                        self.Button_allProfiles,
                        self.startDate,
                        self.finalDate,
                        self.lineEdit_path,
                        self.lineEdit_filename,
                        self.TRY_Choice_combobox,
                        self.Button_SelectM1,
                        self.Button_SelectM2,
                        self.Button_SelectM3,
                        self.substitute_button)

class Worker_Generate_TPM(QtCore.QRunnable):
    """
    Outsourcing the generate TPM function, after started
    """
    def __init__(self, Button_SelectM1_tpm, Button_SelectM2_tpm, Button_SelectM3_tpm,
                    lineEdit_fileselect_tpm, lineEdit_name_tpm, lineEdit_temperatures_tpm, wp_choice):
        super(Worker_Generate_TPM, self).__init__()
        self.Button_SelectM1_tpm = Button_SelectM1_tpm
        self.Button_SelectM2_tpm = Button_SelectM2_tpm
        self.Button_SelectM3_tpm = Button_SelectM3_tpm
        self.lineEdit_fileselect_tpm = lineEdit_fileselect_tpm
        self.lineEdit_name_tpm = lineEdit_name_tpm
        self.lineEdit_temperatures_tpm = lineEdit_temperatures_tpm
        self.wp_choice = wp_choice

    def run(self):
        MC.generate_TPM(self.Button_SelectM1_tpm,
                        self.Button_SelectM2_tpm,
                        self.Button_SelectM3_tpm,
                        self.lineEdit_fileselect_tpm,
                        self.lineEdit_name_tpm,
                        self.lineEdit_temperatures_tpm,
                        self.wp_choice)

class Worker_Validate(QtCore.QRunnable):
    """
    Outsourcing the generate VAL function, after started
    """
    def __init__(self, Data_Choice_combobox, profile_choice_files, Button_RandomChoice, int_random_files,
                 Button_ProfileChoice, Button_allProfiles, TRY_Choice_combobox, Button_SelectM1, Button_SelectM2,
                 Button_SelectM3, integer_number_horizon):
        super(Worker_Validate, self).__init__()
        self.Data_Choice_combobox_val = Data_Choice_combobox
        self.profile_choice_files_val = profile_choice_files
        self.Button_RandomChoice_val = Button_RandomChoice
        self.int_random_files_val = int_random_files
        self.Button_ProfileChoice_val = Button_ProfileChoice
        self.Button_allProfiles_val = Button_allProfiles
        self.TRY_Choice_combobox_val = TRY_Choice_combobox
        self.Button_SelectM1_val = Button_SelectM1
        self.Button_SelectM2_val = Button_SelectM2
        self.Button_SelectM3_val = Button_SelectM3
        self.integer_number_horizon = integer_number_horizon

    def run(self):
        MC.validate(self.Data_Choice_combobox_val,
                    self.profile_choice_files_val,
                    self.Button_RandomChoice_val,
                    self.int_random_files_val,
                    self.Button_ProfileChoice_val,
                    self.Button_allProfiles_val,
                    self.TRY_Choice_combobox_val,
                    self.Button_SelectM1_val,
                    self.Button_SelectM2_val,
                    self.Button_SelectM3_val,
                    self.integer_number_horizon)

class TaskThread(QtCore.QThread):
    """
    functionality of the progressbar for WSP and VAL
    """
    notifyProgress = QtCore.pyqtSignal(int)

    def __init__(self, button="WSP"):
        super(TaskThread, self).__init__()
        self.button = button

    def run(self):
        if self.button == "WSP":
            mD_gen_WSP.pre_wsp = "start_pulse"
            self.notifyProgress.emit("start_pulse")
            while True:
                if mD_gen_WSP.wsp_start_progress == 1 or mD_gen_WSP.turbo_marker == 1: break
                time.sleep(1)
            mD_gen_WSP.pre_wsp = "stop_pulse"
            self.notifyProgress.emit("stop_pulse")
            if mD_gen_WSP.turbo_marker == 1:
                for i in range(101):
                    self.notifyProgress.emit(i)
                    sleeptime = (mD_gen_WSP.duration*mD_gen_WSP.simDays)/100
                    time.sleep(sleeptime)
            if mD_gen_WSP.wsp_start_progress == 1:
                while True:
                    self.notifyProgress.emit(mD_gen_WSP.already_done*100/mD_gen_WSP.combinations)
                    if mD_gen_WSP.already_done * 100 / mD_gen_WSP.combinations == 100:
                        mD_gen_WSP.wsp_start_progress = 0
                        mD_gen_WSP.already_done = 0
                        mD_gen_WSP.combinations = 0
                        break
                    time.sleep(0.2)
        if self.button == "VAL":
            mD_gen_VAL.pre_wsp = "start_pulse"
            self.notifyProgress.emit("start_pulse")
            while True:
                if mD_gen_VAL.wsp_start_progress == 1 or mD_gen_VAL.turbo_marker == 1: break
                time.sleep(1)
            mD_gen_VAL.pre_wsp = "stop_pulse"
            self.notifyProgress.emit("stop_pulse")
            if mD_gen_VAL.turbo_marker == 1:
                for i in range(101):
                    self.notifyProgress.emit(i)
                    sleeptime = (mD_gen_VAL.val_horizon*365.25*mD_gen_VAL.duration)/100
                    time.sleep(sleeptime)
            if mD_gen_VAL.wsp_start_progress == 1:
                while True:
                    self.notifyProgress.emit((mD_gen_VAL.sim_year +
                                              mD_gen_VAL.already_done * 100 / mD_gen_VAL.combinations) /
                                             mD_gen_VAL.val_horizon)
                    if (mD_gen_VAL.sim_year + mD_gen_VAL.already_done * 100 / mD_gen_VAL.combinations) / mD_gen_VAL.val_horizon == 100:
                        mD_gen_WSP.wsp_start_progress = 0
                        mD_gen_WSP.already_done = 0
                        mD_gen_WSP.combinations = 0
                        break
                    time.sleep(0.2)

class TPMThread(QtCore.QThread):
    """
    functionality of the progressbar for TPM
    """
    taskFinished = QtCore.pyqtSignal()

    def run(self):
        while True:
            time.sleep(0.1)
            if mD_gen_TPM.check_tpm == 0: break
        self.taskFinished.emit()


class MW(QtGui.QMainWindow):
    """
    GUI Class, adding components etc.
    """

    def __init__(self):
        super(QtGui.QMainWindow, self).__init__()
        self.setWindowTitle(
            QtGui.QApplication.translate("MainWindow", "WinProGen", None, QtGui.QApplication.UnicodeUTF8))
        self.resize(609, 770)
        self.setFixedSize(609, 780)
        myQWidget = QtGui.QWidget()
        myBoxLayout = QtGui.QVBoxLayout()
        myQWidget.setLayout(myBoxLayout)
        self.setCentralWidget(myQWidget)
        self.centralwidget = QtGui.QWidget(myQWidget)
        self.threadpool = QThreadPool()

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 591, 770))
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        stylesheet = """
            QTabBar::tab {background-color: #0063b1; color: white; height: 30px; width: 98px; border: None}
            QTabBar::tab:selected {background: #008bfd;}
            """
        self.tabWidget.setStyleSheet(stylesheet)
        #self.tabWidget.setStyleSheet('QTabBar::tab-bar {right: 50x;}')
        myBoxLayout.addWidget(self.tabWidget)

        """
        Tab 1 - Generate WSP
        """

        self.tab_1 = QtGui.QWidget()

        ## Model Box with buttons for Model Selection
        self.Model_Box = QtGui.QGroupBox(self.tab_1)
        self.Model_Box.setGeometry(QtCore.QRect(0, 30, 591, 70))
        self.Model_Box.setTitle(QtGui.QApplication.translate("MainWindow", "Model selection",
                                                             None, QtGui.QApplication.UnicodeUTF8))
        self.Button_SelectM1 = QtGui.QRadioButton(self.Model_Box)
        self.Button_SelectM1.setGeometry(QtCore.QRect(20, 30, 120, 18))
        self.Button_SelectM1.setToolTip("Daily average ambient\ntemperature dependency")
        self.Button_SelectM1.setStyleSheet(style_tooltip)
        self.Button_SelectM1.setChecked(True)
        self.Button_SelectM1.setText(
            QtGui.QApplication.translate("MainWindow", "M1 - DAAT",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Button_SelectM2 = QtGui.QRadioButton(self.Model_Box)
        self.Button_SelectM2.setGeometry(QtCore.QRect(180, 30, 180, 18))
        self.Button_SelectM2.setToolTip("Daily average ambient temperature,"
                                        "\nweekday and weekend day dependency")
        self.Button_SelectM2.setStyleSheet(style_tooltip)
        self.Button_SelectM2.setText(
            QtGui.QApplication.translate("MainWindow", "M2 - DAAT WWED",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Button_SelectM3 = QtGui.QRadioButton(self.Model_Box)
        self.Button_SelectM3.setGeometry(QtCore.QRect(340, 30, 180, 18))
        self.Button_SelectM3.setToolTip("Daily average ambient temperature"
                                        "\nof actual and previous day dependency")
        self.Button_SelectM3.setStyleSheet(style_tooltip)
        self.Button_SelectM3.setText(
            QtGui.QApplication.translate("MainWindow", "M3 - DAAT A+PD",
                                         None, QtGui.QApplication.UnicodeUTF8))

        ## Profile Properties Box - WSP
        self.profile_properties_WSP_Box = QtGui.QGroupBox(self.tab_1)
        self.profile_properties_WSP_Box.setGeometry(QtCore.QRect(0, 120, 591, 291))
        self.profile_properties_WSP_Box.setTitle(QtGui.QApplication.translate("MainWindow",
                                                                              "Profile properties", None,
                                                                              QtGui.QApplication.UnicodeUTF8))
        self.Button_RandomChoice = QtGui.QRadioButton(self.profile_properties_WSP_Box)
        self.Button_RandomChoice.setGeometry(QtCore.QRect(340, 120, 111, 18))
        self.Button_RandomChoice.setToolTip("Type in the number of appartments"
                                            "\nwhich are randomly selected for"
                                            "\nprofile generation")
        self.Button_RandomChoice.setStyleSheet(style_tooltip)
        self.Button_RandomChoice.setText(
            QtGui.QApplication.translate("MainWindow", "Random choice", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.Button_ProfileChoice = QtGui.QRadioButton(self.profile_properties_WSP_Box)
        self.Button_ProfileChoice.setGeometry(QtCore.QRect(180, 120, 101, 18))
        self.Button_ProfileChoice.setToolTip("Select the appartments you"
                                             "\nwant to generate profiles for")
        self.Button_ProfileChoice.setStyleSheet(style_tooltip)
        self.Button_ProfileChoice.setText(
            QtGui.QApplication.translate("MainWindow", "Profile choice", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.label_chooseFieldtest = QtGui.QLabel(self.profile_properties_WSP_Box)
        self.label_chooseFieldtest.setGeometry(QtCore.QRect(20, 40, 130, 16))
        self.label_chooseFieldtest.setText(
            QtGui.QApplication.translate("MainWindow", "Choose a field test", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.Button_allProfiles = QtGui.QRadioButton(self.profile_properties_WSP_Box)
        self.Button_allProfiles.setGeometry(QtCore.QRect(20, 120, 150, 18))
        self.Button_allProfiles.setText(
            QtGui.QApplication.translate("MainWindow", "Complete dataset", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.Button_allProfiles.setToolTip("Generate all appartments")
        self.Button_allProfiles.setStyleSheet(style_tooltip)
        self.Button_allProfiles.setChecked(True)
        self.Data_Choice_combobox = QtGui.QComboBox(self.profile_properties_WSP_Box)
        self.Data_Choice_combobox.setGeometry(QtCore.QRect(20, 70, 120, 22))
        # add items to fieldtest-combobox
        self.Data_Choice_combobox.addItems(MC.dataset_fieldtests)

        def disable_model_selection():
            models = ["M1", "M2", "M3"]
            for model in models:
                if not os.path.exists(os.getcwd() +
                                              '/Data/TPM/TPM_' + str(self.Data_Choice_combobox.currentText()) +
                                              '_' + model + '.csv'):
                    if model == "M1": self.Button_SelectM1.setEnabled(False)
                    if model == "M2": self.Button_SelectM2.setEnabled(False)
                    if model == "M3": self.Button_SelectM3.setEnabled(False)
                else:
                    if model == "M1": self.Button_SelectM1.setEnabled(True)
                    if model == "M2": self.Button_SelectM2.setEnabled(True)
                    if model == "M3": self.Button_SelectM3.setEnabled(True)
        disable_model_selection()
        self.Data_Choice_combobox.currentIndexChanged.connect(lambda: disable_model_selection())

        ## implementing checkable combobox, not ready yet !!
        # self.Data_Choice_combobox = CheckableComboBox()
        # self.Data_Choice_combobox.setGeometry(QtCore.QRect(20, 70, 120, 22))
        # for i in range(3):
        #     self.Data_Choice_combobox.addItem("Combobox Item " + str(i))
        #     item = self.Data_Choice_combobox.model().item(i, 0)
        #     item.setCheckState(QtCore.Qt.Unchecked)

        self.substitute_button = QtGui.QCheckBox(self.profile_properties_WSP_Box)
        self.substitute_button.setGeometry(QtCore.QRect(20, 260, 400, 22))
        self.substitute_button.setToolTip("replace data of defect sensors"
                                          "\nby randomly assigned data from\nthe same type of room")
        self.substitute_button.setStyleSheet(style_tooltip)
        self.substitute_button.setChecked(True)
        self.substitute_button.setText(
            QtGui.QApplication.translate("MainWindow", "Substitute profiles with no changes in the state of the window",
                                         None, QtGui.QApplication.UnicodeUTF8))

        def disable_substitute_button():
            if str(MC.return_activated(self.Data_Choice_combobox)) in ["B1E1", "B1E2", "B1E3",
                                                                       "B2E1", "B2E2", "B2E3",
                                                                       "B3E1", "B3E2", "B3E3"]:
                self.substitute_button.setEnabled(True)
            else:
                self.substitute_button.setEnabled(False)
                self.substitute_button.setChecked(False)
        disable_substitute_button()
        self.Data_Choice_combobox.currentIndexChanged.connect(lambda: disable_substitute_button())

        self.int_random_files = QtGui.QSpinBox(self.profile_properties_WSP_Box)
        self.int_random_files.setGeometry(QtCore.QRect(340, 150, 46, 22))
        ## set maximum elements depending on number of profiles
        self.int_random_files.setMaximum(len(MC.get_levels(building=MC.return_activated(self.Data_Choice_combobox))))
        self.int_random_files.setMinimum(1)
        self.profile_choice_files = QtGui.QListWidget(self.profile_properties_WSP_Box)
        self.profile_choice_files.setGeometry(QtCore.QRect(180, 150, 120, 91))
        self.profile_choice_files.setSortingEnabled(False)
        __sortingEnabled = self.profile_choice_files.isSortingEnabled()
        self.profile_choice_files.setSortingEnabled(__sortingEnabled)
        # add profiles to list
        MC.fill_lists(self.profile_choice_files, MC.get_levels(building=MC.return_activated(self.Data_Choice_combobox)))
        self.Data_Choice_combobox.currentIndexChanged.\
            connect(lambda: MC.fill_lists(self.profile_choice_files, MC.get_levels(building=MC.return_activated(
                                                                                       self.Data_Choice_combobox))))
        self.label_TRY = QtGui.QLabel(self.profile_properties_WSP_Box)
        self.label_TRY.setGeometry(QtCore.QRect(180, 40, 150, 16))
        self.label_TRY.setText(QtGui.QApplication.translate("MainWindow", "Select weather conditions", None,
                                                            QtGui.QApplication.UnicodeUTF8))
        self.TRY_Choice_combobox = QtGui.QComboBox(self.profile_properties_WSP_Box)
        self.TRY_Choice_combobox.setGeometry(QtCore.QRect(180, 70, 180, 22))
        self.TRY_add_button = QtGui.QPushButton(self.profile_properties_WSP_Box)
        self.TRY_add_button.setGeometry(QtCore.QRect(362, 69, 34, 24))
        self.TRY_add_button.setText(
            QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))

        def openfile():
            # adding weather files to database
            self.getfiles()
            if self.path:
                if self.path.split(".")[-1] == "dat":
                    year = int(self.path.split("/")[-1].split("_")[0].split("TRY")[1])
                    df_final = pd.DataFrame(columns=["Date", "Weather"])
                    df = pd.read_table(self.path, skiprows=36, delim_whitespace=True, header=0)
                    df.drop(df.index[0], inplace=True)
                    df.reset_index(inplace=True)
                    df.drop(["index", "RG", "HH", "IS", "N", "WR", "WG", "p", "x",
                             "RF", "W", "B", "D", "IK", "A", "E","IL"], axis=1, inplace=True)

                    ix = 0
                    for month in range(12):
                        for day in range(calendar.monthrange(year, month + 1)[1]):
                            ix += 1
                            df_temp = df.loc[df['MM'] == month + 1]
                            df_temp = df_temp.loc[df['DD'] == day + 1]
                            temp_mean = np.float(df_temp["t"].mean())
                            df = df[(df['MM'] != month + 1) | (df['DD'] != day + 1)]
                            df_final.loc[ix] = [date(year, month + 1, day + 1), temp_mean]

                    df_final.columns = pd.MultiIndex.from_tuples([("", "", "", ""),
                                                                  ("Weather", "-", "-", "AT")])
                    df_final.to_csv(os.getcwd()+ "/Data/AT/additional_AT_files/" +
                                    self.path.split("/")[-1].split(".")[0] + ".csv", ";",index=0)
                else:
                    shutil.copyfile(self.path, os.getcwd() + self.path.split("/")[-1])
                self.TRY_Choice_combobox.addItem(self.path.split("/")[-1].split(".")[0])

        self.TRY_add_button.clicked.connect(lambda: openfile())
        # add items to weather-combobox
        self.TRY_Choice_combobox.addItems(MC.weatherset)

        ## Timestep Groupbox
        self.timestep_groupBox = QtGui.QGroupBox(self.tab_1)
        self.timestep_groupBox.setGeometry(QtCore.QRect(0, 430, 591, 101))
        self.timestep_groupBox.setTitle(
            QtGui.QApplication.translate("MainWindow", "Timestep", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.startDate = QtGui.QDateEdit(self.timestep_groupBox)
        self.startDate.setGeometry(QtCore.QRect(20, 60, 110, 22))
        self.startDate.setDate(QtCore.QDate.currentDate())
        self.startDate.setDisplayFormat("dd.MM")
        self.finalDate = QtGui.QDateEdit(self.timestep_groupBox)
        self.finalDate.setGeometry(QtCore.QRect(180, 60, 110, 22))
        self.finalDate.setDate(QtCore.QDate.currentDate())
        self.finalDate.setDisplayFormat("dd.MM")
        # get simulation days
        self.simulationdays = 0
        self.startDate.dateChanged.connect(self.update_simDays)
        self.finalDate.dateChanged.connect(self.update_simDays)
        self.label_startDate = QtGui.QLabel(self.timestep_groupBox)
        self.label_startDate.setGeometry(QtCore.QRect(20, 40, 46, 13))
        self.label_startDate.setText(
            QtGui.QApplication.translate("MainWindow", "from", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.label_finalDate = QtGui.QLabel(self.timestep_groupBox)
        self.label_finalDate.setGeometry(QtCore.QRect(180, 40, 46, 13))
        self.label_finalDate.setText(
            QtGui.QApplication.translate("MainWindow", "to", None,
                                         QtGui.QApplication.UnicodeUTF8))

        ## Output Groupbox - WSP
        self.output_groupBox_WSP = QtGui.QGroupBox(self.tab_1)
        self.output_groupBox_WSP.setGeometry(QtCore.QRect(0, 550, 591, 111))
        self.output_groupBox_WSP.setTitle(
            QtGui.QApplication.translate("MainWindow", "Output", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.label_outputDirectory = QtGui.QLabel(self.output_groupBox_WSP)
        self.label_outputDirectory.setGeometry(QtCore.QRect(20, 40, 241, 16))
        self.label_outputDirectory.setText(
            QtGui.QApplication.translate("MainWindow", "Select the output directory",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.label_filename = QtGui.QLabel(self.output_groupBox_WSP)
        self.label_filename.setGeometry(QtCore.QRect(20, 70, 241, 16))
        self.label_filename.setText(
            QtGui.QApplication.translate("MainWindow", "Choose a filename",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_path = QtGui.QLineEdit(self.output_groupBox_WSP)
        self.lineEdit_path.setGeometry(QtCore.QRect(200, 40, 340, 20))
        self.lineEdit_filename = QtGui.QLineEdit(self.output_groupBox_WSP)
        self.lineEdit_filename.setGeometry(QtCore.QRect(200, 70, 240, 20))
        # set default line for directory selection
        self.raw_path = pd.read_csv(os.getcwd() +
                                    "/properties/properties.csv", delimiter=";", index_col=0)
        if isinstance(self.raw_path.get_value("Output-path WSP", "Button state"), basestring):
            self.lineEdit_path.setText(self.raw_path.get_value("Output-path WSP", "Button state"))
        else: self.lineEdit_path.setText(os.getcwd())
        def text_change():
            self.raw_path.set_value("Output-path WSP", "Button state", str(self.lineEdit_path.text()))
            self.raw_path.to_csv(os.getcwd() + "/properties/properties.csv",";")
        self.lineEdit_path.textChanged.connect(lambda: text_change())
        self.checked_ini_date = self.startDate
        self.checked_fin_date = self.finalDate
        self.lineEdit_filename.setText("M1_" + str(MC.return_activated(self.Data_Choice_combobox)) + "_" +
                                       str(self.checked_ini_date.date().toPyDate()) + '_' +
                                       str(self.checked_fin_date.date().toPyDate()) + '.csv')

        def check_overwrite():
            # check if chosen file already exists and raise information
            self.label_warning.hide()
            self.warning_symbol.hide()
            filepaths = glob.glob(str(self.raw_path.get_value("Output-path WSP",
                                                              "Button state")) + "/*.csv")
            filepaths = [str(path.split("\\")[-1]) for path in filepaths]
            if "proSet_" +str(self.lineEdit_filename.text()) in filepaths:
                self.lineEdit_filename.setStyleSheet("color: rgb(255, 0, 0);")
                self.warning_symbol = QtGui.QLabel(self.output_groupBox_WSP) # add warnig pic
                self.warning_symbol.setGeometry(455, 71, 20, 18)
                MC.load_pic(self.warning_symbol, os.getcwd() + "/icons/warning.png")
                self.label_warning = QtGui.QLabel(self.output_groupBox_WSP)
                self.label_warning.setGeometry(QtCore.QRect(480, 72, 100, 16))
                self.label_warning.setText(
                    QtGui.QApplication.translate("MainWindow", "File already exists!",
                                                 None, QtGui.QApplication.UnicodeUTF8))
                self.warning_symbol.show()
                self.label_warning.show()
                self.label_warning.setText(
                    QtGui.QApplication.translate("MainWindow", "File already exists!",
                                                 None,QtGui.QApplication.UnicodeUTF8))
                self.check_variable = 1 # 1 if filename exists
            else:
                self.lineEdit_filename.setStyleSheet("color: rgb(0, 0, 0);")
                self.label_warning.hide()
                self.warning_symbol.hide()
                self.check_variable = 0 # 0 if filename doesn't exist

        self.check_variable = 1
        self.warning_symbol = QtGui.QLabel(self.output_groupBox_WSP)
        self.label_warning = QtGui.QLabel(self.output_groupBox_WSP)
        check_overwrite()

        def filename_update():
            # updating the filename if changed in GUI
            if self.Button_SelectM1.isChecked() == True:
                self.lineEdit_filename.setText("M1_" + str(MC.return_activated(self.Data_Choice_combobox)) +
                                               "_" + str(self.checked_ini_date.date().toPyDate()) + '_' +
                                               str(self.checked_fin_date.date().toPyDate()) + '.csv')
            elif self.Button_SelectM2.isChecked() == True:
                self.lineEdit_filename.setText("M2_" + str(MC.return_activated(self.Data_Choice_combobox)) +
                                               "_" + str(self.checked_ini_date.date().toPyDate()) + '_' +
                                               str(self.checked_fin_date.date().toPyDate()) + '.csv')
            elif self.Button_SelectM3.isChecked() == True:
                self.lineEdit_filename.setText("M3_" + str(MC.return_activated(self.Data_Choice_combobox)) +
                                               "_" + str(self.checked_ini_date.date().toPyDate()) + '_' +
                                               str(self.checked_fin_date.date().toPyDate()) + '.csv')

        self.startDate.dateChanged.connect(lambda: filename_update())
        self.finalDate.dateChanged.connect(lambda: filename_update())
        self.Data_Choice_combobox.activated.connect(lambda: filename_update())
        self.Button_SelectM1.clicked.connect(lambda: filename_update())
        self.Button_SelectM2.clicked.connect(lambda: filename_update())
        self.Button_SelectM3.clicked.connect(lambda: filename_update())
        self.lineEdit_filename.textChanged.connect(lambda: check_overwrite())

        self.directory_select_button_WSP = QtGui.QPushButton(self.output_groupBox_WSP)
        self.directory_select_button_WSP.setGeometry(QtCore.QRect(540, 39, 31, 22))
        self.directory_select_button_WSP.setText(
            QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.Button_Generate_WSP = QtGui.QPushButton(self.tab_1)
        self.Button_Generate_WSP.setGeometry(QtCore.QRect(0, 680, 75, 41))
        self.Button_Generate_WSP.setText(
            QtGui.QApplication.translate("MainWindow", "Generate", None, QtGui.QApplication.UnicodeUTF8))
        self.Button_Generate_WSP.setToolTip("profiles will be generated -"
                                            "\ninstance of program won't be"
                                            "\navailable while processing")
        self.Button_Generate_WSP.setStyleSheet(style_button_and_tooltip)
        self.progressBar = QtGui.QProgressBar(self.tab_1)
        self.progressBar.setGeometry(QtCore.QRect(90, 690, 471, 23))
        # set start value of progress bar
        self.progressBar.setProperty("value", 0)

        ## opening Windows directory to choose output directory
        def open_dialog_gen():
            self.openfolder()
            self.lineEdit_path.setText(str(self.directory))
        self.directory_select_button_WSP.clicked.connect(lambda: open_dialog_gen())

        ## Disabeling unused buttons
        self.profile_choice_files.setDisabled(True)
        self.int_random_files.setDisabled(True)

        def disable_buttons(button_rand=1, button_choose=0):
            # Disabeling unused buttons
            if button_rand == 1 and button_choose == 0:
                self.profile_choice_files.setDisabled(True)
                self.int_random_files.setEnabled(True)
            elif button_rand == 0 and button_choose == 1:
                self.profile_choice_files.setEnabled(True)
                self.int_random_files.setDisabled(True)
            else:
                self.profile_choice_files.setDisabled(True)
                self.int_random_files.setDisabled(True)

        self.Button_RandomChoice.clicked.connect(lambda: disable_buttons(1, 0))
        self.Button_ProfileChoice.clicked.connect(lambda: disable_buttons(0, 1))
        self.Button_allProfiles.clicked.connect(lambda: disable_buttons(1, 1))

        ## In case of existing filename, should file be overwritten?
        self.popup_result = 1

        def warn_dia():
            if self.check_variable == 1 and self.checkbox_overwrite.isChecked() == True:
                self.warning_popup()
            elif self.checkbox_overwrite.isChecked() == False:
                self.popup_result = 1

        self.Button_Generate_WSP.clicked.connect(lambda: warn_dia())

        ## Functionality of the progress bar
        self.myLongTask_WSP = TaskThread(button="WSP")
        self.Button_Generate_WSP.clicked.connect(self.onStart_WSP)
        self.myLongTask_WSP.notifyProgress.connect(self.onProgress_WSP)

        ## in case of profile selection, check if a min of 1 profile is checked
        self.popup_warning = 1

        def warning_profiles():
            if self.Button_ProfileChoice.isChecked() == True and \
                            MC.return_ckecked_profiles(self.profile_choice_files) == []:
                self.profiles_popup()
            else:
                self.popup_warning = 1

        self.Button_Generate_WSP.clicked.connect(lambda: warning_profiles())

        ## Function of "Generate" Button, starting the programm
        self.Button_Generate_WSP.clicked.connect(lambda: self.progressBar.setValue(0))
        self.Button_Generate_WSP.clicked.connect(self.generate_WSP)

        self.tabWidget.addTab(self.tab_1, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1),
                                  QtGui.QApplication.translate(
                                      "MainWindow", "Generate WSP", None, QtGui.QApplication.UnicodeUTF8))

        """
        Tab 2 - Generate TPM
        """

        self.tab_3 = QtGui.QWidget()

        ## Model Box with buttons for Model Selection - Validation
        self.Model_Box_tpm = QtGui.QGroupBox(self.tab_3)
        self.Model_Box_tpm.setGeometry(QtCore.QRect(0, 30, 591, 70))
        self.Model_Box_tpm.setTitle(
            QtGui.QApplication.translate("MainWindow", "Model selection",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Button_SelectM1_tpm = QtGui.QRadioButton(self.Model_Box_tpm)
        self.Button_SelectM1_tpm.setGeometry(QtCore.QRect(20, 30, 120, 18))
        self.Button_SelectM1_tpm.setText(
            QtGui.QApplication.translate("MainWindow", "M1 - DAAT",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Button_SelectM1_tpm.setToolTip("Daily average ambient\ntemperature dependency")
        self.Button_SelectM1_tpm.setStyleSheet(style_tooltip)
        self.Button_SelectM1_tpm.setChecked(True)
        self.Button_SelectM2_tpm = QtGui.QRadioButton(self.Model_Box_tpm)
        self.Button_SelectM2_tpm.setGeometry(QtCore.QRect(180, 30, 180, 18))
        self.Button_SelectM2_tpm.setText(
            QtGui.QApplication.translate("MainWindow", "M2 - DAAT WWED",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Button_SelectM2_tpm.setToolTip("Daily average ambient temperature,"
                                            "\nweekday and weekend day dependency")
        self.Button_SelectM2_tpm.setStyleSheet(style_tooltip)
        self.Button_SelectM3_tpm = QtGui.QRadioButton(self.Model_Box_tpm)
        self.Button_SelectM3_tpm.setGeometry(QtCore.QRect(340, 30, 180, 18))
        self.Button_SelectM3_tpm.setText(
            QtGui.QApplication.translate("MainWindow", "M3 - DAAT A+PD",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Button_SelectM3_tpm.setToolTip("Daily average ambient temperature"
                                            "\nof actual and previous day dependency")
        self.Button_SelectM3_tpm.setStyleSheet(style_tooltip)

        ## Profile properties box
        self.groupBox_profileprops_tpm = QtGui.QGroupBox(self.tab_3)
        self.groupBox_profileprops_tpm.setGeometry(QtCore.QRect(0, 120, 591, 241))
        self.groupBox_profileprops_tpm.setTitle(
            QtGui.QApplication.translate("MainWindow", "Profile Properties",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_fileselect_tpm = QtGui.QLineEdit(self.groupBox_profileprops_tpm)
        self.lineEdit_fileselect_tpm.setGeometry(QtCore.QRect(170, 40, 361, 20))
        self.label_fileselect_tpm = QtGui.QLabel(self.groupBox_profileprops_tpm)
        self.label_fileselect_tpm.setGeometry(QtCore.QRect(20, 40, 101, 16))
        self.label_fileselect_tpm.setText(
            QtGui.QApplication.translate("MainWindow", "Select a file",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_fileselect_tpm = QtGui.QPushButton(self.groupBox_profileprops_tpm)
        self.pushButton_fileselect_tpm.setGeometry(QtCore.QRect(531, 39, 31, 22))
        self.pushButton_fileselect_tpm.setText(
            QtGui.QApplication.translate("MainWindow", "...",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.label_fieldtestname_tpm = QtGui.QLabel(self.groupBox_profileprops_tpm)
        self.label_fieldtestname_tpm.setGeometry(QtCore.QRect(20, 70, 101, 16))
        self.label_fieldtestname_tpm.setText(
            QtGui.QApplication.translate("MainWindow", "Name of the fieldtest",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_name_tpm = QtGui.QLineEdit(self.groupBox_profileprops_tpm)
        self.lineEdit_name_tpm.setGeometry(QtCore.QRect(170, 70, 361, 20))
        self.lineEdit_name_tpm.setPlaceholderText("e. g. MainBuilding")
        self.label_temperatures_tpm = QtGui.QLabel(self.groupBox_profileprops_tpm)
        self.label_temperatures_tpm.setGeometry(QtCore.QRect(20, 100, 101, 16))
        self.label_temperatures_tpm.setText(
            QtGui.QApplication.translate("MainWindow", "Temperature range",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_temperatures_tpm = QtGui.QLineEdit(self.groupBox_profileprops_tpm)
        self.lineEdit_temperatures_tpm.setGeometry(QtCore.QRect(170, 100, 361, 20))
        self.lineEdit_temperatures_tpm.setPlaceholderText("e. g. 5,11,14,18 - Give a minimum of 3 temperatures!")

        #todo activate after solving problem with TPM generation by equal windows
        # self.label_equal_windows = QtGui.QLabel(self.groupBox_profileprops_tpm)
        # self.label_equal_windows.setGeometry(QtCore.QRect(20, 130, 141, 16))
        # self.label_equal_windows.setText(
        #     QtGui.QApplication.translate("MainWindow", "Windows with equal sizes", None, QtGui.QApplication.UnicodeUTF8))
        #
        # self.wp_choice = QtGui.QListWidget(self.groupBox_profileprops_tpm)
        # self.wp_choice.setGeometry(QtCore.QRect(170, 130, 361, 20))
        # self.wp_choice.setFlow(QtGui.QListView.LeftToRight)
        # self.wp_choice.setSortingEnabled(False)
        # __sortingEnabled = self.profile_choice_files.isSortingEnabled()
        # self.wp_choice.setSortingEnabled(__sortingEnabled)
        # ## refresh profiles in list
        # def refresh_wps():
        #     wps = np.unique(pd.read_csv(str(self.lineEdit_fileselect_tpm.text()), skiprows=2, nrows=1, skip_blank_lines=True, sep=";").values[0]).tolist()
        #     del wps[:2]
        #     MC.fill_lists(self.wp_choice, wps)
        # self.lineEdit_fileselect_tpm.textChanged.connect(lambda: refresh_wps())

        self.wp_choice=[]

        self.Button_Generate_TPM = QtGui.QPushButton(self.tab_3)
        self.Button_Generate_TPM.setGeometry(QtCore.QRect(0, 385, 75, 41))
        self.Button_Generate_TPM.setStyleSheet("background-color: #0063b1; color: white;")
        self.Button_Generate_TPM.setText(
            QtGui.QApplication.translate("MainWindow", "Generate",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.progressBar_tpm = QtGui.QProgressBar(self.tab_3)
        self.progressBar_tpm.setGeometry(QtCore.QRect(90, 395, 471, 23))
        self.progressBar_tpm.setProperty("value", 0)

        ## opening orininal input file from Windows directory
        def open_dialog_tpm():
            self.openfile()
            self.lineEdit_fileselect_tpm.setText(str(self.path))
        self.pushButton_fileselect_tpm.clicked.connect(lambda: open_dialog_tpm())

        ## warnings, in case of: no file, name or temperature range selected
        mD_gen_TPM.check_tpm = 1
        def warn_tpm():
            if self.lineEdit_fileselect_tpm.text() == "" or \
                            self.lineEdit_name_tpm.text() == "" or \
                            self.lineEdit_temperatures_tpm.text() == "" or \
                            "_" in self.lineEdit_name_tpm.text() or \
                            self.lineEdit_name_tpm.text().count(",") >= 2:
                self.warnings_tpm()
                mD_gen_TPM.check_tpm = 0
            else:
                mD_gen_TPM.check_tpm = 1

            for char in str(self.lineEdit_temperatures_tpm.text()):
                if char.isalpha() == True:
                    wrng = QtGui.QMessageBox.warning(
                        self, "Warning!", "Wrong format. "
                                          "\nImput should only contain numbers and commas in form"
                                          "\n\n a,b, ... ,z"
                                          "\n\n for number a,b, .. ,z!", QtGui.QMessageBox.Ok)
                    mD_gen_TPM.check_tpm = 0
                    break
                
        self.Button_Generate_TPM.clicked.connect(lambda: warn_tpm())
        self.Button_Generate_TPM.clicked.connect(self.onStart_TPM)
        self.myLongTask_TPM = TPMThread()
        self.myLongTask_TPM.taskFinished.connect(self.onFinished_TPM)
        self.Button_Generate_TPM.clicked.connect(self.generate_TPM)

        self.tabWidget.addTab(self.tab_3, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3),
                                  QtGui.QApplication.translate("MainWindow", "Add field test", None,
                                                               QtGui.QApplication.UnicodeUTF8))

        """
        Tab 3 - MCMC validation
        """

        self.tab_4 = QtGui.QWidget()

        ## Model Box with buttons for Model Selection - Validation
        self.Model_Box_val = QtGui.QGroupBox(self.tab_4)
        self.Model_Box_val.setGeometry(QtCore.QRect(0, 30, 591, 70))
        self.Model_Box_val.setTitle(
            QtGui.QApplication.translate("MainWindow", "Model selection",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Button_SelectM1_val = QtGui.QRadioButton(self.Model_Box_val)
        self.Button_SelectM1_val.setGeometry(QtCore.QRect(20, 30, 120, 18))
        self.Button_SelectM1_val.setText(
            QtGui.QApplication.translate("MainWindow", "M1 - DAAT",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Button_SelectM1_val.setToolTip("Daily average ambient"
                                            "\ntemperature dependency")
        self.Button_SelectM1_val.setStyleSheet(style_tooltip)
        self.Button_SelectM1_val.setChecked(True)
        self.Button_SelectM2_val = QtGui.QRadioButton(self.Model_Box_val)
        self.Button_SelectM2_val.setGeometry(QtCore.QRect(180, 30, 180, 18))
        self.Button_SelectM2_val.setText(
            QtGui.QApplication.translate("MainWindow", "M2 - DAAT WWED",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Button_SelectM2_val.setToolTip("Daily average ambient temperature,"
                                            "\nweekday and weekend day dependency")
        self.Button_SelectM2_val.setStyleSheet(style_tooltip)
        self.Button_SelectM3_val = QtGui.QRadioButton(self.Model_Box_val)
        self.Button_SelectM3_val.setGeometry(QtCore.QRect(340, 30, 180, 18))
        self.Button_SelectM3_val.setText(
            QtGui.QApplication.translate("MainWindow", "M3 - DAAT A+PD",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Button_SelectM3_val.setToolTip("Daily average ambient temperature"
                                            "\nof actual and previous day dependency")
        self.Button_SelectM3_val.setStyleSheet(style_tooltip)

        ## Profile Properties Box - Validation
        self.profile_properties_WSP_Box_val = QtGui.QGroupBox(self.tab_4)
        self.profile_properties_WSP_Box_val.setGeometry(QtCore.QRect(0, 120, 591, 271))
        self.profile_properties_WSP_Box_val.setTitle(
            QtGui.QApplication.translate("MainWindow", "Profile properties",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Button_RandomChoice_val = QtGui.QRadioButton(self.profile_properties_WSP_Box_val)
        self.Button_RandomChoice_val.setGeometry(QtCore.QRect(340, 120, 111, 18))
        self.Button_RandomChoice_val.setText(
            QtGui.QApplication.translate("MainWindow", "Random choice",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Button_RandomChoice_val.setToolTip("Type in the number of appartments"
                                                "\nwhich are randomly selected for\nprofile generation")
        self.Button_RandomChoice_val.setStyleSheet(style_tooltip)
        self.Button_ProfileChoice_val = QtGui.QRadioButton(self.profile_properties_WSP_Box_val)
        self.Button_ProfileChoice_val.setGeometry(QtCore.QRect(180, 120, 101, 18))
        self.Button_ProfileChoice_val.setText(
            QtGui.QApplication.translate("MainWindow", "Profile choice",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Button_ProfileChoice_val.setToolTip("Select the appartments you"
                                                 "\nwant to generate profiles for")
        self.Button_ProfileChoice_val.setStyleSheet(style_tooltip)
        self.label_chooseFieldtest_val = QtGui.QLabel(self.profile_properties_WSP_Box_val)
        self.label_chooseFieldtest_val.setGeometry(QtCore.QRect(20, 40, 130, 16))
        self.label_chooseFieldtest_val.setText(
            QtGui.QApplication.translate("MainWindow", "Choose a field test",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Button_allProfiles_val = QtGui.QRadioButton(self.profile_properties_WSP_Box_val)
        self.Button_allProfiles_val.setGeometry(QtCore.QRect(20, 120, 150, 18))
        self.Button_allProfiles_val.setText(
            QtGui.QApplication.translate("MainWindow", "Complete dataset",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Button_allProfiles_val.setToolTip("Generate all appartments")
        self.Button_allProfiles_val.setStyleSheet(style_tooltip)
        self.Button_allProfiles_val.setChecked(True)
        self.Data_Choice_combobox_val = QtGui.QComboBox(self.profile_properties_WSP_Box_val)
        self.Data_Choice_combobox_val.setGeometry(QtCore.QRect(20, 70, 120, 22))
        # add items to fieldtest-combobox
        self.Data_Choice_combobox_val.addItems(MC.dataset_fieldtests)

        def disable_model_selection_val():
            models_val = ["M1", "M2", "M3"]
            for model_val in models_val:
                if not os.path.exists(os.getcwd() +
                                              '/Data/TPM/TPM_' + str(self.Data_Choice_combobox_val.currentText()) +
                                              '_' + model_val + '.csv'):
                    if model_val == "M1": self.Button_SelectM1_val.setEnabled(False)
                    if model_val == "M2": self.Button_SelectM2_val.setEnabled(False)
                    if model_val == "M3": self.Button_SelectM3_val.setEnabled(False)
                else:
                    if model_val == "M1": self.Button_SelectM1_val.setEnabled(True)
                    if model_val == "M2": self.Button_SelectM2_val.setEnabled(True)
                    if model_val == "M3": self.Button_SelectM3_val.setEnabled(True)
        disable_model_selection_val()
        self.Data_Choice_combobox_val.currentIndexChanged.connect(lambda: disable_model_selection_val())

        self.int_random_files_val = QtGui.QSpinBox(self.profile_properties_WSP_Box_val)
        self.int_random_files_val.setGeometry(QtCore.QRect(340, 150, 46, 22))
        # set maximum elements depending on number of profiles
        self.int_random_files_val.setMaximum(len(MC.get_levels(
            building=MC.return_activated(self.Data_Choice_combobox_val))))
        self.int_random_files_val.setMinimum(1)
        self.profile_choice_files_val = QtGui.QListWidget(self.profile_properties_WSP_Box_val)
        self.profile_choice_files_val.setGeometry(QtCore.QRect(180, 150, 120, 91))
        self.profile_choice_files_val.setSortingEnabled(False)
        __sortingEnabled = self.profile_choice_files.isSortingEnabled()
        self.profile_choice_files_val.setSortingEnabled(__sortingEnabled)
        # add profiles to list
        MC.fill_lists(self.profile_choice_files_val, MC.get_levels(
            building=MC.return_activated(self.Data_Choice_combobox_val)))
        self.Data_Choice_combobox_val.currentIndexChanged.connect(
            lambda: MC.fill_lists(self.profile_choice_files_val, MC.get_levels(
                building=MC.return_activated( self.Data_Choice_combobox_val))))
        self.label_TRY_val = QtGui.QLabel(self.profile_properties_WSP_Box_val)
        self.label_TRY_val.setGeometry(QtCore.QRect(180, 40, 150, 16))
        self.label_TRY_val.setText(QtGui.QApplication.translate(
            "MainWindow", "Select weather conditions", None, QtGui.QApplication.UnicodeUTF8))
        self.TRY_Choice_combobox_val = QtGui.QComboBox(self.profile_properties_WSP_Box_val)
        self.TRY_Choice_combobox_val.setGeometry(QtCore.QRect(180, 70, 180, 22))
        self.TRY_add_button_val = QtGui.QPushButton(self.profile_properties_WSP_Box_val)
        self.TRY_add_button_val.setGeometry(QtCore.QRect(362, 69, 34, 24))
        self.TRY_add_button_val.setText(
            QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))

        def openfile_val():
            # adding weather files to database
            self.getfiles()
            if self.path:
                if self.path.split(".")[-1] == "dat":
                    year = int(self.path.split("/")[-1].split("_")[0].split("TRY")[1])
                    df_final = pd.DataFrame(columns=["Date", "Weather"])
                    df = pd.read_table(self.path, skiprows=36, delim_whitespace=True, header=0)
                    df.drop(df.index[0], inplace=True)
                    df.reset_index(inplace=True)
                    df.drop(["index", "RG", "HH", "IS", "N", "WR", "WG", "p", "x",
                             "RF", "W", "B", "D", "IK", "A", "E","IL"], axis=1, inplace=True)

                    ix = 0
                    for month in range(12):
                        for day in range(calendar.monthrange(year, month + 1)[1]):
                            ix += 1
                            df_temp = df.loc[df['MM'] == month + 1]
                            df_temp = df_temp.loc[df['DD'] == day + 1]
                            temp_mean = np.float(df_temp["t"].mean())
                            df = df[(df['MM'] != month + 1) | (df['DD'] != day + 1)]
                            df_final.loc[ix] = [date(year, month + 1, day + 1), temp_mean]

                    df_final.columns = pd.MultiIndex.from_tuples([("", "", "", ""),
                                                                  ("Weather", "-", "-", "AT")])
                    df_final.to_csv(os.getcwd()+ "/Data/AT/additional_AT_files/" +
                                    self.path.split("/")[-1].split(".")[0] + ".csv", ";",index=0)
                else:
                    shutil.copyfile(self.path, os.getcwd() + self.path.split("/")[-1])
                self.TRY_Choice_combobox_val.addItem(self.path.split("/")[-1])

        self.TRY_add_button_val.clicked.connect(lambda: openfile_val())
        # add items to weather-combobox
        self.TRY_Choice_combobox_val.addItems(MC.weatherset)

        ## Validation Horizon Groupbox
        self.ValidationHorizon_groupBox_val = QtGui.QGroupBox(self.tab_4)
        self.ValidationHorizon_groupBox_val.setGeometry(QtCore.QRect(0, 410, 591, 90))
        self.ValidationHorizon_groupBox_val.setTitle(
            QtGui.QApplication.translate("MainWindow", "Validation horizon",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.label_horizon = QtGui.QLabel(self.ValidationHorizon_groupBox_val)
        self.label_horizon.setGeometry(QtCore.QRect(20, 40, 300, 16))
        self.label_horizon.setText(
            QtGui.QApplication.translate("MainWindow", "Number of years for the MCMC Validation",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.integer_number_horizon = QtGui.QSpinBox(self.ValidationHorizon_groupBox_val)
        self.integer_number_horizon.setGeometry(QtCore.QRect(280, 38, 50, 22))
        self.integer_number_horizon.setMaximum(200)
        self.integer_number_horizon.setMinimum(2)
        self.integer_number_horizon.setValue(100)
        self.integer_number_horizon.valueChanged.connect(self.update_val_horizon)

        self.Button_Validate_val = QtGui.QPushButton(self.tab_4)
        self.Button_Validate_val.setGeometry(QtCore.QRect(0, 680, 75, 41))
        self.Button_Validate_val.setText(
            QtGui.QApplication.translate("MainWindow", "Validate", None, QtGui.QApplication.UnicodeUTF8))
        self.Button_Validate_val.setToolTip("profiles will be validated -"
                                            "\ninstance of program won't be"
                                            "\navailable while processing")
        self.Button_Validate_val.setStyleSheet(style_button_and_tooltip)
        self.progressBar_val = QtGui.QProgressBar(self.tab_4)
        self.progressBar_val.setGeometry(QtCore.QRect(90, 690, 471, 23))
        # set start value of progress bar
        self.progressBar_val.setProperty("value", 0)

        ## Disabeling unused buttons
        self.profile_choice_files_val.setDisabled(True)
        self.int_random_files_val.setDisabled(True)

        def disable_buttons_val(button_rand=1, button_choose=0):
            if button_rand == 1 and button_choose == 0:
                self.profile_choice_files_val.setDisabled(True)
                self.int_random_files_val.setEnabled(True)
            elif button_rand == 0 and button_choose == 1:
                self.profile_choice_files_val.setEnabled(True)
                self.int_random_files_val.setDisabled(True)
            else:
                self.profile_choice_files_val.setDisabled(True)
                self.int_random_files_val.setDisabled(True)

        self.Button_RandomChoice_val.clicked.connect(lambda: disable_buttons_val(1, 0))
        self.Button_ProfileChoice_val.clicked.connect(lambda: disable_buttons_val(0, 1))
        self.Button_allProfiles_val.clicked.connect(lambda: disable_buttons_val(1, 1))

        ## Functionality of the progress bar
        self.myLongTask_val = TaskThread(button="VAL")
        self.Button_Validate_val.clicked.connect(self.onStart_VAL)
        self.myLongTask_val.notifyProgress.connect(self.onProgress_VAL)

        ## in case of profile selection, check if a min of 1 profile is checked
        self.popup_warning_val = 1

        def warning_profiles_val():
            if self.Button_ProfileChoice_val.isChecked() == True and \
                            MC.return_ckecked_profiles(self.profile_choice_files_val) == []:
                self.profiles_popup()
            else:
                self.popup_warning_val = 1

        self.Button_Validate_val.clicked.connect(lambda: warning_profiles_val())

        ## Function of "Validate" Button, starting the programm
        self.Button_Validate_val.clicked.connect(lambda: self.progressBar_val.setProperty("value", 0))
        self.Button_Validate_val.clicked.connect(self.validate)

        self.tabWidget.addTab(self.tab_4, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4),
                                  QtGui.QApplication.translate("MainWindow", "MCMC Validation",
                                                               None, QtGui.QApplication.UnicodeUTF8))

        """
        Tab 4 - Visualize Data
        """

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        ## Diagram typology groupbox visualize
        self.diagram_typology_groupBox = QtGui.QGroupBox(self.tab_2)
        self.diagram_typology_groupBox.setGeometry(QtCore.QRect(0, 30, 591, 300))
        self.diagram_typology_groupBox.setTitle(
            QtGui.QApplication.translate("MainWindow", "Diagram typology",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.label_Diagram1 = QtGui.QLabel(self.diagram_typology_groupBox)
        self.label_Diagram1.setGeometry(QtCore.QRect(36, 190, 250, 40))
        self.label_Diagram1.setText(QtGui.QApplication.translate(
            "MainWindow", "Windows status \ndepending on daily average \noutdoor temperature",
            None, QtGui.QApplication.UnicodeUTF8))
        self.label_Diagram2 = QtGui.QLabel(self.diagram_typology_groupBox)
        self.label_Diagram2.setGeometry(QtCore.QRect(217, 190, 250, 40))
        self.label_Diagram2.setText(
            QtGui.QApplication.translate("MainWindow", "Daily profile: "
                                                       "\nWindows status depending "
                                                       "\non daytime", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.label_Diagram3 = QtGui.QLabel(self.diagram_typology_groupBox)
        self.label_Diagram3.setGeometry(QtCore.QRect(396, 190, 250, 40))
        self.label_Diagram3.setText(
            QtGui.QApplication.translate("MainWindow", "Daily profile: "
                                                       "\nStatus change depending "
                                                       "\non daytime", None,
                                         QtGui.QApplication.UnicodeUTF8))
        # adding buttons for diagrams
        self.Button_dia1 = QtGui.QToolButton(self.diagram_typology_groupBox)
        self.Button_dia1.setGeometry(QtCore.QRect(20, 40, 170, 140))
        self.Button_dia1.setStyleSheet("background-color: #dcdcdc")
        self.icon_dia1 = QIcon(os.getcwd() + "/icons/dia1.png")
        self.Button_dia1.setIcon(self.icon_dia1)
        self.Button_dia1.setIconSize(QtCore.QSize(150, 150))
        self.Button_dia1.setCheckable(True)
        #self.Button_dia1.setToolTip("Tooltip following ...")
        self.Button_dia2 = QtGui.QToolButton(self.diagram_typology_groupBox)
        self.Button_dia2.setGeometry(QtCore.QRect(201, 40, 170, 140))
        self.Button_dia2.setStyleSheet("background-color: #dcdcdc")
        self.icon_dia2 = QIcon(os.getcwd() + "/icons/dia2.png")
        self.Button_dia2.setIcon(self.icon_dia2)
        self.Button_dia2.setIconSize(QtCore.QSize(150, 150))
        self.Button_dia2.setCheckable(True)
        #self.Button_dia2.setToolTip("Tooltip following ...")
        self.Button_dia3 = QtGui.QToolButton(self.diagram_typology_groupBox)
        self.Button_dia3.setGeometry(QtCore.QRect(380, 40, 170, 140))
        self.Button_dia3.setStyleSheet("background-color: #dcdcdc")
        self.icon_dia3 = QIcon(os.getcwd() + "/icons/dia3.png")
        self.Button_dia3.setIcon(self.icon_dia3)
        self.Button_dia3.setIconSize(QtCore.QSize(150, 150))
        self.Button_dia3.setCheckable(True)
        #self.Button_dia3.setToolTip("Tooltip following ...")
        self.checkbox_std = QCheckBox(self.diagram_typology_groupBox)
        self.checkbox_std.setGeometry(QtCore.QRect(36, 225, 250, 40))
        self.checkbox_std.setText(QtGui.QApplication.translate("MainWindow",
                                                               "include standard deviation", None,
                                                               QtGui.QApplication.UnicodeUTF8))
        self.building_comparison = QtGui.QRadioButton(self.diagram_typology_groupBox)
        self.building_comparison.setGeometry(QtCore.QRect(36, 270, 120, 18))
        self.building_comparison.setText(
            QtGui.QApplication.translate("MainWindow", "Building comparison",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.room_comparison = QtGui.QRadioButton(self.diagram_typology_groupBox)
        self.room_comparison.setGeometry(QtCore.QRect(396, 270, 120, 18))
        self.room_comparison.setText(
            QtGui.QApplication.translate("MainWindow", "Room comparison",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.level_comparison = QtGui.QRadioButton(self.diagram_typology_groupBox)
        self.level_comparison.setGeometry(QtCore.QRect(216, 270, 120, 18))
        self.level_comparison.setText(
            QtGui.QApplication.translate("MainWindow", "Level comparison",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_load_profile = QtGui.QLineEdit(self.diagram_typology_groupBox)
        self.lineEdit_load_profile.setGeometry(QtCore.QRect(140, 270, 380, 20))
        self.lineEdit_load_profile.textChanged.connect(lambda: self.label_fieldtest_dyanamic.setText(
            QtGui.QApplication.translate(
                "MainWindow", str(self.lineEdit_load_profile.text().split("/")[-1].split("_")[2]), None,
                                         QtGui.QApplication.UnicodeUTF8)))
        self.lineEdit_load_profile.hide()
        self.label_lineEdit_load_profile = QtGui.QLabel(self.diagram_typology_groupBox)
        self.label_lineEdit_load_profile.setGeometry(QtCore.QRect(36, 270, 241, 16))
        self.label_lineEdit_load_profile.setText(
            QtGui.QApplication.translate("MainWindow", "Select a profile:",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.label_lineEdit_load_profile.hide()
        self.dir_button_profile_load = QtGui.QPushButton(self.diagram_typology_groupBox)
        self.dir_button_profile_load.setGeometry(QtCore.QRect(520, 269, 31, 22))
        self.dir_button_profile_load.setText(
            QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.dir_button_profile_load.hide()

        ## Profile Properties Visualize Groupbox
        self.profile_properties_visual = QtGui.QGroupBox(self.tab_2)
        self.profile_properties_visual.setGeometry(QtCore.QRect(0, 350, 591, 180))
        self.profile_properties_visual.setTitle(
            QtGui.QApplication.translate("MainWindow", "Profile properties",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.label_choose_diagram = QtGui.QLabel(self.profile_properties_visual)
        self.label_choose_diagram.setGeometry(QtCore.QRect(200, 90, 200, 16))
        self.label_choose_diagram.setText(
            QtGui.QApplication.translate("MainWindow", "Select a diagram typology previously!",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.label_selectFieldtest = QtGui.QLabel(self.profile_properties_visual)
        self.label_selectFieldtest.setGeometry(QtCore.QRect(20, 30, 150, 16))
        self.label_selectFieldtest.setText(
            QtGui.QApplication.translate("MainWindow", "Fieldtests:",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.list_fieldtest_choice = QtGui.QListWidget(self.profile_properties_visual)
        self.list_fieldtest_choice.setGeometry(QtCore.QRect(20, 50, 120, 91))
        # add profiles to list
        for profile in MC.dataset_fieldtests:
            item = QtGui.QListWidgetItem(self.list_fieldtest_choice)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setText(str(profile))
        self.building_combobox = QtGui.QComboBox(self.profile_properties_visual)
        self.building_combobox.setGeometry(QtCore.QRect(20, 50, 120, 22))
        self.building_combobox.hide()
        # add items to combobox
        self.building_combobox.addItems(MC.dataset_fieldtests)
        self.allData = QtGui.QCheckBox(self.profile_properties_visual)
        self.allData.setGeometry(QtCore.QRect(25, 145, 100, 22))
        self.allData.setText(QtGui.QApplication.translate("MainWindow", "All",
                                                          None, QtGui.QApplication.UnicodeUTF8))
        self.label_selectLevel = QtGui.QLabel(self.profile_properties_visual)
        self.label_selectLevel.setGeometry(QtCore.QRect(200, 30, 150, 16))
        self.label_selectLevel.setText(
            QtGui.QApplication.translate("MainWindow", "Levels:",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.list_levels = QtGui.QListWidget(self.profile_properties_visual)
        self.list_levels.setGeometry(QtCore.QRect(200, 50, 120, 91))
        # add profiles to list
        MC.fill_lists(self.list_levels, MC.get_levels(
            building=MC.return_activated(self.building_combobox)))
        self.level_combobox = QtGui.QComboBox(self.profile_properties_visual)
        self.level_combobox.setGeometry(QtCore.QRect(200, 50, 120, 22))
        self.level_combobox.hide()
        # add items to level-combobox
        self.level_combobox.addItems(MC.get_levels(
            building=MC.return_activated(self.building_combobox)))
        self.allLevels = QtGui.QCheckBox(self.profile_properties_visual)
        self.allLevels.setGeometry(QtCore.QRect(205, 145, 100, 22))
        self.allLevels.setText(QtGui.QApplication.translate("MainWindow", "All",
                                                            None, QtGui.QApplication.UnicodeUTF8))
        self.label_selectRoom = QtGui.QLabel(self.profile_properties_visual)
        self.label_selectRoom.setGeometry(QtCore.QRect(380, 30, 150, 16))
        self.label_selectRoom.setText(
            QtGui.QApplication.translate("MainWindow", "Rooms:",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.list_rooms = QtGui.QListWidget(self.profile_properties_visual)
        self.list_rooms.setGeometry(QtCore.QRect(380, 50, 120, 91))
        # add profiles to list
        MC.fill_lists(self.list_rooms, MC.get_rooms(
            building=MC.return_activated(self.building_combobox),
            level=str(MC.return_activated(self.level_combobox))))
        MC.fill_combobox(self.level_combobox, MC.get_levels(
            building=MC.return_activated(self.building_combobox)))
        self.label_intervals = QtGui.QLabel(self.profile_properties_visual)
        self.label_intervals.setGeometry(QtCore.QRect(380, 30, 150, 16))
        self.label_intervals.setText(
            QtGui.QApplication.translate("MainWindow", "Intervals:",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.label_intervals.hide()
        self.list_intervals = QtGui.QListWidget(self.profile_properties_visual)
        self.list_intervals.setGeometry(QtCore.QRect(380, 50, 200, 91))
        self.list_intervals.hide()
        self.allIntervals = QtGui.QCheckBox(self.profile_properties_visual)
        self.allIntervals.setGeometry(QtCore.QRect(385, 145, 100, 22))
        self.allIntervals.setText(
            QtGui.QApplication.translate("MainWindow", "All",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.allIntervals.hide()
        # fill interval list
        MC.fill_lists(self.list_intervals,
                      MC.get_intervals(MC.return_activated(self.building_combobox)))
        self.allRooms = QtGui.QCheckBox(self.profile_properties_visual)
        self.allRooms.setGeometry(QtCore.QRect(385, 145, 100, 22))
        self.allRooms.setText(QtGui.QApplication.translate("MainWindow", "All",
                                                           None, QtGui.QApplication.UnicodeUTF8))
        self.rooms_combobox = QtGui.QComboBox(self.profile_properties_visual)
        self.rooms_combobox.setGeometry(QtCore.QRect(200, 95, 120, 22))
        # fill combobox
        MC.fill_combobox(self.rooms_combobox, MC.get_rooms(
            building=MC.return_activated(self.building_combobox),
            level=str(MC.return_activated(self.level_combobox))))
        self.rooms_combobox.hide()
        self.label_rooms_combobox = QtGui.QLabel(self.profile_properties_visual)
        self.label_rooms_combobox.setGeometry(QtCore.QRect(200, 75, 100, 22))
        self.label_rooms_combobox.setText(
            QtGui.QApplication.translate("MainWindow", "Rooms:",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.label_rooms_combobox.hide()
        self.WP_combobox = QtGui.QComboBox(self.profile_properties_visual)
        self.WP_combobox.setGeometry(QtCore.QRect(200, 140, 120, 22))
        # fill combobox
        MC.fill_combobox(self.WP_combobox, MC.get_WPs(
            building=MC.return_activated(self.building_combobox),
            room=str(MC.return_activated(self.rooms_combobox))))
        self.WP_combobox.hide()
        self.label_WP_combobox = QtGui.QLabel(self.profile_properties_visual)
        self.label_WP_combobox.setGeometry(QtCore.QRect(200, 120, 100, 22))
        self.label_WP_combobox.setText(
            QtGui.QApplication.translate("MainWindow", "Window position:",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.label_WP_combobox.hide()
        self.label_fieldtest_dyanamic = QtGui.QLabel(self.profile_properties_visual)
        self.label_fieldtest_dyanamic.setGeometry(QtCore.QRect(20, 50, 120, 22))
        self.label_fieldtest_dyanamic.setText(
            QtGui.QApplication.translate("MainWindow", "",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.label_model = QtGui.QLabel(self.profile_properties_visual)
        self.label_model.setGeometry(QtCore.QRect(20, 75, 100, 22))
        self.label_model.setText(
            QtGui.QApplication.translate("MainWindow", "Model:",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.model_combobox = QtGui.QComboBox(self.profile_properties_visual)
        self.model_combobox.setGeometry(QtCore.QRect(20, 95, 120, 22))
        # fill combobox
        MC.fill_combobox(self.model_combobox, MC.get_models(
            MC.return_activated(self.building_combobox)))
        self.label_model.hide()
        self.model_combobox.hide()
        # elements only for diagram 3
        self.level_combobox_profiles = QtGui.QComboBox(self.profile_properties_visual)
        self.level_combobox_profiles.setGeometry(QtCore.QRect(200, 50, 120, 22))
        self.level_combobox_profiles.hide()
        self.rooms_combobox_profiles = QtGui.QComboBox(self.profile_properties_visual)
        self.rooms_combobox_profiles.setGeometry(QtCore.QRect(200, 95, 120, 22))
        self.rooms_combobox_profiles.hide()
        self.WP_combobox_profiles = QtGui.QComboBox(self.profile_properties_visual)
        self.WP_combobox_profiles.setGeometry(QtCore.QRect(200, 140, 120, 22))
        self.WP_combobox_profiles.hide()

        def fill_profile_comboboxes():
            MC.fill_combobox(
                self.level_combobox_profiles, MC.get_levels(
                    file=str(self.lineEdit_load_profile.text()),
                    building=str(self.lineEdit_load_profile.text().split("/")[-1].split("_")[2])))
            MC.fill_combobox(
                self.rooms_combobox_profiles, MC.get_rooms(
                    file=str(self.lineEdit_load_profile.text()),
                    building=str(self.lineEdit_load_profile.text().split("/")[-1].split("_")[2]),
                    level=str(MC.return_activated(self.level_combobox_profiles))))
            MC.fill_combobox(
                self.WP_combobox_profiles, MC.get_WPs(
                    file=str(self.lineEdit_load_profile.text()),
                    building=str(self.lineEdit_load_profile.text().split("/")[-1].split("_")[2]),
                    room=str(MC.return_activated(self.rooms_combobox_profiles))))

        ## Groupbox of Output directory Visualize Data
        self.groupBox_output = QtGui.QGroupBox(self.tab_2)
        self.groupBox_output.setGeometry(QtCore.QRect(0, 600, 591, 120))
        self.groupBox_output.setTitle(
            QtGui.QApplication.translate("MainWindow", "Output",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_Vis = QtGui.QLineEdit(self.groupBox_output)
        self.lineEdit_Vis.setGeometry(QtCore.QRect(170, 30, 380, 20))

        # self.directory_Vis = os.getcwd()+ "/Data/visualizations"
        # self.lineEdit_Vis.setText(self.directory_Vis)
        self.label_Vis = QtGui.QLabel(self.groupBox_output)
        self.label_Vis.setGeometry(QtCore.QRect(20, 30, 241, 16))
        self.label_Vis.setText(QtGui.QApplication.translate( "MainWindow", "Select the output directory",
                                                             None, QtGui.QApplication.UnicodeUTF8))
        self.dir_button_vis = QtGui.QPushButton(self.groupBox_output)
        self.dir_button_vis.setGeometry(QtCore.QRect(550, 29, 31, 22))
        self.dir_button_vis.setText(
            QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))

        self.Visualize_Button = QtGui.QPushButton(self.tab_2)
        self.Visualize_Button.setGeometry(QtCore.QRect(5, 545, 581, 41))
        self.Visualize_Button.setText(
            QtGui.QApplication.translate("MainWindow", "Visualize",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Visualize_Button.setStyleSheet("background-color: #0063b1; color: white;")
        self.Save_Button = QtGui.QPushButton(self.groupBox_output)
        self.Save_Button.setGeometry(QtCore.QRect(510, 70, 75, 41))
        self.Save_Button.setText(
            QtGui.QApplication.translate("MainWindow", "Save",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.Save_Button.setStyleSheet("background-color: #0063b1; color: white;")

        ## refresh comboboxes and lists
        self.building_combobox.activated.connect(
            lambda: MC.fill_lists(self.list_levels, MC.get_levels(
                building=MC.return_activated(self.building_combobox))))
        self.building_combobox.activated.connect(
            lambda: MC.fill_combobox(self.level_combobox, MC.get_levels(
                building=MC.return_activated(self.building_combobox))))
        self.building_combobox.activated.connect(
            lambda: MC.fill_lists(self.list_intervals, MC.get_intervals(
                building=str(MC.return_activated(self.building_combobox)))))
        self.building_combobox.activated.connect(
            lambda: MC.fill_lists(self.list_rooms, MC.get_rooms(
                building=str(MC.return_activated(self.building_combobox)),
                level=str(MC.return_activated(self.level_combobox)))))
        self.building_combobox.activated.connect(
            lambda: MC.fill_combobox(self.level_combobox, MC.get_levels(
                building=MC.return_activated(self.building_combobox))))
        self.building_combobox.activated.connect(
            lambda: MC.fill_combobox(self.rooms_combobox, MC.get_rooms(
                building=MC.return_activated(self.building_combobox),
                level=str(MC.return_activated(self.level_combobox)))))
        self.building_combobox.activated.connect(
            lambda: MC.fill_combobox(self.WP_combobox, MC.get_WPs(
                building=MC.return_activated(self.building_combobox),
                room=str(MC.return_activated(self.rooms_combobox)))))
        self.building_combobox.activated.connect(
            lambda: MC.fill_combobox(self.model_combobox, MC.get_models(
                building=MC.return_activated(self.building_combobox))))
        self.level_combobox.activated.connect(
            lambda: MC.fill_combobox(self.model_combobox, MC.get_models(
                building=MC.return_activated(self.building_combobox))))
        self.level_combobox.activated.connect(
            lambda: MC.fill_combobox(self.WP_combobox, MC.get_WPs(
                building=MC.return_activated(self.building_combobox),
                room=str(MC.return_activated(self.rooms_combobox)))))
        self.level_combobox.activated.connect(
            lambda: MC.fill_lists(self.list_rooms, MC.get_rooms(
                building=str(MC.return_activated(self.building_combobox)),
                level=str(MC.return_activated(self.level_combobox)))))
        self.level_combobox.activated.connect(
            lambda: MC.fill_combobox(self.rooms_combobox, MC.get_rooms(
                building=MC.return_activated(self.building_combobox),
                level=str(MC.return_activated(self.level_combobox)))))
        self.rooms_combobox.activated.connect(
            lambda: MC.fill_combobox(self.WP_combobox, MC.get_WPs(
                building=MC.return_activated(self.building_combobox),
                room=str(MC.return_activated(self.rooms_combobox)))))
        self.lineEdit_Vis.textChanged.connect(
            lambda: MC.fill_combobox(self.level_combobox, MC.get_levels(
                building=str(self.label_fieldtest_dyanamic.text()))))
        self.level_combobox_profiles.activated.connect(
            lambda: MC.fill_combobox(self.rooms_combobox_profiles, MC.get_rooms(
                file=str(self.lineEdit_load_profile.text()),
                building=MC.return_activated(self.building_combobox),
                level=str(MC.return_activated(self.level_combobox_profiles)))))
        self.level_combobox_profiles.activated.connect(
            lambda: MC.fill_combobox(self.WP_combobox_profiles, MC.get_WPs(
                file=str(self.lineEdit_load_profile.text()),
                building=MC.return_activated(self.building_combobox),
                room=str(MC.return_activated(self.rooms_combobox_profiles)))))
        self.rooms_combobox_profiles.activated.connect(
            lambda: MC.fill_combobox(self.WP_combobox_profiles, MC.get_WPs(
                file=str(self.lineEdit_load_profile.text()),
                building=MC.return_activated(self.building_combobox),
                room=str(MC.return_activated(self.rooms_combobox_profiles)))))

        ## opening dialog profile path
        def open_file_vis():
            self.getfiles()
            self.path = str(self.path)
            self.lineEdit_load_profile.setText(self.path)
        self.dir_button_profile_load.clicked.connect(lambda: open_file_vis())

        ## saving dialog
        def savefile():
            self.savefile()
            self.lineEdit_Vis.setText(self.path)
        self.dir_button_vis.clicked.connect(lambda: savefile())

        ## Hiding listsWidgets
        MC.hide(variables=[self.list_fieldtest_choice,
                           self.allData,
                           self.list_levels,
                           self.list_levels,
                           self.allLevels,
                           self.list_rooms,
                           self.allRooms,
                           self.label_selectFieldtest,
                           self.label_selectLevel,
                           self.label_selectRoom,
                           self.building_comparison,
                           self.level_comparison,
                           self.room_comparison,
                           self.checkbox_std])

        ## Diagram selection
        def diagram_selection(dia1=0, dia2=0, dia3=0):
            if dia1 == 1:
                self.Button_dia1.setChecked(True)
                self.Button_dia2.setChecked(False)
                self.Button_dia3.setChecked(False)
                refresh_lists()
            if dia2 == 1:
                self.Button_dia1.setChecked(False)
                self.Button_dia2.setChecked(True)
                self.Button_dia3.setChecked(False)
                refresh_lists()
            if dia3 == 1:
                self.Button_dia1.setChecked(False)
                self.Button_dia2.setChecked(False)
                self.Button_dia3.setChecked(True)
                refresh_lists()

        self.Button_dia1.clicked.connect(lambda: diagram_selection(1, 0, 0))
        self.Button_dia2.clicked.connect(lambda: diagram_selection(0, 1, 0))
        self.Button_dia3.clicked.connect(lambda: diagram_selection(0, 0, 1))

        self.building_comparison.clicked.connect(lambda: refresh_lists())
        self.level_comparison.clicked.connect(lambda: refresh_lists())
        self.room_comparison.clicked.connect(lambda: refresh_lists())
        self.lineEdit_load_profile.textChanged.connect(lambda: refresh_lists())
        self.list_fieldtest_choice.clicked.connect(lambda: refresh_lists())
        self.allData.clicked.connect(lambda: refresh_lists())
        self.allLevels.clicked.connect(lambda: refresh_lists())
        self.allRooms.clicked.connect(lambda: refresh_lists())
        self.allIntervals.clicked.connect(lambda: refresh_lists())

        ## listing all variables in "profiles properties" and "diagram typology" groupbox
        vars = [
            # buttons in diagram typology
            self.checkbox_std,
            self.building_comparison,
            self.level_comparison,
            self.room_comparison,
            self.label_lineEdit_load_profile,
            self.lineEdit_load_profile,
            self.dir_button_profile_load,

            # buttons of Diagram 1
            # all buttons of building comparison
            self.label_selectFieldtest,
            self.list_fieldtest_choice,
            self.allData,

            # all buttons of level comparison
            self.label_selectFieldtest,
            self.building_combobox,
            self.label_selectLevel,
            self.list_levels,
            self.allLevels,

            # all buttons of room comparison
            self.label_selectFieldtest,
            self.building_combobox,
            self.label_selectLevel,
            self.level_combobox,
            self.label_selectRoom,
            self.list_rooms,
            self.allRooms,

            # all butons of diagram 2
            self.label_selectFieldtest,
            self.building_combobox,
            self.label_model,
            self.model_combobox,
            self.label_selectLevel,
            self.level_combobox,
            self.label_rooms_combobox,
            self.rooms_combobox,
            self.label_WP_combobox,
            self.WP_combobox,
            self.label_intervals,
            self.list_intervals,
            self.allIntervals,

            # all buttons of diagram 3 in profile properties
            self.label_selectFieldtest,
            self.label_fieldtest_dyanamic,
            self.label_selectLevel,
            self.level_combobox_profiles,
            self.label_rooms_combobox,
            self.rooms_combobox_profiles,
            self.label_WP_combobox,
            self.WP_combobox_profiles,

            # label if no diagram is selected
            self.label_choose_diagram]

        def refresh_lists():
            if self.Button_dia1.isChecked():
                MC.show_and_hide(
                    variables=[self.building_comparison, self.level_comparison,
                               self.room_comparison, self.checkbox_std, self.checkbox_std],
                    all_variables=vars)

                ## properties if building comparison is enabeled
                if self.building_comparison.isChecked() == True:
                    MC.show_and_hide(
                        variables=[self.checkbox_std, self.building_comparison, self.level_comparison,
                                   self.room_comparison, self.label_selectFieldtest, self.list_fieldtest_choice,
                                   self.allData])
                    if self.allData.isChecked() == True:
                        self.list_fieldtest_choice.setDisabled(True)
                        for index in range(self.list_fieldtest_choice.count()):
                            self.list_fieldtest_choice.item(index).setCheckState(False)
                    else: self.list_fieldtest_choice.setEnabled(True)

                ## properties if level comparison is enabeled
                if self.level_comparison.isChecked() == True:
                    MC.show_and_hide(
                        variables=[self.checkbox_std, self.building_comparison, self.level_comparison,
                                   self.room_comparison, self.label_selectFieldtest, self.building_combobox,
                                   self.label_selectLevel, self.list_levels, self.allLevels],
                        all_variables=vars)
                    if self.allLevels.isChecked() == True:
                        self.list_levels.setDisabled(True)
                        for index in range(self.list_levels.count()):
                            self.list_levels.item(index).setCheckState(False)
                    else: self.list_levels.setEnabled(True)

                ## properties if room comparison is enabeled
                if self.room_comparison.isChecked() == True:
                    MC.show_and_hide(
                        variables=[self.checkbox_std, self.building_comparison, self.level_comparison,
                                   self.room_comparison, self.label_selectFieldtest, self.building_combobox,
                                   self.label_selectLevel, self.level_combobox, self.label_selectRoom,
                                   self.list_rooms, self.allRooms],
                        all_variables=vars)
                    if self.allRooms.isChecked() == True:
                        self.list_rooms.setDisabled(True)
                        for index in range(self.list_rooms.count()):
                            self.list_rooms.item(index).setCheckState(False)
                    else: self.list_rooms.setEnabled(True)

            elif self.Button_dia2.isChecked():
                MC.show_and_hide(
                    variables=[self.label_selectFieldtest, self.building_combobox, self.label_model,
                               self.model_combobox, self.label_selectLevel, self.level_combobox,
                               self.label_rooms_combobox, self.rooms_combobox, self.label_WP_combobox,
                               self.WP_combobox, self.label_intervals, self.list_intervals, self.allIntervals],
                    all_variables=vars)
                if self.allIntervals.isChecked() == True:
                    self.list_intervals.setDisabled(True)
                    for index in range(self.list_intervals.count()):
                        self.list_intervals.item(index).setCheckState(False)
                else:
                    self.list_intervals.setEnabled(True)

            elif self.Button_dia3.isChecked() == True:
                MC.show_and_hide(
                    variables=[self.label_lineEdit_load_profile, self.lineEdit_load_profile,
                               self.dir_button_profile_load],
                    all_variables=vars)
                if self.lineEdit_load_profile.text() != "":
                    fill_profile_comboboxes()
                    MC.show_and_hide(
                        variables=[self.label_lineEdit_load_profile, self.lineEdit_load_profile,
                                   self.dir_button_profile_load, self.label_selectFieldtest,
                                   self.label_fieldtest_dyanamic, self.label_selectLevel,
                                   self.level_combobox_profiles, self.label_rooms_combobox,
                                   self.rooms_combobox_profiles, self.label_WP_combobox, self.WP_combobox_profiles],
                        all_variables=vars)

        ## warning if no diagram is selected
        def warningselection():
            if self.Button_dia1.isChecked() == False and \
                            self.Button_dia2.isChecked() == False and \
                            self.Button_dia3.isChecked() == False:
                self.selection_popup()
        self.Visualize_Button.clicked.connect(lambda: warningselection())

        ## Function of "Visualize" Button, starting the programm
        self.Visualize_Button.clicked.connect(lambda:
            MC.visualize(self.Button_dia1,
                     self.Button_dia2,
                     self.Button_dia3,
                     self.checkbox_std,
                     self.building_comparison,
                     self.level_comparison,
                     self.room_comparison,
                     self.list_fieldtest_choice,
                     self.building_combobox,
                     self.allData,
                     self.list_levels,
                     self.level_combobox,
                     self.allLevels,
                     self.list_rooms,
                     self.allRooms,
                     self.rooms_combobox,
                     self.WP_combobox,
                     self.list_intervals,
                     self.allIntervals,
                     self.lineEdit_load_profile,
                     self.model_combobox,
                     self.level_combobox_profiles,
                     self.rooms_combobox_profiles,
                     self.WP_combobox_profiles))

        self.Save_Button.clicked.connect(lambda:
            MC.save_plot(self.Button_dia1,
                     self.Button_dia2,
                     self.Button_dia3,
                     self.checkbox_std,
                     self.building_comparison,
                     self.level_comparison,
                     self.room_comparison,
                     self.list_fieldtest_choice,
                     self.building_combobox,
                     self.allData,
                     self.list_levels,
                     self.level_combobox,
                     self.allLevels,
                     self.list_rooms,
                     self.allRooms,
                     self.rooms_combobox,
                     self.WP_combobox,
                     self.list_intervals,
                     self.allIntervals,
                     self.lineEdit_load_profile,
                     self.lineEdit_Vis,
                     self.model_combobox,
                     self.level_combobox_profiles,
                     self.rooms_combobox_profiles,
                     self.WP_combobox_profiles))

        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate(
                "MainWindow", "Visualize Data", None,  QtGui.QApplication.UnicodeUTF8))

        """
        Tab 5 - Properties (saved properties from other tabs are also mentioned here)
        """

        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName("tab_5")

        ## Groupbox to deactivate warnings
        self.warnings_groupBox = QtGui.QGroupBox(self.tab_5)
        self.warnings_groupBox.setGeometry(QtCore.QRect(0, 30, 591, 70))
        self.warnings_groupBox.setTitle(
            QtGui.QApplication.translate(
                "MainWindow", "Generate WSP", None, QtGui.QApplication.UnicodeUTF8))
        self.checkbox_overwrite = QtGui.QCheckBox(self.warnings_groupBox)
        self.checkbox_overwrite.setGeometry(QtCore.QRect(20, 28, 300, 22))
        self.checkbox_overwrite.setText(
            QtGui.QApplication.translate(
                "MainWindow", "Show warning if generated file already exists",
                None, QtGui.QApplication.UnicodeUTF8))

        ## reading and writing the database
        self.save_data = pd.read_csv(os.getcwd() +
                                     "/properties/properties.csv", delimiter=";", index_col=0)
        if int(self.save_data.get_value("Checkbox Warning","Button state")) == 1:
            self.checkbox_overwrite.setChecked(True)
        else: self.checkbox_overwrite.setChecked(False)

        if int(self.save_data.get_value("Checkbox Substitute","Button state")) == 1:
            self.substitute_button.setChecked(True)
        else: self.substitute_button.setChecked(False)

        def write_state_change_warningButton():
            if int(self.save_data.get_value("Checkbox Warning", "Button state")) == 1:
                self.save_data.set_value("Checkbox Warning", "Button state", 0)
            else:
                self.save_data.set_value("Checkbox Warning", "Button state", 1)
            self.save_data.to_csv(os.getcwd() + "/properties/properties.csv",";")

        def write_state_change_substituteButton():
            if int(self.save_data.get_value("Checkbox Substitute", "Button state")) == 1:
                self.save_data.set_value("Checkbox Substitute", "Button state", 0)
            else:
                self.save_data.set_value("Checkbox Substitute", "Button state", 1)
            self.save_data.to_csv(os.getcwd() + "/properties/properties.csv", ";")

        self.checkbox_overwrite.stateChanged.connect(lambda: write_state_change_warningButton())
        self.substitute_button.stateChanged.connect(lambda: write_state_change_substituteButton())

        # ## Groupbox of general plot Properties
        # self.plot_props_groupBox = QtGui.QGroupBox(self.tab_5)
        # self.plot_props_groupBox.setGeometry(QtCore.QRect(0, 120, 591, 300))
        # self.plot_props_groupBox.setTitle(
        #     QtGui.QApplication.translate("MainWindow", "General plot properties", None, QtGui.QApplication.UnicodeUTF8))
        # self.label_size = QtGui.QLabel(self.plot_props_groupBox)
        # self.label_size.setGeometry(QtCore.QRect(20, 40, 50, 16))
        # self.label_size.setText(
        #     QtGui.QApplication.translate("MainWindow", "Size", None, QtGui.QApplication.UnicodeUTF8))
        # self.label_resolution = QtGui.QLabel(self.plot_props_groupBox)
        # self.label_resolution.setGeometry(QtCore.QRect(20, 70, 50, 16))
        # self.label_resolution.setText(
        #     QtGui.QApplication.translate("MainWindow", "Resolution", None, QtGui.QApplication.UnicodeUTF8))
        # self.label_font = QtGui.QLabel(self.plot_props_groupBox)
        # self.label_font.setGeometry(QtCore.QRect(20, 100, 50, 16))
        # self.label_font.setText(
        #     QtGui.QApplication.translate("MainWindow", "Font", None, QtGui.QApplication.UnicodeUTF8))
        # self.label_font_size = QtGui.QLabel(self.plot_props_groupBox)
        # self.label_font_size.setGeometry(QtCore.QRect(20, 130, 50, 16))
        # self.label_font_size.setText(
        #     QtGui.QApplication.translate("MainWindow", "Font size", None, QtGui.QApplication.UnicodeUTF8))
        # self.label_font_color = QtGui.QLabel(self.plot_props_groupBox)
        # self.label_font_color.setGeometry(QtCore.QRect(20, 160, 50, 16))
        # self.label_font_color.setText(
        #     QtGui.QApplication.translate("MainWindow", "Font color", None, QtGui.QApplication.UnicodeUTF8))
        # self.label_frame_and_lines_color = QtGui.QLabel(self.plot_props_groupBox)
        # self.label_frame_and_lines_color.setGeometry(QtCore.QRect(20, 190, 50, 16))
        # self.label_frame_and_lines_color.setText(
        #     QtGui.QApplication.translate("MainWindow", "Frame and lines color", None, QtGui.QApplication.UnicodeUTF8))
        # self.label_data_colors = QtGui.QLabel(self.plot_props_groupBox)
        # self.label_data_colors.setGeometry(QtCore.QRect(20, 220, 50, 16))
        # self.label_data_colors.setText(
        #     QtGui.QApplication.translate("MainWindow", "Data Colors", None, QtGui.QApplication.UnicodeUTF8))

        self.tabWidget.addTab(self.tab_5, "")
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_5), QtGui.QApplication.translate(
                "MainWindow", "Properties", None, QtGui.QApplication.UnicodeUTF8))

        """
        Info Tab
        """

        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName("tab_6")

        self.credits_groupBox = QtGui.QGroupBox(self.tab_6)
        self.credits_groupBox.setGeometry(QtCore.QRect(0, 30, 591, 180))
        self.credits_groupBox.setTitle(
            QtGui.QApplication.translate("MainWindow", "Credits:", None, QtGui.QApplication.UnicodeUTF8))
        self.text_credits = QtGui.QLabel(self.credits_groupBox)
        self.text_credits.setGeometry(QtCore.QRect(10, 30, 600, 130))
        self.text_credits.setText(
            QtGui.QApplication.translate(
                "MainWindow",
                "Thank you for using WinProGen!\nIf you liked it, please don't forget to cite us!" 
                "\n\nYou can cite WinProGen, by citing:"
                "\n\n   D. Cali, Occupants' Behavior and its Impact upon the Energy Performance of Buildings. "
                "Dissertation, "
                "\n       Aachen, Germany, 2016."
                "\n\n\nCheck for updates @ ",
                None, QtGui.QApplication.UnicodeUTF8))
        #"\n\n   2) Davide Cali, Mark Wesseling, Dirk Mueller. WinProGen: "
        #"A Markov Chain Based Stochastic Window Status Profile Generator for the Simulation of "
        #"\n       Realistic Energy Performances of Buildings. Building and Environment, 2017."
        self.hlink = QtGui.QLabel(self.credits_groupBox)
        self.hlink.setGeometry(QtCore.QRect(116, 90, 600, 130))
        self.hlink.setStyleSheet("color: blue")
        self.hlink.setText(
            QtGui.QApplication.translate(
                "MainWindow",
                "https://git.rwth-aachen.de/lukas.schmitt/WinProGen.git",
                None, QtGui.QApplication.UnicodeUTF8))
        self.hlink.setTextFormat(Qt.RichText)
        self.hlink.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.hlink.setOpenExternalLinks(True)
        self.infos_groupBox = QtGui.QGroupBox(self.tab_6)
        self.infos_groupBox.setGeometry(QtCore.QRect(0, 230, 591, 110))
        self.infos_groupBox.setTitle(
            QtGui.QApplication.translate("MainWindow", "Infos:",
                                         None, QtGui.QApplication.UnicodeUTF8))
        self.text_infos = QtGui.QLabel(self.infos_groupBox)
        self.text_infos.setGeometry(QtCore.QRect(10, -10, 600, 130))
        self.text_infos.setText(
            QtGui.QApplication.translate(
                "MainWindow", "WinProGen is a software for the generation of stochastic window states profiles. "
                              "WinProGen is entirely"
                              "\nwritten in Python, make use of the Markov Chain technique and adopt "
                              "field test data as robust basis "
                              "\nfor the generation of the profiles. Please refer to our publications "
                              "to know the way WinProGen works. "
                              "\nIf you have any question, just contact dcali@rwth-aachen.de.",
                                         None, QtGui.QApplication.UnicodeUTF8))

        self.tabWidget.addTab(self.tab_6, "")
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_6), QtGui.QApplication.translate(
                "MainWindow", "Info", None, QtGui.QApplication.UnicodeUTF8))

    """
    Additional widgets (messagbox, directory selection, ...) & functions
    """

    def onStart_WSP(self):
        # starting progressbar for WSP function if conditions are fulfilled
        if self.popup_result == 1 and self.popup_warning == 1:
            self.myLongTask_WSP.start()

    def onProgress_WSP(self, i):
        if mD_gen_WSP.pre_wsp == "start_pulse":
            self.progressBar.setRange(0, 0)
        elif mD_gen_WSP.pre_wsp == "stop_pulse":
            self.progressBar.setRange(0, 100)
            # setting progress on WSP progressbar
            self.progressBar.setValue(i)

    def onStart_TPM(self):
        # starting progressbar pulsation for TPM function if conditions are fulfilled
        if mD_gen_TPM.check_tpm == 1:
            self.myLongTask_TPM.start()
            self.progressBar_tpm.setRange(0, 0)

    def onFinished_TPM(self):
        # Stop the pulsation
        self.progressBar_tpm.setRange(0, 100)
        # Set progressbar to 100%
        self.progressBar_tpm.setValue(100)

    def onStart_VAL(self):
        # starting progressbar for VAL function if conditions are fulfilled
        if self.popup_warning == 1:
            self.myLongTask_val.start()

    def onProgress_VAL(self, i):
        if mD_gen_VAL.pre_wsp == "start_pulse":
            self.progressBar_val.setRange(0, 0)
        elif mD_gen_VAL.pre_wsp == "stop_pulse":
            self.progressBar_val.setRange(0, 100)
            # setting progress on VAL progressbar
            self.progressBar_val.setValue(i)

    def update_simDays(self):
        # calculating simulation days if start or final date is changed in the GUI
        self.simulationdays = (self.finalDate.date().toPyDate() - self.startDate.date().toPyDate()).days + 1
        mD_gen_WSP.simDays = self.simulationdays

    def update_val_horizon(self):
        # updating the validation horizon if it is changed in the GUI
        mD_val.val_horizon = MC.return_int(self.integer_number_horizon)

    def profiles_popup(self):
        # warning in case of "Profile Selection" is choosed but no profile is selected
        choice = QtGui.QMessageBox.warning(self, 'Warning!',
                                            "No profile selected. \nPlease select a profile!", QtGui.QMessageBox.Ok)
        if choice == QtGui.QMessageBox.Ok:
            self.popup_warning = 0
            self.popup_warning_val = 0

    def selection_popup(self):
        # warning in case no diagram is selected
        choice = QtGui.QMessageBox.warning(self, "Warning!", "No diagram selected. \nPlease select a diagram!",
                                           QtGui.QMessageBox.Ok)
        if choice == QtGui.QMessageBox.Ok: self.selection_warning = 0

    def warning_popup(self):
        # waring in case user is about to overwrite a file
        choice = QtGui.QMessageBox.warning(self, "Warning!", "You are about to overwrite a file. \nAre you sure?",
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes: self.popup_result = 1
        else: self.popup_result = 0

    def warnings_tpm(self):
        # waring messages for TPM Tab
        if self.lineEdit_fileselect_tpm.text() == "":
            wrng = QtGui.QMessageBox.warning(self, "Warning!", "No file selected. \nPlease select a file!",
                                               QtGui.QMessageBox.Ok)
        if self.lineEdit_name_tpm.text() == "":
            wrng = QtGui.QMessageBox.warning(self, "Warning!",
                                             "No fieldtest name selected. \nPlease select a fieldtest name!",
                                             QtGui.QMessageBox.Ok)
        if self.lineEdit_temperatures_tpm.text() == "":
            wrng = QtGui.QMessageBox.warning(self, "Warning!",
                                             "No temperature range selected. \nPlease select a temperature range!",
                                             QtGui.QMessageBox.Ok)
        if "_" in self.lineEdit_name_tpm.text():
            wrng = QtGui.QMessageBox.warning(self, "Warning!", "Forbidden char in filename. \nUsage of \"_\" is not allowed!",
                                             QtGui.QMessageBox.Ok)
        if self.lineEdit_name_tpm.text().count(",") >= 2:
            wrng = QtGui.QMessageBox.warning(self, "Warning!", "Number of Temperature intervals below minimum. \nGive a minimum of 3 temperatures!",
                                             QtGui.QMessageBox.Ok)

    def getfiles(self):
        # dialog to open files
        filter = "CSV (*.csv);;DAT (*.dat)"
        self.path = QtGui.QFileDialog().getOpenFileNameAndFilter(self, "Open files",
                                                                 os.getcwd(), filter)
        self.path = str(self.path).split("u'")[1].split("')")[0]

    def openfile(self):
        # dialog to open Original file for TPM generation
        self.path = QtGui.QFileDialog().getOpenFileNameAndFilter(self, "Open files",
                                                                 os.getcwd(), "CSV (*.csv)")
        self.path = str(self.path).split("u'")[1].split("')")[0]

    def savefile(self):
        # dialog for saving file as PDF or PNG
        filter = "PNG (*.png);;PDF (*.pdf)"
        self.path = QtGui.QFileDialog().getSaveFileNameAndFilter(self, "Save files",
                                                                 os.getcwd(), filter)
        self.path = str(self.path).split("u'")[1].split("')")[0]

    def openfolder(self):
        # output directory selection for WSP generation
        self.directory = QtGui.QFileDialog.getExistingDirectory(self, 'Open directory',
                                                                os.getcwd())

    def generate_WSP(self):
        # outsourcing function of the "Generate" button (in WSP Tab), avoiding interrupted GUI
        if self.popup_result == 1 and self.popup_warning == 1:
            worker = Worker_Generate_WSP(self.Data_Choice_combobox,
                                         self.profile_choice_files,
                                         self.Button_RandomChoice,
                                         self.int_random_files,
                                         self.Button_ProfileChoice,
                                         self.Button_allProfiles,
                                         self.startDate, self.finalDate,
                                         self.lineEdit_path,
                                         self.lineEdit_filename,
                                         self.TRY_Choice_combobox,
                                         self.Button_SelectM1,
                                         self.Button_SelectM2,
                                         self.Button_SelectM3,
                                         self.substitute_button)
            self.threadpool.start(worker)

    def generate_TPM(self):
        # outsourcing function of the "Generate" button (in TPM Tab), avoiding interrupted GUI
        if mD_gen_TPM.check_tpm == 1:
            worker = Worker_Generate_TPM(self.Button_SelectM1_tpm,
                                         self.Button_SelectM2_tpm,
                                         self.Button_SelectM3_tpm,
                                         self.lineEdit_fileselect_tpm,
                                         self.lineEdit_name_tpm,
                                         self.lineEdit_temperatures_tpm,
                                         self.wp_choice)
            self.threadpool.start(worker)

    def validate(self):
        # outsourcing function of the "Validation" button (in VAL Tab), avoiding interrupted GUI
        if self.popup_warning == 1:
            worker = Worker_Validate(self.Data_Choice_combobox_val,
                                     self.profile_choice_files_val,
                                     self.Button_RandomChoice_val,
                                     self.int_random_files_val,
                                     self.Button_ProfileChoice_val,
                                     self.Button_allProfiles_val,
                                     self.TRY_Choice_combobox_val,
                                     self.Button_SelectM1_val,
                                     self.Button_SelectM2_val,
                                     self.Button_SelectM3_val,
                                     self.integer_number_horizon)
            self.threadpool.start(worker)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app_icon = QtGui.QIcon()
    app_icon.addFile(os.getcwd() + "/icons/logo_square.png", QtCore.QSize(16, 16))
    app.setWindowIcon(app_icon)
    app.setStyleSheet('QMainWindow{background-color: #bfbfbf; border: 1px solid black;}')
    ui = MW()
    ui.show()
    sys.exit(app.exec_())


