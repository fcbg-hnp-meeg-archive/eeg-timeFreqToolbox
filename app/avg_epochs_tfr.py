from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg \
    import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from app.avg_epochs_tfr_UI import Ui_AvgTFRWindow

class AvgTFRWindow(QDialog):
    def __init__(self, avgTFR, parent=None):
        super(AvgTFRWindow, self).__init__(parent)
        self.avg = avgTFR
        self.ui = Ui_AvgTFRWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.setup()

    #=====================================================================
    # Setup functions
    #=====================================================================
    def setup(self) :
        self.set_canvas()
        self.set_box()
        self.set_line_edit()
        self.set_bindings()
        self.set_slider()
        self.plot_changed()

    #---------------------------------------------------------------------
    def set_canvas(self) :
        """setup canvas for matplotlib"""
        self.ui.figure = plt.figure(figsize = (10,10))
        self.ui.figure.patch.set_facecolor('None')
        self.ui.canvas = FigureCanvas(self.ui.figure)
        self.ui.canvas.setStyleSheet("background-color:transparent;")
        # Matplotlib toolbar
        self.ui.toolbar = NavigationToolbar(self.ui.canvas, self)
        self.ui.matplotlibLayout.addWidget(self.ui.toolbar)
        self.ui.matplotlibLayout.addWidget(self.ui.canvas)

    #---------------------------------------------------------------------
    def set_line_edit(self) :
        """Sets up scaling line edit"""
        self.vmax = None
        self.ui.lineEdit.setText("0")
        self.ui.lineEdit.setMaxLength(6)

    #---------------------------------------------------------------------
    def set_box(self) :
        """Setup box names"""
        self.ui.displayBox.addItem("Time-Frequency plot")
        self.ui.displayBox.addItem("Channel-Frequency plot")
        self.ui.displayBox.addItem("Channel-Time plot")
        self.plotType = "Time-Frequency plot"

    #---------------------------------------------------------------------
    def set_slider(self) :
        """Setup the main slider"""
        self.index = self.ui.mainSlider.value()
        self.ui.mainSlider.setMinimum(0)
        self.update_slider()

    #---------------------------------------------------------------------
    def set_bindings(self) :
        """Set the bindings"""
        self.ui.lineEdit.editingFinished.connect(self.scaling_changed)
        self.ui.displayBox.currentIndexChanged.connect(self.plot_changed)
        self.ui.mainSlider.valueChanged.connect(self.index_changed)

    #=====================================================================
    # Updating functions
    #=====================================================================
    def plot_changed(self) :
        """Get called when the method is changed"""
        self.plotType = self.ui.displayBox.currentText()
        self.update_slider()
        self.plot()

    #---------------------------------------------------------------------
    def index_changed(self) :
        """Gets called when the index is changed"""
        self.index = self.ui.mainSlider.value()
        self.plot()

    #---------------------------------------------------------------------
    def scaling_changed(self) :
        """Gets called when scaling is changed"""
        self.vmax = float(self.ui.lineEdit.text())
        if self.vmax == 0 : self.vmax = None
        self.plot()

    #---------------------------------------------------------------------
    def update_slider(self) :
        """Update Maximum of the slider"""
        self.ui.mainSlider.setValue(0)
        if self.plotType == "Time-Frequency plot" :
            self.ui.mainSlider.setMaximum(self.avg.tfr.data.shape[0] - 1)
            self.ui.mainLabel.setText('Channels')
        if self.plotType == "Channel-Frequency plot" :
            self.ui.mainSlider.setMaximum(self.avg.tfr.data.shape[2] - 1)
            self.ui.mainLabel.setText('Times')
        if self.plotType == "Channel-Time plot" :
            self.ui.mainSlider.setMaximum(self.avg.tfr.data.shape[1] - 1)
            self.ui.mainLabel.setText('Frequencies')
        self.ui.mainSlider.setTickInterval(1)
        self.plot()

    #=====================================================================
    # Plotting functions
    #=====================================================================
    def plot(self) :
        """Plot the correct representation"""
        if self.plotType == "Time-Frequency plot" :
            self.plot_time_freq()
        if self.plotType == "Channel-Frequency plot" :
            self.plot_freq_ch()
        if self.plotType == "Channel-Time plot" :
            self.plot_time_ch()

    #---------------------------------------------------------------------
    def plot_time_freq(self) :
        """Plot the time-frequency representation"""
        self.ui.figure.clear()
        ax = self.ui.figure.add_subplot(1, 1, 1)
        self.cbar_image = self.avg.plot_time_freq(
            self.index, ax, vmax = self.vmax)
        ax.set_title("Time-Frequency Plot - Channel {}".format(
                     self.avg.info['ch_names'][self.avg.picks[self.index]]),
                     fontsize = 15, fontweight = 'light')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Frequencies (Hz)')
        self.add_colorbar([0.915, 0.15, 0.01, 0.7])
        self.ui.figure.subplots_adjust(top = 0.85, right = 0.8,
                                       left = 0.1, bottom = 0.1)
        self.ui.canvas.draw()

    #---------------------------------------------------------------------
    def plot_freq_ch(self) :
        """Plot the frequency-channel representation"""
        self.ui.figure.clear()
        ax = self.ui.figure.add_subplot(1, 1, 1)
        self.cbar_image = self.avg.plot_freq_ch(
            self.index, ax, vmax = self.vmax)
        ax.set_title(("Frequency-Channel Plot - Time {:.2f}s"
                     .format(self.avg.tfr.times[self.index])),
                     fontsize = 15, fontweight = 'light')
        ax.set_xlabel('Frequencies (Hz)')
        ax.set_ylabel('Channels')
        ax.set_yticks([i for i in range(1,len(self.avg.picks)+1)])
        ax.set_yticklabels(self.avg.picks)
        self.add_colorbar([0.915, 0.15, 0.01, 0.7])
        self.ui.figure.subplots_adjust(top = 0.85, right = 0.8,
                                       left = 0.1, bottom = 0.1)
        self.ui.canvas.draw()

    #---------------------------------------------------------------------
    def plot_time_ch(self) :
        """Plot the time-channels representation"""
        self.ui.figure.clear()
        ax = self.ui.figure.add_subplot(1, 1, 1)
        self.cbar_image = self.avg.plot_time_ch(
            self.index, ax, vmax = self.vmax)
        ax.set_title(("Time-Channel Plot - Frequency {:.2f}"
                      .format(self.avg.tfr.freqs[self.index])),
                     fontsize = 15, fontweight = 'light')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Channels')
        ax.set_yticks([i for i in range(1,len(self.avg.picks)+1)])
        ax.set_yticklabels(self.avg.picks)
        self.add_colorbar([0.915, 0.15, 0.01, 0.7])
        self.ui.figure.subplots_adjust(top = 0.85, right = 0.8,
                                       left = 0.1, bottom = 0.1)
        self.ui.canvas.draw()

    #---------------------------------------------------------------------
    def add_colorbar(self, position) :
        """ Add colorbar to the plot at correct position """
        cax = self.ui.figure.add_axes(position)
        cbar = plt.colorbar(self.cbar_image, cax = cax)
        cbar.ax.get_xaxis().labelpad = 15
        cbar.ax.set_xlabel('Power')
