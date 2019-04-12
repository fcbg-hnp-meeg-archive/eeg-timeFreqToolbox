from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from app.time_freq_UI import Ui_TimeFreq
from backend.util import blockPrint, enablePrint

class TimeFreq(QMainWindow):
    def __init__(self, parent=None):
        super(TimeFreq, self).__init__(parent)
        self.ui = Ui_TimeFreq()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.setup_ui()

    #---------------------------------------------------------------------
    def setup_ui(self) :
        self.filePaths = ['']
        self.type = None
        self.selected_ch = []
        self.montage = None
        self.set_bindings()
        self.setup_boxes()
        self.init_psd_parameters()
        self.init_tfr_parameters()

    #---------------------------------------------------------------------
    def setup_boxes(self) :
        """Setup the boxes with names"""
        self.ui.psdMethod.addItem('multitaper')
        self.ui.psdMethod.addItem('welch')
        self.ui.tfrMethodBox.addItem('multitaper')
        self.ui.tfrMethodBox.addItem('stockwell')
        self.ui.tfrMethodBox.addItem('morlet')

    #---------------------------------------------------------------------
    def set_bindings(self) :
        """Set the bindings"""
        (self.ui.pathButton.clicked
        .connect(self.choose_data_path))

        (self.ui.plotButton.clicked
        .connect(self.plot_data))

        (self.ui.psdMethod.currentIndexChanged
        .connect(self.init_psd_parameters))

        (self.ui.tfrMethodBox.currentIndexChanged
        .connect(self.init_tfr_parameters))

        (self.ui.channelButton.clicked
        .connect(self.open_channel_picker))

        (self.ui.dataFilesBox.currentIndexChanged
        .connect(self.data_box_changed))

        (self.ui.psdButton.clicked
        .connect(self.open_psd_visualizer))

        (self.ui.tfrButton.clicked
        .connect(self.open_tfr_visualizer))

        (self.ui.savePsdButton.clicked
        .connect(self.choose_save_path))

    #---------------------------------------------------------------------
    def choose_data_path(self) :
        """Open window for choosing data path and updates the line"""
        try :
            self.filePaths, _ = QFileDialog.getOpenFileNames(
                                        self,"Choose data path", "")
            self.ui.pathLine.setText(self.filePaths[0])

            if len(self.filePaths) > 1 :
                from os.path import dirname
                self.ui.pathLine.setText(
                    dirname(self.filePaths[0]) + ' :: Multiple files')
        except :
            print('error while trying to read data')
        else :
            from backend.util import eeg_to_montage

            self.set_data_box()
            self.read_data()
            self.set_informations()
            self.montage = eeg_to_montage(self.data)
            self.selected_ch = [name for name in self.data.info['ch_names']]

    #---------------------------------------------------------------------
    def read_data(self) :
        """Reads the data from path"""
        index = self.ui.dataFilesBox.currentIndex()
        try :
            if self.filePaths[0].endswith('-epo.fif') :
                from mne import read_epochs
                self.type = 'epochs'
                self.data = read_epochs(self.filePaths[index])
                print("Epoch file initialized")
            else :
                from mne.io import read_raw_fif
                self.type = 'raw'
                self.data = read_raw_fif(self.filePaths[index])
                print("Raw file initialized")
        except :
            print("Can't read the file")

    #---------------------------------------------------------------------
    def set_data_box(self) :
        """Initialize the combo box with the name"""
        from os.path import basename

        self.ui.dataFilesBox.clear()
        for path in self.filePaths :
            self.ui.dataFilesBox.addItem(basename(path))

    #---------------------------------------------------------------------
    def data_box_changed(self) :
        """Re-initialize the data when the value in the box is changed"""
        from backend.util import eeg_to_montage

        self.read_data()
        self.set_informations()
        self.montage = eeg_to_montage(self.data)
        self.selected_ch = [name for name in self.data.info['ch_names']]

    #---------------------------------------------------------------------
    def plot_data(self) :
        """Plot the data"""
        from matplotlib.pyplot import close, show
        try :
            close('all')
            self.data.plot(block = True, scalings = 'auto')
            show()
        except AttributeError :
            print('No data initialized')

    #---------------------------------------------------------------------
    def set_informations(self) :
        from backend.util import init_info_string
        self.ui.infoLabel.setText(init_info_string(self.data))

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

    #---------------------------------------------------------------------
    # Channel picking functions
    #---------------------------------------------------------------------
    def open_channel_picker(self) :
        """Open the channel picker"""
        from app.select_channels import PickChannels
        channels = self.data.info['ch_names']
        picker = PickChannels(self, channels, self.selected_ch)
        picker.exec_()

    #---------------------------------------------------------------------
    def set_selected_ch(self, selected) :
        """Set selected channels"""
        self.selected_ch = selected

    #---------------------------------------------------------------------
    def init_picks(self) :
        """Init list with picks"""
        try :
            picked_ch = [self.data.info['ch_names'].index(name)
                         for name in self.selected_ch]
            if len(picked_ch) == 0 :
                return None
            else :
                return picked_ch
        except :
            print('Please initialize the EEG data before '
                            + 'proceeding.')

    #---------------------------------------------------------------------
    # Open PSD Visualizer
    #---------------------------------------------------------------------
    def open_psd_visualizer(self) :
        """Redirect to PSD Visualize app"""
        try :
            self.read_parameters()

        except (AttributeError, FileNotFoundError, OSError) :
            print("Can't find/read Parameters.\n"
                  + "Please verify the path and extension")
        else :
            if self.type == 'epochs' :
                self.open_epochs_psd_visualizer()
            elif self.type == 'raw' :
                self.open_raw_psd_visualizer()
            else :
                print("Please initialize the EEG data "
                                + "before proceeding.")

    #---------------------------------------------------------------------
    def init_nfft(self) :
        """Init the n_fft parameter"""
        from backend.util import int_

        n_fft    = int_(self.params.get('n_fft', None))
        if n_fft is None :
            if self.type == 'raw' :
                 n_fft = self.data.n_times
            if self.type == 'epochs' :
                n_fft = len(self.data.times)
        return n_fft

    #---------------------------------------------------------------------
    def init_epochs_psd(self) :
        """Initialize the instance of EpochsPSD"""
        from backend.epochs_psd import EpochsPSD
        from backend.util import float_, int_

        if self.ui.psdMethod.currentText() == 'welch' :
            n_fft = self.init_nfft()
            self.psd = EpochsPSD(self.data,
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
            self.psd = EpochsPSD(self.data,
                                 fmin       = float_(self.params['fmin']),
                                 fmax       = float_(self.params['fmax']),
                                 tmin       = float_(self.params['tmin']),
                                 tmax       = float_(self.params['tmax']),
                                 method     = 'multitaper',
                                 bandwidth  = float_(self.params
                                                     .get('bandwidth', 4)),
                                 picks      = self.init_picks(),
                                 montage    = self.montage)

    #---------------------------------------------------------------------
    def init_raw_psd(self) :
        """Initialize the instance of RawPSD"""
        from backend.raw_psd import RawPSD
        from backend.util import float_, int_

        if self.ui.psdMethod.currentText() == 'welch' :
            n_fft = self.init_nfft()
            self.psd = RawPSD(self.data,
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
            self.psd = RawPSD(self.data,
                              fmin       = float_(self.params['fmin']),
                              fmax       = float_(self.params['fmax']),
                              tmin       = float_(self.params['tmin']),
                              tmax       = float_(self.params['tmax']),
                              method     = 'multitaper',
                              bandwidth  = float_(self.params
                                               .get('bandwidth', 4)),
                              picks      = self.init_picks(),
                              montage    = self.montage)

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


    #---------------------------------------------------------------------
    # Open TFR Visualizer
    #---------------------------------------------------------------------
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

        picks = self.init_picks()

        try :
            self.avgTFR = AvgEpochsTFR(
                self.data, freqs, n_cycles,
                method         = self.ui.tfrMethodBox.currentText(),
                time_bandwidth = float_(self.params.get('time_bandwidth', 4)),
                width          = float_(self.params.get('width', 1)),
                n_fft          = n_fft,
                picks          = picks)

        except ValueError :
            print("Time-Window or n_cycles is too high for"
                  + "the length of the signal :(\n"
                  + "Please use a smaller Time-Window"
                  + " or less cycles.")

        except AttributeError :
            print("Please initialize the EEG data before"
                  + " proceeding.")

    #---------------------------------------------------------------------
    def open_tfr_visualizer(self) :
        """Open TFR Visualizer for epochs"""
        from app.avg_epochs_tfr import AvgTFRWindow

        try :
            self.read_parameters(tfr=True)
        except (AttributeError, FileNotFoundError, OSError) :
            print("Can't find/read file.\n"
                            + "Please verify the path and extension")
        else :
            self.init_avg_tfr()
            psdVisualizer = AvgTFRWindow(self.avgTFR)
            psdVisualizer.show()


    #---------------------------------------------------------------------
    # Read Parameters function
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
                if val == 'Default' or val == 'None' :
                    dic[param] = None
                else :
                        dic[param] = val

        except ValueError :
                self.show_error("Format of parameters must be "
                                + "param_id = values")
        self.params = dic


    #---------------------------------------------------------------------
    # Saving
    #---------------------------------------------------------------------
    def choose_save_path(self) :
        """Open window for choosing save path"""
        if len(self.filePaths) == 1 :
            self.savepath, _ = QFileDialog.getSaveFileName(self)
        else :
            self.savepath = QFileDialog.getExistingDirectory(self)

        try :
            self.read_parameters()
        except (AttributeError, FileNotFoundError, OSError) :
            print("Can't find/read file :(\n"
                            + "Please verify the path and extension")
        else :
            self.save_matrix()

    #---------------------------------------------------------------------
    def save_matrix(self) :
        """Save the matrix containing the PSD"""

        n_files = len(self.filePaths)
        if n_files == 1 :
            print('Saving one file ...', end = '')
            if self.type == 'epochs' :
                self.init_epochs_psd()
            if self.type == 'raw'    :
                self.init_raw_psd()
            self.psd.save_avg_matrix_sef(self.savepath)
            print('done !')

        else :
            from os.path import basename, splitext, join

            print('Batch Processing of {} files'
                  .format(len(self.filePaths)))
            n = 0
            for path in self.filePaths :
                print('Saving file {} out of {} ...'
                      .format(n+1, n_files), end = '')
                file_name = splitext(basename(path))[0]
                self.ui.dataFilesBox.setCurrentIndex(0)
                if self.type == 'epochs' :
                    self.init_epochs_psd()
                if self.type == 'raw' :
                    self.init_raw_psd()

                savepath = join(self.savepath, file_name + '-PSD.sef')
                self.psd.save_avg_matrix_sef(savepath)
                print('done !')
                n+=1
