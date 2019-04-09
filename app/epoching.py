import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg \
    import NavigationToolbar2QT as NavigationToolbar

from app.epoching_UI import EpochingWindowUI

class EpochingWindow(QDialog):
    def __init__(self, parent=None):
        super(EpochingWindow, self).__init__(parent)
        self.ui = EpochingWindowUI()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.setup_ui()

    #=====================================================================
    # Setup functions
    #=====================================================================
    def setup_ui(self) :
        """Call all of the setup functions"""
        self.set_bindings()
        self.set_boxes()
        self.set_values()

    #------------------------------------------------------------------------
    def set_bindings(self) :
        """Setup the bindings of Button"""
        self.ui.rawPathButton.clicked.connect(self.choose_raw_path)
        self.ui.mrkPathButton.clicked.connect(self.choose_mrk_path)
        self.ui.plotRawButton.clicked.connect(self.plot_raw)
        self.ui.plotMrkButton.clicked.connect(self.plot_events)
        self.ui.mrkLine.editingFinished.connect(self.set_mrk_box)
        self.ui.saveEpochsButton.clicked.connect(self.choose_save_path)
        self.ui.visuEpochsButton.clicked.connect(self.plot_epochs)

    #------------------------------------------------------------------------
    def set_boxes(self) :
        """Setup the boxes for file extensions"""
        self.ui.rawBox.addItem(".sef")
        self.ui.rawBox.addItem(".fif")
        self.ui.mrkBox.addItem(".mrk")
        self.ui.mrkBox.addItem("-eve.fif")

    #------------------------------------------------------------------------
    def set_values(self) :
        """Set default values"""
        self.ui.tmin.setText('-0.5')
        self.ui.tmin.setMaxLength(5)
        self.ui.tmax.setText('0.5')
        self.ui.tmax.setMaxLength(5)

    #------------------------------------------------------------------------
    def set_mrk_box(self) :
        """Set the marker box"""
        try :
            self.read_events()
        except :
            print("ERROR")
        else :
            self.ui.chooseMrkBox.clear()
            for item in self.events.get_labels() :
                self.ui.chooseMrkBox.addItem(item)

    #=====================================================================
    # Path settings
    #=====================================================================
    def choose_raw_path(self) :
        """Gets called when choosing raw path"""
        self.rawPath, _ = QFileDialog.getOpenFileName(
            self,"Choose data path", "Raw Data (*.fif, *.sef)")
        self.ui.rawLine.setText(self.rawPath)
        self.ui.mrkLine.setText(self.rawPath + '.mrk')

    #------------------------------------------------------------------------
    def choose_mrk_path(self) :
        """Gets called when choosing marker path"""
        self.mrkPath, _ = QFileDialog.getOpenFileName(
            self,"Choose markers path", "mrk files (*.mrk)")
        self.ui.mrkLine.setText(self.mrkPath)
        self.set_mrk_box()

    #=====================================================================
    # Reading data functions
    #=====================================================================
    def read_raw(self) :
        """Set-up the raw data in mne class"""
        extension = self.ui.rawBox.currentText()
        self.rawPath = self.ui.rawLine.text()
        if extension == '.fif' :
            from mne.io import read_raw_fif
            self.raw = read_raw_fif(self.rawPath)

        if extension == '.sef' :
            from backend.read import read_sef
            self.raw = read_sef(self.rawPath)

    #------------------------------------------------------------------------
    def read_events(self) :
        """Set up the events in correct class"""
        extension = self.ui.mrkBox.currentText()
        self.mrkPath = self.ui.mrkLine.text()
        if extension == '.fif' :
            return 0
        if extension == '.mrk' :
            from backend.events import Events
            self.events = Events(self.mrkPath)

    #=====================================================================
    # Data Visualization
    #=====================================================================
    def plot_raw(self) :
        """
        Initialize the raw eeg data and plot the data on a
        matplotlib window
        """
        try :
            self.read_raw()
        except (AttributeError, FileNotFoundError, OSError) :
            self.show_error("Can't find/read file\n"
                            + "Please verify the path and extension")
        else :
            plt.close('all')
            self.raw.plot(scalings = 'auto')
            plt.show()

    #------------------------------------------------------------------------
    def plot_events(self) :
        """
        Initialize the events data and plot the data on a matplotlib window
        """
        try :
            self.read_events()
        except (AttributeError, FileNotFoundError, OSError) :
            self.show_error("Can't find/read file\n"
                            + "Please verify the path and extension")
        else :
            plt.close('all')
            self.events.plot()
            plt.show()

    #=====================================================================
    # Saving the data
    #=====================================================================
    def init_epochs(self) :
        """
        Save epochs as -epo.fif file
        """
        label = self.ui.chooseMrkBox.currentText()
        tmin = float(self.ui.tmin.text())
        tmax = float(self.ui.tmax.text())
        return self.events.compute_epochs(label, self.raw, tmin, tmax)

    #------------------------------------------------------------------------
    def choose_save_path(self) :
        self.savePath, _ = QFileDialog.getSaveFileName(self)
        try :
            self.read_raw()
            self.read_events()
        except (AttributeError, FileNotFoundError, OSError) :
            self.show_error("Can't find/read file.\n"
                            + "Please verify the path and extension")
        else :
            self.init_epochs().save(self.savePath)

    #------------------------------------------------------------------------
    def plot_epochs(self) :
        try :
            self.read_raw()
            self.read_events()
        except (AttributeError, FileNotFoundError, OSError) :
            self.show_error("Can't find/read file.\n"
                            + "Please verify the path and extension")
        else :
            epochs = self.init_epochs()
            plt.close('all')
            epochs.plot(scalings = 'auto')
            plt.show()

    #=====================================================================
    # Error handling
    #=====================================================================
    def show_error(self, msg) :
        error = QMessageBox()
        error.setIcon(QMessageBox.Warning)
        error.setText("Error")
        error.setInformativeText(msg)
        error.setWindowTitle("Error")
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
