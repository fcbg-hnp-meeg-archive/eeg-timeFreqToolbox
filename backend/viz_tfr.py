from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
def _plot_time_freq(self):
    """Plot the time-frequency representation
    """
    self.ui.figure.clear()
    ax = self.ui.figure.add_subplot(1, 1, 1)
    self.cbar_image = self.avg.plot_time_freq(
        self.index, ax, vmax=self.vmax)
    ax.set_title('Time-Frequency Plot - Channel {}'.format(
                 self.avg.info['ch_names'][self.avg.picks[self.index]]),
                 fontsize=15, fontweight='light')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequencies (Hz)')
    add_colorbar(self, [0.915, 0.15, 0.01, 0.7])
    self.ui.figure.subplots_adjust(top=0.85, right=0.8,
                                   left=0.1, bottom=0.1)
    self.ui.canvas.draw()


# ---------------------------------------------------------------------
def _plot_freq_ch(self):
    """Plot the frequency-channel representation
    """
    self.ui.figure.clear()
    ax = self.ui.figure.add_subplot(1, 1, 1)
    self.cbar_image = self.avg.plot_freq_ch(
        self.index, ax, vmax=self.vmax)
    ax.set_title(('Frequency-Channel Plot - Time {:.2f}s'
                 .format(self.avg.tfr.times[self.index])),
                 fontsize=15, fontweight='light')
    ax.set_xlabel('Frequencies (Hz)')
    ax.set_ylabel('Channels')
    ax.set_yticks([i for i in range(1, len(self.avg.picks)+1)])
    ax.set_yticklabels(self.avg.picks)
    add_colorbar(self, [0.915, 0.15, 0.01, 0.7])
    self.ui.figure.subplots_adjust(top=0.85, right=0.8,
                                   left=0.1, bottom=0.1)
    self.ui.canvas.draw()


# ---------------------------------------------------------------------
def _plot_time_ch(self):
    """Plot the time-channels representation
    """
    self.ui.figure.clear()
    ax = self.ui.figure.add_subplot(1, 1, 1)
    self.cbar_image = self.avg.plot_time_ch(
        self.index, ax, vmax=self.vmax)
    ax.set_title(('Time-Channel Plot - Frequency {:.2f}'
                  .format(self.avg.tfr.freqs[self.index])),
                 fontsize=15, fontweight='light')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Channels')
    ax.set_yticks([i for i in range(1, len(self.avg.picks)+1)])
    ax.set_yticklabels(self.avg.picks)
    add_colorbar(self, [0.915, 0.15, 0.01, 0.7])
    self.ui.figure.subplots_adjust(top=0.85, right=0.8,
                                   left=0.1, bottom=0.1)
    self.ui.canvas.draw()


# ---------------------------------------------------------------------
def add_colorbar(self, position):
    """ Add colorbar to the plot at correct position
    """
    cax = self.ui.figure.add_axes(position)
    cbar = plt.colorbar(self.cbar_image, cax=cax)
    cbar.ax.get_xaxis().labelpad = 15
    cbar.ax.set_xlabel('Power')
