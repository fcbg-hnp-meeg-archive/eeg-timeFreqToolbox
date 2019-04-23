from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg \
    import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from app.ui.avg_epochs_tfr_UI import Ui_AvgTFRWindow


class AvgTFRWindow(QDialog):

    def __init__(self, avgTFR, parent=None):
        super(AvgTFRWindow, self).__init__(parent)
        self.avg = avgTFR
        self.ui = Ui_AvgTFRWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.setup()

    # Setup functions
    # =====================================================================
    def setup(self):
        self.set_canvas()
        self.set_box()
        self.set_bindings()
        self.set_slider()
        self.value_changed()
        self.ui.vmax.setMaxLength(6)
        self.ui.vmin.setMaxLength(6)

    # ---------------------------------------------------------------------
    def set_canvas(self):
        """setup canvas for matplotlib
        """
        self.ui.figure = plt.figure(figsize=(10, 10))
        self.ui.figure.patch.set_facecolor('None')
        self.ui.canvas = FigureCanvas(self.ui.figure)
        self.ui.canvas.setStyleSheet('background-color:transparent;')
        # Matplotlib toolbar
        self.ui.toolbar = NavigationToolbar(self.ui.canvas, self)
        self.ui.matplotlibLayout.addWidget(self.ui.toolbar)
        self.ui.matplotlibLayout.addWidget(self.ui.canvas)

    # ---------------------------------------------------------------------
    def set_box(self):
        """Setup box names
        """
        self.ui.displayBox.addItem('Time-Frequency plot')
        self.ui.displayBox.addItem('Channel-Frequency plot')
        self.ui.displayBox.addItem('Channel-Time plot')
        self.plotType = 'Time-Frequency plot'

    # ---------------------------------------------------------------------
    def set_slider(self):
        """Setup the main slider
        """
        self.index = self.ui.mainSlider.value()
        self.ui.mainSlider.setMinimum(0)
        self.update_slider()

    # ---------------------------------------------------------------------
    def set_bindings(self):
        """Set the bindings
        """
        self.ui.vmin.editingFinished.connect(self.value_changed)
        self.ui.vmax.editingFinished.connect(self.value_changed)
        self.ui.displayBox.currentIndexChanged.connect(self.update_slider)
        self.ui.mainSlider.valueChanged.connect(self.value_changed)
        self.ui.log.stateChanged.connect(self.value_changed)

    # Updating functions
    # =====================================================================
    def value_changed(self):
        """Gets called when scaling is changed
        """
        self.index = self.ui.mainSlider.value()
        self.log = self.ui.log.checkState()
        self.vmin = self.ui.vmin.text()
        self.vmax = self.ui.vmax.text()
        try:
            self.vmax = float(self.vmax)
        except ValueError:
            self.vmax = None
        try:
            self.vmin = float(self.vmin)
        except ValueError:
            self.vmin = None
        self.plot()

    # ---------------------------------------------------------------------
    def update_slider(self):
        """Update Maximum of the slider
        """
        self.plotType = self.ui.displayBox.currentText()
        self.ui.mainSlider.setValue(0)
        if self.plotType == 'Time-Frequency plot':
            self.ui.mainSlider.setMaximum(self.avg.tfr.data.shape[0] - 1)
            self.ui.mainLabel.setText('Channels')
        if self.plotType == 'Channel-Frequency plot':
            self.ui.mainSlider.setMaximum(self.avg.tfr.data.shape[2] - 1)
            self.ui.mainLabel.setText('Times')
        if self.plotType == 'Channel-Time plot':
            self.ui.mainSlider.setMaximum(self.avg.tfr.data.shape[1] - 1)
            self.ui.mainLabel.setText('Frequencies')
        self.ui.mainSlider.setTickInterval(1)
        self.value_changed()

    # Plotting functions
    # =====================================================================
    def plot(self):
        """Plot the correct representation
        """
        from backend.viz_tfr import \
            _plot_time_freq, _plot_freq_ch, _plot_time_ch

        if self.plotType == 'Time-Frequency plot':
            _plot_time_freq(self)
        if self.plotType == 'Channel-Frequency plot':
            _plot_freq_ch(self)
        if self.plotType == 'Channel-Time plot':
            _plot_time_ch(self)
