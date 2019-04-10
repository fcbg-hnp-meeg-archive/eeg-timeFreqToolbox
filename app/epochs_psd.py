from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from math import floor

from app.epochs_psd_UI import Ui_EpochsPSDWindow

"""
File containing the PSDWindow class, which enable to visualize the PSDs
"""
class EpochsPSDWindow(QDialog):
    def __init__(self, epochsPSD, parent=None):
        super(EpochsPSDWindow, self).__init__(parent)
        self.psd = epochsPSD
        self.ui = Ui_EpochsPSDWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.setup_window()

    #---------------------------------------------------------------------
    def setup_window(self) :
        """Call all the setup functions"""
        self.set_canvas()
        self.set_initial_values()
        self.set_bindings()
        self.plot_change()

    #=====================================================================
    # Setup functions
    #=====================================================================
    def set_initial_values(self) :
        """Setup initial values"""
        self.ui.epochsSlider.setMaximum(self.psd.data.shape[0] - 1)
        self.ui.epochsSlider.setMinimum(0)
        self.ui.epochsSlider.setValue(0)
        self.ui.epochsSlider.setTickInterval(1)
        self.ui.frequencySlider.setMaximum(len(self.psd.freqs) - 1)
        self.ui.frequencySlider.setMinimum(0)
        self.ui.frequencySlider.setValue(0)
        self.ui.frequencySlider.setTickInterval(1)
        self.ui.fmin.setMaxLength(4)
        self.ui.fmin.setText(str(self.psd.freqs[0]))
        self.ui.fmax.setMaxLength(4)
        self.ui.fmax.setText(str(self.psd.freqs[-1]))
        self.ui.vmax.setText("0")
        self.ui.vmax.setMaxLength(6)
        self.ui.showMean.setCheckState(2)
        self.ui.selectPlotType.addItem("PSD Matrix")
        self.ui.selectPlotType.addItem("Topomap")

    #---------------------------------------------------------------------
    def set_bindings(self) :
        """Set Bindings"""
        self.ui.epochsSlider.valueChanged.connect(self.value_changed)
        self.ui.frequencySlider.valueChanged.connect(self.slider_changed)
        self.ui.fmin.editingFinished.connect(self.value_changed)
        self.ui.fmax.editingFinished.connect(self.value_changed)
        self.ui.showMean.stateChanged.connect(self.value_changed)
        self.ui.displayLog.stateChanged.connect(self.value_changed)
        self.ui.showSingleEpoch.stateChanged.connect(self.value_changed)
        self.ui.vmax.editingFinished.connect(self.value_changed)
        self.ui.selectPlotType.currentIndexChanged.connect(self.plot_change)

    #---------------------------------------------------------------------
    def set_canvas(self) :
        """setup canvas for matplotlib"""
        self.ui.figure = plt.figure(figsize = (10,10))
        self.ui.figure.patch.set_facecolor('None')
        self.ui.canvas = FigureCanvas(self.ui.figure)
        self.ui.canvas.setStyleSheet("background-color:transparent;")
        cid = self.ui.canvas.mpl_connect('button_press_event', self.onclick)
        self.cursor = ()
        # Matplotlib toolbar
        self.ui.toolbar = NavigationToolbar(self.ui.canvas, self)
        self.ui.figureLayout.addWidget(self.ui.toolbar)
        self.ui.figureLayout.addWidget(self.ui.canvas)

    #=====================================================================
    # Main Plotting function
    #=====================================================================
    def plot_psd(self, epoch_index, f_index_min, f_index_max, vmax) :
        """Plot the correct type of PSD"""
        if self.plotType == "Topomap" :
            try :
                self.plot_topomaps(epoch_index,
                                   f_index_min, f_index_max, vmax)
            except : #If no topomap is initialized, there is an error ...
                self.show_error(
                    "No coordinates for topomap have been initialized :(")
                self.ui.selectPlotType.setCurrentIndex(0)
        if self.plotType == "PSD Matrix" :
            self.plot_matrix(epoch_index, f_index_min, f_index_max, vmax)

    #---------------------------------------------------------------------
    def plot_topomaps(self, epoch_index, f_index_min, f_index_max, vmax):
        """Plot the topomaps"""
        self.ui.figure.clear()
        self.topomaps_adjust(epoch_index, f_index_min, f_index_max, vmax)
        self.add_colorbar([0.915, 0.15, 0.01, 0.7])
        self.ui.figure.subplots_adjust(top = 0.9, right = 0.8,
                                       left = 0.1, bottom = 0.1)
        self.ui.canvas.draw()

    #---------------------------------------------------------------------
    def plot_matrix(self, epoch_index, f_index_min, f_index_max, vmax) :
        """Plot the PSD Matrix"""
        self.ui.figure.clear()
        self.matrix_adjust(epoch_index, f_index_min, f_index_max, vmax)
        self.add_colorbar([0.915, 0.15, 0.01, 0.7])
        self.ui.figure.subplots_adjust(top = 0.85, right = 0.8,
                                       left = 0.1, bottom = 0.1)
        self.ui.canvas.draw()

    #=====================================================================
    # Updating the canvas functions
    #=====================================================================
    def plot_change(self) :
        """Update the plot type"""
        self.plotType = self.ui.selectPlotType.currentText()
        self.value_changed()

    #---------------------------------------------------------------------
    def value_changed(self) :
        """ Get called if a value is changed """
        fmin = float(self.ui.fmin.text())
        fmax = float(self.ui.fmax.text())
        self.vmax = float(self.ui.vmax.text())
        self.log = self.ui.displayLog.checkState()
        self.vmin = 0

        if self.log : self.vmin = None
        if self.vmax == 0 and not self.log : self.vmax = None

        self.f_index_min, self.f_index_max = self.get_index_freq(fmin ,fmax)
        epoch_index = self.ui.epochsSlider.value()
        self.plot_psd(epoch_index, self.f_index_min, self.f_index_max,
                      self.vmax)

    #---------------------------------------------------------------------
    def slider_changed(self) :
        """Get called when the slider is touched"""
        freq_index = self.ui.frequencySlider.value()
        freq = self.psd.freqs[freq_index]
        self.ui.fmin.setText(str(freq))
        self.ui.fmax.setText(str(freq))
        self.value_changed()

    #=====================================================================
    # Adjusting the plots
    #=====================================================================
    def topomaps_adjust(self, epoch_index, f_index_min, f_index_max, vmax) :
        """Plot the good number of subplots and update cbar_image instance"""

        if (self.ui.showMean.checkState()
                and self.ui.showSingleEpoch.checkState()) :
            nbFrames = 2
        else : nbFrames = 1

        # Plot single epoch if showSingleEpoch is checked
        if self.ui.showSingleEpoch.checkState() :
            ax = self.ui.figure.add_subplot(1, nbFrames, 1)
            self.cbar_image, _ = self.psd.plot_topomap_band(
                                    epoch_index, f_index_min, f_index_max,
                                    axes = ax, vmin = self.vmin, vmax = vmax,
                                    log_display = self.log)

            ax.set_title("Epoch {}".format(epoch_index + 1),
                         fontsize = 15, fontweight = 'light')

        # plot average data if showMean is checked
        if self.ui.showMean.checkState() :
            ax = self.ui.figure.add_subplot(1, nbFrames, nbFrames)
            self.cbar_image, _ = self.psd.plot_avg_topomap_band(
                                    f_index_min, f_index_max, axes = ax,
                                    vmin = self.vmin, vmax = vmax,
                                    log_display = self.log)

            ax.set_title("Average", fontsize = 15, fontweight = 'light')

    #---------------------------------------------------------------------
    def matrix_adjust(self, epoch_index, f_index_min, f_index_max, vmax) :
        """Plot the matrix and update cbar_image instance """
        if (self.ui.showMean.checkState()
                and self.ui.showSingleEpoch.checkState()) :
            nbFrames = 2
        else : nbFrames = 1

        # plot single epoch data uf showSingleEpoch is checked
        if self.ui.showSingleEpoch.checkState() :
            ax = self.ui.figure.add_subplot(1, nbFrames, 1)
            self.cbar_image = self.psd.plot_matrix(
                                  epoch_index, f_index_min, f_index_max,
                                  vmin = self.vmin, vmax = vmax,
                                  axes = ax, log_display = self.log)
            ax.axis('tight')
            ax.set_title("PSD Matrix for epoch {}".format(epoch_index + 1),
                         fontsize = 15, fontweight = 'light')
            ax.set_xlabel('Frequencies (Hz)')
            ax.set_ylabel('Channels')
            ax.xaxis.set_ticks_position('bottom')

        # plot average data if showMean is checked
        if self.ui.showMean.checkState() :
            ax = self.ui.figure.add_subplot(1, nbFrames, nbFrames)
            self.cbar_image = self.psd.plot_avg_matrix(
                                  f_index_min, f_index_max, axes = ax,
                                  vmin = self.vmin, vmax = vmax,
                                  log_display = self.log)
            ax.axis('tight')
            ax.set_title("Average PSD Matrix", fontsize = 15,
                         fontweight = 'light')
            ax.set_xlabel('Frequencies (Hz)')
            ax.set_ylabel('Channels')
            ax.xaxis.set_ticks_position('bottom')

    #---------------------------------------------------------------------
    def add_colorbar(self, position) :
        """ Add colorbar to the plot at correct position """
        if (self.ui.showSingleEpoch.checkState()
                or self.ui.showMean.checkState()) :
            # plot a common colorbar for both representations
            cax = self.ui.figure.add_axes(position)
            cbar = plt.colorbar(self.cbar_image, cax = cax)
            cbar.ax.get_xaxis().labelpad = 15
            if self.log : label = 'PSD (dB)'
            else        : label = 'PSD (µV²/Hz)'
            cbar.ax.set_xlabel(label)

    #=====================================================================
    # Handle PSD single plotting on click
    #=====================================================================
    def onclick(self, click) :
        """Get coordinates on the canvas and plot the corresponding PSD"""
        if self.plotType == "PSD Matrix" :
            # Handle clicks on PSD matrix
            channel_picked = click.ydata - 1
            ax_picked      = click.inaxes

        elif self.plotType == "Topomap" :
            # Handle clicks on topomaps
            x, y = click.xdata, click.ydata
            channel_picked = self.psd.channel_index_from_coord(x, y)
            ax_picked = click.inaxes

        if (channel_picked is not None and click.dblclick) :

            channel_picked = floor(channel_picked) + 1
            epoch_picked   = self.ui.epochsSlider.value()

            # If both are checked, it depends on which plot user clicked
            if (self.ui.showMean.checkState()
                    and self.ui.showSingleEpoch.checkState()) :

                if ax_picked.is_first_col() :
                    self.plot_single_psd(epoch_picked, channel_picked)
                else :
                    self.plot_single_avg_psd(channel_picked)

            elif self.ui.showSingleEpoch.checkState() :
                self.plot_single_psd(epoch_picked, channel_picked)

            elif self.ui.showMean.checkState() :
                self.plot_single_avg_psd(channel_picked)

    #---------------------------------------------------------------------
    def plot_single_psd(self, epoch_picked, channel_picked) :
        """Plot one single PSD"""
        plt.close('all')
        fig = plt.figure(figsize = (5, 5))
        ax = fig.add_subplot(1, 1, 1)
        self.psd.plot_single_psd(epoch_picked, channel_picked - 1,
                                 self.f_index_min, self.f_index_max,
                                 axes = ax, log_display = self.log)

        index_ch = self.psd.picks[channel_picked - 1]
        ax.set_title('PSD of Epoch {}, channel {}'.format(epoch_picked + 1,
                     self.psd.info['ch_names'][index_ch]))
        self.set_ax_single_psd(ax)

    #---------------------------------------------------------------------
    def plot_single_avg_psd(self, channel_picked) :
        """Plot one single averaged PSD"""
        plt.close('all')
        fig = plt.figure(figsize = (5, 5))
        ax = fig.add_subplot(1, 1, 1)
        self.psd.plot_single_avg_psd(
            channel_picked - 1, self.f_index_min, self.f_index_max,
            axes = ax, log_display = self.log)

        index_ch = self.psd.picks[channel_picked - 1]
        ax.set_title('Average PSD of channel {}'.format(
                     self.psd.info['ch_names'][index_ch]))
        self.set_ax_single_psd(ax)

    #---------------------------------------------------------------------
    def set_ax_single_psd(self, ax) :
        """Set axes values for a single PSD plot"""
        ax.set_xlim([self.psd.freqs[self.f_index_min],
                     self.psd.freqs[self.f_index_max]])
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Power (µV²/Hz)')
        plt.show()

    #=====================================================================
    # Auxiliary function
    #=====================================================================
    def get_index_freq(self, fmin, fmax) :
        """Get the indices of the freq between fmin and fmax"""
        f_index_min, f_index_max = -1, 0
        for freq in self.psd.freqs :
            if freq <= fmin : f_index_min += 1
            if freq <= fmax : f_index_max += 1

        # Just check if f_index_max is not out of bound
        f_index_max = min(len(self.psd.freqs) - 1, f_index_max)
        f_index_min = max(0, f_index_min)
        return f_index_min, f_index_max

    #---------------------------------------------------------------------
    def show_error(self, msg) :
        """Display window with an error message"""
        error = QMessageBox()
        error.setBaseSize(QSize(800, 200))
        error.setIcon(QMessageBox.Warning)
        error.setInformativeText(msg)
        error.setWindowTitle("Error")
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
