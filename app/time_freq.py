from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from app.ui.time_freq_UI import Ui_TimeFreq


class TimeFreq(QMainWindow):
    """Main Window for time-frequency
    """
    def __init__(self, parent=None):
        super(TimeFreq, self).__init__(parent)
        self.ui = Ui_TimeFreq()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.setup_ui()

    # Setup functions for UI
    # ========================================================================
    def setup_ui(self):
        self.filePaths = ['']
        self.type = None
        self.selected_ch = []
        self.montage = None
        self.set_bindings()
        self.setup_boxes()
        self.init_parameters()

    # ---------------------------------------------------------------------
    def setup_boxes(self):
        """Setup the boxes with names"""
        self.ui.psdMethod.addItem('welch')
        self.ui.psdMethod.addItem('multitaper')
        self.ui.tfrMethodBox.addItem('morlet')
        self.ui.tfrMethodBox.addItem('multitaper')
        self.ui.tfrMethodBox.addItem('stockwell')

    # ---------------------------------------------------------------------
    def set_bindings(self):
        """Set the bindings
        """
        (self.ui.pathButton.clicked
         .connect(self.choose_data_path))

        (self.ui.plotButton.clicked
         .connect(self.plot_data))

        (self.ui.psdMethod.currentIndexChanged
         .connect(self.init_parameters))

        (self.ui.tfrMethodBox.currentIndexChanged
         .connect(self.init_parameters))

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

    # Data path and Data handling functions
    # ========================================================================
    def choose_data_path(self):
        """Open window for choosing data path and updates the line
        """
        from os.path import dirname
        try:
            self.filePaths, _ = QFileDialog.getOpenFileNames(
                                        self, 'Choose data path', '')
            self.ui.pathLine.setText(dirname(self.filePaths[0]))

            if len(self.filePaths) > 1:
                self.ui.pathLine.setText(
                    dirname(self.filePaths[0]) + ':: Multiple files')
        except Exception as e:
            print(e)
            print('Error while trying to read data')
        else:
            self.set_data_box()
            self.data_box_changed()

    # ---------------------------------------------------------------------
    def read_data(self):
        """Reads the data from path
        """
        index = self.ui.dataFilesBox.currentIndex()
        if self.filePaths[index].endswith('-epo.fif'):
            from mne import read_epochs
            self.type = 'epochs'
            self.data = read_epochs(self.filePaths[index])
            print('Epoch file initialized')
        elif self.filePaths[index].endswith('.fif'):
            from mne.io import read_raw_fif
            self.type = 'raw'
            self.data = read_raw_fif(self.filePaths[index])
            print('Raw file initialized')
        else:
            raise TypeError("Type not handled")

    # ---------------------------------------------------------------------
    def set_data_box(self):
        """Initialize the combo box with the names
        """
        from os.path import basename

        self.ui.dataFilesBox.clear()
        for path in self.filePaths:
            self.ui.dataFilesBox.addItem(basename(path))

    # ---------------------------------------------------------------------
    def data_box_changed(self):
        """Re-initialize the data when the value in the box is changed
        """
        from backend.util import eeg_to_montage
        try:
            self.read_data()
            self.set_informations()
            self.montage = eeg_to_montage(self.data)
            self.selected_ch = [name for name in self.data.info['ch_names']]
        except TypeError:
            print("File not handled")

    # ---------------------------------------------------------------------
    def plot_data(self):
        """Plot the data
        """
        from matplotlib.pyplot import close, show
        try:
            close('all')
            self.data.plot(block=True, scalings='auto')
            show()
        except AttributeError:
            print('No data initialized')

    # ---------------------------------------------------------------------
    def set_informations(self):
        """Set informations in the information label
        """
        from backend.util import init_info_string
        self.ui.infoLabel.setText(init_info_string(self.data))

    # Parameters initialization
    # ========================================================================
    def init_parameters(self):
        """Init the parameters in the text editor
        """
        from backend.time_freq import \
            _init_psd_parameters, _init_tfr_parameters

        _init_psd_parameters(self)
        _init_tfr_parameters(self)

    # Channel picking functions
    # ========================================================================
    def open_channel_picker(self):
        """Open the channel picker
        """
        from app.select_channels import PickChannels
        channels = self.data.info['ch_names']
        picker = PickChannels(self, channels, self.selected_ch)
        picker.exec_()

    # ---------------------------------------------------------------------
    def set_selected_ch(self, selected):
        """Set selected channels
        """
        self.selected_ch = selected

    # Open PSD Visualizer
    # ========================================================================
    def open_psd_visualizer(self):
        """Redirect to PSD Visualize app
        """
        try:
            from backend.time_freq import _read_parameters
            _read_parameters(self)

        except (AttributeError, FileNotFoundError, OSError):
            print('Cannot find/read Parameters.\n'
                  + 'Please verify the path and extension')
        else:
            if self.type == 'epochs':
                from backend.time_freq import _open_epochs_psd_visualizer
                _open_epochs_psd_visualizer(self)
            elif self.type == 'raw':
                from backend.time_freq import _open_raw_psd_visualizer
                _open_raw_psd_visualizer(self)
            else:
                print('Please initialize the EEG data '
                      + 'before proceeding.')

    # Open TFR Visualizer
    # ========================================================================
    def open_tfr_visualizer(self):
        """Open TFR Visualizer for epochs
        """
        try:
            from backend.time_freq import _read_parameters
            _read_parameters(self, True)

        except (AttributeError, FileNotFoundError, OSError):
            print('Cannot find/read file.\n'
                  + 'Please verify the path and extension')
        else:
            from backend.time_freq import _open_tfr_visualizer
            _open_tfr_visualizer(self)

    # Saving
    # ========================================================================
    def choose_save_path(self):
        """Open window for choosing save path
        """
        if len(self.filePaths) == 1:
            self.savepath, _ = QFileDialog.getSaveFileName(self)
        else:
            self.savepath = QFileDialog.getExistingDirectory(self)

        try:
            self.read_parameters()
        except (AttributeError, FileNotFoundError, OSError):
            print('Cannot find/read file:(\n'
                  + 'Please verify the path and extension')
        else:
            self.save_matrix()

    # ---------------------------------------------------------------------
    def save_matrix(self):
        """Save the matrix containing the PSD
        """
        from backend.time_freq import _save_matrix
        _save_matrix(self)
