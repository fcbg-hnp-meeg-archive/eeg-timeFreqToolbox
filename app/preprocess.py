from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg as FigureCanvas

from app.preprocess_UI import Ui_PreprocessWindow

class PreprocessWindow(QMainWindow) :
    def __init__(self) :
        super(PreprocessWindow, self).__init__(parent = None)
        self.setWindowTitle("Preprocessing")
        self.ui = Ui_PreprocessWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.setup_ui()

    #---------------------------------------------------------------------
    # Setup of the UI functions
    #---------------------------------------------------------------------
    def setup_ui(self) :
        """Setup the ui with initial values and bindings"""
        self.set_preview_canvas()
        self.set_bindings()
        self.set_boxes()
        self.filePath = ['']
        self.dataType = None
        self.selected_ch = []
        self.montage = None
        self.bads = []

    #---------------------------------------------------------------------
    def set_preview_canvas(self) :
        """setup canvas for matplotlib"""
        import matplotlib.pyplot as plt
        self.ui.figurePreview = plt.figure()
        self.ui.figurePreview.patch.set_facecolor('None')
        self.ui.preview = FigureCanvas(self.ui.figurePreview)
        self.ui.preview.setStyleSheet("background-color:transparent;")
        self.ui.previewLayout.addWidget(self.ui.preview)

    #---------------------------------------------------------------------
    def set_bindings(self) :
        (self.ui.pathButtonData.clicked
        .connect(self.choose_data_path))

        (self.ui.dataFilesBox.currentIndexChanged
        .connect(self.data_box_changed))

        (self.ui.plotDataButton.clicked
        .connect(self.plot_data))

        (self.ui.initDataButton.clicked
        .connect(self.plot_init_data))

        (self.ui.showMontageButton.clicked
        .connect(self.plot_montage))

        (self.ui.montageBox.currentIndexChanged
        .connect(self.read_montage))

        (self.ui.refBox.currentIndexChanged
        .connect(self.ref_box_changed))

    #---------------------------------------------------------------------
    def set_boxes(self) :
        """Set the combo boxes"""
        types = ['standard_1020', 'standard_1005', 'Use xyz file']
        for type in types :
            self.ui.montageBox.addItem(type)

        for type in ['accurate', 'fast'] :
            self.ui.interpBox.addItem(type)

        for type in ['No referencing', 'average', 'Multiple Channels'] :
            self.ui.refBox.addItem(type)

    #---------------------------------------------------------------------
    def data_box_changed(self) :
        """Re-initialize the data when the value in the box is changed"""
        from backend.preprocess import _read_data
        _read_data(self)

    #---------------------------------------------------------------------
    def set_data_box(self) :
        """Initialize the combo box with the names"""
        from os.path import basename

        self.ui.dataFilesBox.clear()
        for path in self.filePaths :
            self.ui.dataFilesBox.addItem(basename(path))

    #---------------------------------------------------------------------
    # Choose Path for data
    #---------------------------------------------------------------------
    def choose_data_path(self) :
        """Open window for choosing data path and updates the line"""
        from os.path import dirname
        from backend.preprocess import _read_data

        self.filePaths, _ = QFileDialog.getOpenFileNames(
                                self,"Choose data path", "")
        path = dirname(self.filePaths[0])
        self.ui.pathLineData.setText(path)
        self.set_data_box()   #Also calls _read_data

    #---------------------------------------------------------------------
    def plot_init_data(self) :
        from matplotlib.pyplot import close, show

        try :
            close('all')
            self.data.plot(scalings = 'auto')
            show(block = True)

        except AttributeError :
            print('No data initialized')

    #---------------------------------------------------------------------
    def plot_data(self) :
        """Plot the processed data"""
        from matplotlib.pyplot import close, show
        from backend.preprocess import _apply_preprocess

        _apply_preprocess(self)
        try :
            close('all')
            self.processed_data.plot(scalings = 'auto')
            show(block = True)

        except AttributeError :
            print('No data initialized')

    #---------------------------------------------------------------------
    # Plot Montage
    #---------------------------------------------------------------------
    def read_montage(self) :
        """Read the montage data"""

        montage = self.ui.montageBox.currentText()

        if montage == 'Use xyz file' :
            from backend.util import xyz_to_montage
            xyzPath, _ = QFileDialog.getOpenFileName(
                                    self,"Choose data path", "")
            self.montage = xyz_to_montage(xyzPath)

        elif montage == 'Imported from file' :
            pass

        elif montage != 'No coordinates' :
            from mne.channels import read_montage
            self.montage = read_montage(montage)

    #---------------------------------------------------------------------
    def plot_montage(self) :
        from matplotlib.pyplot import close, show

        data = self.data.copy()
        bads = self.processed_data.info['bads']
        data.info['bads'] = bads

        if self.ui.montageBox.currentText() != "Imported from file" :
            data.set_montage(self.montage)

        close('all')
        data.plot_sensors(show_names = True)
        show()

    #---------------------------------------------------------------------
    # Data changed
    #---------------------------------------------------------------------
    def ref_box_changed(self) :
        if self.ui.refBox.currentText() == 'Multiple Channels' :
            from app.select_channels import PickChannels

            pick = PickChannels(self, self.data.info['ch_names'])
            pick.exec_()

    #---------------------------------------------------------------------
    def set_selected_ch(self, selected) :
        self.selected_ch = selected
