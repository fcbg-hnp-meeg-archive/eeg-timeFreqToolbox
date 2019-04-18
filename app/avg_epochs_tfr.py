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
        self.set_line_edit()
        self.set_bindings()
        self.set_slider()
        self.plot_changed()

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
    def set_line_edit(self):
        """Sets up scaling line edit
        """
        self.vmax = None
        self.ui.lineEdit.setText('0')
        self.ui.lineEdit.setMaxLength(6)

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
        self.ui.lineEdit.editingFinished.connect(self.scaling_changed)
        self.ui.displayBox.currentIndexChanged.connect(self.plot_changed)
        self.ui.mainSlider.valueChanged.connect(self.index_changed)

    # Updating functions
    # =====================================================================
    def plot_changed(self):
        """Get called when the method is changed
        """
        self.plotType = self.ui.displayBox.currentText()
        self.update_slider()
        self.plot()

    # ---------------------------------------------------------------------
    def index_changed(self):
        """Gets called when the index is changed
        """
        self.index = self.ui.mainSlider.value()
        self.plot()

    # --------------------------------------------------------------------
    def scaling_changed(self):
        """Gets called when scaling is changed
        """
        self.vmax = float(self.ui.lineEdit.text())
        if self.vmax == 0:
            self.vmax = None
        self.plot()

    # ---------------------------------------------------------------------
    def update_slider(self):
        """Update Maximum of the slider
        """
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
        self.plot()

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
