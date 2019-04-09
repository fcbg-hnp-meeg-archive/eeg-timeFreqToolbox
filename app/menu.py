from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from matplotlib.pyplot import close, show
from app.menu_UI import Ui_MenuWindow
from backend.util import blockPrint, enablePrint


"""
File containing the main window class, ie the window for selectionning
the path of the dataset, choose the parameters for computing the PSD etc.
"""

class MenuWindow(QMainWindow) :
    def __init__(self) :
        super(MenuWindow, self).__init__(parent = None)
        self.setWindowTitle("Open PSD Visualize")
        self.ui = Ui_MenuWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.setup_ui()

    #=====================================================================
    # Setup and Initialization functions
    #=====================================================================
    def setup_ui(self) :
        """Setup the ui with initial values and bindings"""
        self.set_boxes()
        self.set_bindings()
        self.init_psd_parameters()
        self.init_tfr_parameters()
        self.filePath = ['']
        self.dataType = None
        self.selected_ch = []
        self.montage = None

    #------------------------------------------------------------------------
    def set_bindings(self) :
        """Set all the bindings"""
        (self.ui.psdButton.clicked
        .connect(self.open_psd_visualizer))

        (self.ui.tfrButton.clicked
        .connect(self.open_tfr_visualizer))

        (self.ui.pathButton.clicked
        .connect(self.choose_eeg_path))

        (self.ui.savePsdButton.clicked
        .connect(self.choose_save_path))

        (self.ui.plotData.clicked
        .connect(self.plot_data))

        (self.ui.displayDataButton.clicked
        .connect(self.display_data_infos))

        (self.ui.psdParametersButton.clicked
        .connect(self.choose_psd_parameters_path))

        (self.ui.tfrParametersButton.clicked
        .connect(self.choose_tfr_parameters_path))

        (self.ui.lineEdit.editingFinished
        .connect(self.eeg_path_changed))

        (self.ui.psdParametersLine.editingFinished
        .connect(self.psd_parameters_path_changed))

        (self.ui.psdMethod.currentIndexChanged
        .connect(self.init_psd_parameters))

        (self.ui.tfrMethodBox.currentIndexChanged
        .connect(self.init_tfr_parameters))

        (self.ui.epochingButton.clicked
        .connect(self.open_epoching_window))

        (self.ui.electrodeMontage.currentTextChanged
        .connect(self.choose_xyz_path))

        (self.ui.pushButton.clicked
        .connect(self.open_channel_picker))

    #------------------------------------------------------------------------
    def set_boxes(self) :
        """
        Set the values of the combo boxes for file extension,
        coordinates and fourier methods
        """
        for extension in ['.fif','-epo.fif','.sef', '.ep', '.eph'] :
            self.ui.chooseFileType.addItem(extension)

        for method in ['No coordinates', 'Use xyz file',
                       'standard_1005', 'standard_1020'] :
            self.ui.electrodeMontage.addItem(method)

        self.ui.psdMethod.addItem('multitaper')
        self.ui.psdMethod.addItem('welch')
        self.ui.tfrMethodBox.addItem('multitaper')
        self.ui.tfrMethodBox.addItem('stockwell')
        self.ui.tfrMethodBox.addItem('morlet')

    #---------------------------------------------------------------------
    def init_psd_parameters(self) :
        """Set the parameters in the parameters text slot"""

        text = "fmin=0\nfmax=100\ntmin=Default\ntmax=Default\n"

        if self.ui.psdMethod.currentText() == 'welch' :
            text = text + "n_fft=Default\nn_per_seg=Default\nn_overlap=0"

        if self.ui.psdMethod.currentText() == 'multitaper' :
            text = text + "bandwidth=4"

        self.ui.psdParametersText.setText(text)

    #---------------------------------------------------------------------
    def init_tfr_parameters(self) :
        """Set the parameters in the parameters text slot"""
        text = "fmin=5\nfmax=100"
        if self.ui.tfrMethodBox.currentText() == 'multitaper' :
            text = text + "\nfreq_step=1\ntime_window=0.5\ntime_bandwidth=4"
        if self.ui.tfrMethodBox.currentText() == 'morlet' :
            text = text + "\nfreq_step=1\ntime_window=0.5"
        if self.ui.tfrMethodBox.currentText() == 'stockwell' :
            text = text + "\nwidth=1\nn_fft=Default"
        self.ui.tfrParametersText.setText(text)

    #=====================================================================
    # Reading and setting up data
    #=====================================================================
    def read_eeg_data(self, path) :
        """Read the eeg data depending on the file"""
        extension = self.ui.chooseFileType.currentText()

        blockPrint() #Just to block printing from init functions

        if extension == '.fif' :
            from mne.io import read_raw_fif
            self.dataType = 'raw'
            self.eeg_data = read_raw_fif(path)

        elif extension == '-epo.fif' :
            from mne import read_epochs
            self.dataType = 'epochs'
            self.eeg_data = read_epochs(path)

        elif extension == '.ep' :
            from backend.read import read_ep
            self.dataType = 'raw'
            self.eeg_data = read_ep(path)

        elif extension == '.eph' :
            from backend.read import read_eph
            self.dataType = 'raw'
            self.eeg_data = read_eph(path)

        elif extension == '.sef' :
            from backend.read import read_sef
            self.dataType = 'raw'
            self.eeg_data = read_sef(path)

        else :
            raise ValueError("Invalid Format")

        enablePrint()

    #---------------------------------------------------------------------
    def read_montage(self) :
        """Read the montage data"""

        montage = self.ui.electrodeMontage.currentText()

        if montage == 'Use xyz file' :
            from backend.util import xyz_to_montage
            self.montage = xyz_to_montage(self.ui.xyzPath.text())
            self.eeg_data.set_montage(self.montage)

        elif montage != 'No coordinates' :
            from mne.channels import read_montage
            ch_names = self.eeg_data.info['ch_names']
            self.montage = read_montage(montage)
            self.eeg_data.set_montage(self.montage)

    #---------------------------------------------------------------------
    def init_picks(self) :
        """Init list with picks"""
        try :
            picked_ch = [self.eeg_data.info['ch_names'].index(name)
                         for name in self.selected_ch]
            if len(picked_ch) == 0 :
                return None
            else :
                return picked_ch
        except :
            self.show_error('Please initialize the EEG data before '
                            + 'proceeding.')

    #---------------------------------------------------------------------
    def read_parameters(self, tfr = False) :
        """Read parameters from txt file and sets it up in params"""
        if tfr :
            text = self.ui.tfrParametersText.toPlainText()
        else :
            text = self.ui.psdParametersText.toPlainText()
        params = text.replace(" ", "").split('\n')
        dic = {}
        try :
            for param in params :
                param, val = param.replace(" ", "").split("=")
                if val == 'Default' or val == 'None' : dic[param] = None
                else :
                    val = val.split(",")
                    if len(val) == 1 :
                        dic[param] = val[0]
                    else :
                        dic[param] = [e for e in val]

        except ValueError :
                self.show_error("Format of parameters must be "
                                + "param_id = values")
        self.params = dic

    #---------------------------------------------------------------------
    def plot_data(self) :
        """Initialize the data and plot the data on a matplotlib window"""
        try :
            self.read_parameters()
            close('all')
            self.eeg_data.plot(scalings = 'auto')
            show()
        except (AttributeError, FileNotFoundError, OSError) :
            self.show_error("Can't find/read file\n"
                            + "Please verify the path and extension")
        except (ValueError) :
            self.show_error("Names of electrodes don't fit convention")

    #=====================================================================
    # Open epoching window
    #=====================================================================
    def open_epoching_window(self) :
        """Open epoching window"""
        from app.epoching import EpochingWindow

        window = EpochingWindow()
        window.exec_()

    #=====================================================================
    # Open PSD Visualizer
    #=====================================================================
    def open_psd_visualizer(self) :
        """Redirect to PSD Visualize app"""
        try :
            self.read_parameters()

        except (AttributeError, FileNotFoundError, OSError) :
            self.show_error("Can't find/read file.\n"
                            + "Please verify the path and extension")
        else :
            if self.dataType == 'epochs' :
                self.open_epochs_psd_visualizer()
            elif self.dataType == 'raw' :
                self.open_raw_psd_visualizer()
            else :
                self.show_error("Please initialize the EEG data "
                                + "before proceeding.")

    #---------------------------------------------------------------------
    def init_nfft(self) :
        """Init the n_fft parameter"""
        from backend.util import int_

        n_fft    = int_(self.params.get('n_fft', None))
        if n_fft is None :
            if self.dataType == 'raw' :
                 n_fft = self.eeg_data.n_times
            if self.dataType == 'epochs' :
                n_fft = len(self.eeg_data.times)
        return n_fft

    #---------------------------------------------------------------------
    def init_epochs_psd(self) :
        """Initialize the instance of EpochsPSD"""
        from backend.epochs_psd import EpochsPSD
        from backend.util import float_, int_

        blockPrint() #Just to block printing from init functions

        if self.ui.psdMethod.currentText() == 'welch' :
            n_fft = self.init_nfft()
            self.psd = EpochsPSD(self.eeg_data,
                                 fmin       = float_(self.params['fmin']),
                                 fmax       = float_(self.params['fmax']),
                                 tmin       = float_(self.params['tmin']),
                                 tmax       = float_(self.params['tmax']),
                                 method     = 'welch',
                                 n_fft      = n_fft,
                                 n_per_seg  = int_(self.params
                                                   .get('n_per_seg', n_fft)),
                                 n_overlap  = int_(self.params
                                                   .get('n_overlap', 0)),
                                 picks      = self.init_picks(),
                                 montage    = self.montage)

        if self.ui.psdMethod.currentText() == 'multitaper' :
            self.psd = EpochsPSD(self.eeg_data,
                                 fmin       = float_(self.params['fmin']),
                                 fmax       = float_(self.params['fmax']),
                                 tmin       = float_(self.params['tmin']),
                                 tmax       = float_(self.params['tmax']),
                                 method     = 'multitaper',
                                 bandwidth  = float_(self.params
                                                     .get('bandwidth', 4)),
                                 picks      = self.init_picks(),
                                 montage    = self.montage)

        enablePrint()

    #---------------------------------------------------------------------
    def init_raw_psd(self) :
        """Initialize the instance of RawPSD"""
        from backend.raw_psd import RawPSD
        from backend.util import float_, int_

        blockPrint() #Just to block printing from init functions

        if self.ui.psdMethod.currentText() == 'welch' :
            n_fft = self.init_nfft()
            self.psd = RawPSD(self.eeg_data,
                              fmin       = float_(self.params['fmin']),
                              fmax       = float_(self.params['fmax']),
                              tmin       = float_(self.params['tmin']),
                              tmax       = float_(self.params['tmax']),
                              method     = 'welch',
                              n_fft      = n_fft,
                              n_per_seg  = int_(self.params
                                                .get('n_per_seg', n_fft)),
                              n_overlap  = int_(self.params
                                                .get('n_overlap', 0)),
                              picks      = self.init_picks(),
                              montage    = self.montage)

        if self.ui.psdMethod.currentText() == 'multitaper' :
            self.psd = RawPSD(self.eeg_data,
                              fmin       = float_(self.params['fmin']),
                              fmax       = float_(self.params['fmax']),
                              tmin       = float_(self.params['tmin']),
                              tmax       = float_(self.params['tmax']),
                              method     = 'multitaper',
                              bandwidth  = int(self.params
                                               .get('bandwidth', 4)),
                              picks      = self.init_picks(),
                              montage    = self.montage)

        enablePrint()

    #---------------------------------------------------------------------
    def open_epochs_psd_visualizer(self) :
        """Open PSD visualizer for epochs data"""
        from app.epochs_psd import EpochsPSDWindow

        self.init_epochs_psd()
        psdVisualizer = EpochsPSDWindow(self.psd)
        psdVisualizer.show()

    #---------------------------------------------------------------------
    def open_raw_psd_visualizer(self) :
        """Open PSD Visualizer for raw type data"""
        from app.raw_psd import RawPSDWindow

        self.init_raw_psd()
        psdVisualizer = RawPSDWindow(self.psd)
        psdVisualizer.show()

    #=====================================================================
    # Open TFR Visualizer
    #=====================================================================
    def init_ncycles(self, freqs) :
        """Init the n_cycles parameter"""
        from backend.util import float_

        # Handling of the time window parameter for multitaper and morlet method
        n_cycles = 0
        if self.ui.tfrMethodBox.currentText() != "stockwell" :
            n_cycles = float_(self.params.get('n_cycles', None))
            if n_cycles is None :
                time_window = float_(self.params.get('time_window', None))
                if time_window is None :
                    self.show_error('Please specify a number of cycles,'
                                    + ' or a time_window parameter')
                    raise ValueError("Not enough parameters found")
                else :
                    n_cycles = freqs * time_window
        return n_cycles

    #---------------------------------------------------------------------
    def init_avg_tfr(self) :
        """Init tfr from parameters"""
        from backend.avg_epochs_tfr import AvgEpochsTFR
        from backend.util import float_, int_
        from numpy import arange

        fmin     = float_(self.params['fmin'])
        fmax     = float_(self.params['fmax'])
        step     = float_(self.params.get('freq_step', 1))
        freqs    = arange(fmin, fmax, step)
        n_cycles = self.init_ncycles(freqs)
        n_fft    = int_(self.params.get('n_fft', None))

        try : picks = self.init_picks()
        except : self.show_error("404, a name was not found :(")

        try :
            self.avgTFR = AvgEpochsTFR(self.eeg_data, freqs, n_cycles,
                method         = self.ui.tfrMethodBox.currentText(),
                time_bandwidth = float_(self.params.get('time_bandwidth', 4)),
                width          = float_(self.params.get('width', 1)),
                n_fft          = n_fft,
                picks          = picks)
        except ValueError :
            self.show_error("Time-Window or n_cycles is too high for"
                            + "the length of the signal :(\n"
                            + "Please use a smaller Time-Window"
                            + " or less cycles.")
        except AttributeError :
            self.show_error("Please initialize the EEG data before"
                            + " proceeding.")
        else :
            if picks is None :
                self.show_infos("All channels selected."
                                + " Computing may be long")

    #---------------------------------------------------------------------
    def open_tfr_visualizer(self) :
        """Open TFR Visualizer for epochs"""
        from app.avg_epochs_tfr import AvgTFRWindow

        try :
            self.read_parameters(tfr=True)
        except (AttributeError, FileNotFoundError, OSError) :
            self.show_error("Can't find/read file.\n"
                            + "Please verify the path and extension")
        else :
            self.init_avg_tfr()
            psdVisualizer = AvgTFRWindow(self.avgTFR)
            psdVisualizer.show()

    #=====================================================================
    #Choosing different path
    #=====================================================================
    def choose_eeg_path(self) :
        """Open window for choosing eeg path and updates the line"""
        self.filePath, _ = QFileDialog.getOpenFileNames(
                                self,"Choose data path", "")
        if len(self.filePath) > 1 :
            from os.path import dirname
            path = 'Batch processing in : ' + dirname(self.filePath[0])
        elif len(self.filePath) == 1 :
            path = self.filePath[0]
        else :
            path = ''
        self.ui.lineEdit.setText(path)
        self.eeg_path_changed()

    #---------------------------------------------------------------------
    def eeg_path_changed(self) :
        """Gets called when eeg path is changed and reads the data"""
        if len(self.filePath) != 0 :
            extension = self.filePath[0].split("-")[-1].split('.')
        else :
            extension = ['']

        if extension[0] == 'epo' :
             extension = '-epo.fif'
        else :
            extension = '.' + extension[-1]

        if len(self.filePath) != 0 :
            try :
                index = self.ui.chooseFileType.findText(extension)
                self.ui.chooseFileType.setCurrentIndex(index)
                self.read_eeg_data(self.filePath[0])
            except :
                self.show_error("Cannot read eeg data :(\n"
                                + "Please verifiy the path and extension")

    #---------------------------------------------------------------------
    def choose_psd_parameters_path(self) :
        """Open window for choosing PSD parameters path"""
        self.psdParametersPath, _ = QFileDialog.getOpenFileName(
                                        self,"Choose Parameters", "")
        self.ui.psdParametersLine.setText(self.psdParametersPath)
        try :
            (self.ui.psdParametersText
                .setText(open(self.psdParametersPath, 'r').read()))
        except :
            self.show_error('Path to parameters not found :(')

    #---------------------------------------------------------------------
    def choose_tfr_parameters_path(self) :
        """Open window for choosing TFR parameters path"""
        self.tfrParametersPath, _ = QFileDialog.getOpenFileName(
                                        self,"Choose Parameters", "")
        (self.ui.tfrParametersLine
            .setText(self.tfrParametersPath))
        (self.ui.tfrParametersText
            .setText(open(self.tfrParametersPath, 'r').read()))

    #---------------------------------------------------------------------
    def psd_parameters_path_changed(self) :
        """Gets called when PSD parameters are changed"""
        self.psdParametersPath = self.ui.psdParametersLine.text()
        try :
            (self.ui.psdParametersText
                .setText(open(self.psdParametersPath, 'r').read()))
        except :
            self.show_error('Path to parameters not found :(')

    #---------------------------------------------------------------------
    def choose_xyz_path(self) :
        """Gets called when electrode montage box is updated"""
        try :
            if self.ui.electrodeMontage.currentText() == 'Use xyz file' :
                self.xyzPath, _ = QFileDialog.getOpenFileName(
                                      self,"Choose .xyz file", "")
                self.ui.xyzPath.setText(self.xyzPath)
                self.read_montage()
            else :
                self.ui.xyzPath.setText('')
                self.read_montage()

        except AttributeError :
            index = self.ui.electrodeMontage.findText('No coordinates')
            self.ui.electrodeMontage.setCurrentIndex(index)
            self.show_error("Please initialize the EEG"
                            + " data before proceeding.")
        except :
            self.show_error("Cannot read .xyz file :(")
            index = self.ui.electrodeMontage.findText('No coordinates')
            self.ui.electrodeMontage.setCurrentIndex(index)

    #=====================================================================
    # Saving
    #=====================================================================
    def choose_save_path(self) :
        """Open window for choosing save path"""
        if len(self.filePath) == 1 :
            self.savepath, _ = QFileDialog.getSaveFileName(self)
        else :
            self.savepath = QFileDialog.getExistingDirectory(self)

        try :
            self.read_parameters()
        except (AttributeError, FileNotFoundError, OSError) :
            self.show_error("Can't find/read file :(\n"
                            + "Please verify the path and extension")
        else :
            self.save_matrix()

    #---------------------------------------------------------------------
    def save_matrix(self) :
        """Save the matrix containing the PSD"""

        try :
            n_files = len(self.filePath)
            if n_files == 1 :
                print('Saving one file ...', end = '')
                blockPrint()
                if self.dataType == 'epochs' :
                    self.init_epochs_psd()
                if self.dataType == 'raw'    :
                    self.init_raw_psd()
                enablePrint()
                self.psd.save_avg_matrix_sef(self.savepath)
                print('done !')

            else :
                from os.path import basename, splitext, join

                print('Batch Processing of {} files'
                      .format(len(self.filePath)))
                n = 1
                for path in self.filePath :
                    print('Saving file {} out of {} ...'
                          .format(n, n_files), end = '')
                    blockPrint()
                    file_name = splitext(basename(path))[0]
                    self.read_eeg_data(path)
                    if self.dataType == 'epochs' :
                        self.init_epochs_psd()
                    if self.dataType == 'raw' :
                        self.init_raw_psd()

                    savepath = join(self.savepath, file_name + '-PSD.sef')
                    self.psd.save_avg_matrix_sef(savepath)
                    enablePrint()
                    print('done !')
                    n+=1

        except (AttributeError, FileNotFoundError, OSError) :
            self.show_error("Can't find/read a file.\n"
                + "Please verify the path and extension")
        except :
            self.show_error("An error occured ...")

    #=====================================================================
    # Display data informations
    #=====================================================================
    def display_data_infos(self) :
        """Display informations about data on a pop-up window"""
        try :
            self.read_parameters()
            self.show_infos(self.init_info_string())
        except (AttributeError, FileNotFoundError, OSError) :
            self.show_error("Can't find/read file :(\n"
                            + "Please verify the path and extension")

    # ---------------------------------------------------------------------
    def init_info_string(self) :
        """Init a string with informations about data"""
        sfreq      = self.eeg_data.info["sfreq"]
        n_channels = self.eeg_data.info["nchan"]
        infos1     = "Sampling Frequency:{}\nNumber of Channels : {}".format(
                     sfreq, n_channels)
        if self.dataType == 'raw' :
            n_times = self.eeg_data.n_times
            infos2 = "\nTime points:{}".format(n_times)
            infos3 = "\nDuration of the signal:{0:.2f}s".format(
                         (n_times / sfreq))

        if self.dataType == 'epochs' :
            times  = self.eeg_data.times
            infos2 = "\nTime points per Epoch:{}".format(len(times))
            infos3 = "\nDuration of the signal:{0:.2f}s".format(
                         times[-1] - times[0])

        return infos1 + infos2 + infos3

    #=====================================================================
    # Channel picker
    #=====================================================================
    def open_channel_picker(self) :
        """Open the channel picker"""
        from app.select_channels import PickChannels
        try :
            channels = self.eeg_data.info['ch_names']
            picker = PickChannels(self, channels, self.selected_ch)
            picker.exec_()
        except :
            self.show_error("Please initialize the EEG data"
                            + " before proceeding.")

    #---------------------------------------------------------------------
    def set_selected_ch(self, selected) :
        """Set selected channels"""
        self.selected_ch = selected
        self.ui.displayChannel.setText(",".join(selected))

    #=====================================================================
    # Pop up windows for error and informations
    #=====================================================================
    def show_error(self, msg) :
        """Display window with an error message"""
        error = QMessageBox()
        error.setBaseSize(QSize(800, 200))
        error.setIcon(QMessageBox.Warning)
        error.setInformativeText(msg)
        error.setWindowTitle("Error")
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()

    #---------------------------------------------------------------------
    def show_infos(self, msg) :
        """Display a window with an information message"""
        info = QMessageBox()
        info.setBaseSize(QSize(800, 200))
        info.setIcon(QMessageBox.Information)
        info.setText("Data informations")
        info.setInformativeText(msg)
        info.setWindowTitle("Data Informations")
        info.exec_()
