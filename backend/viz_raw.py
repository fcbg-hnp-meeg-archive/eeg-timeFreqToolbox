from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt

"""
This file contains several utilitary functions to work with the
visualization of raw psd

win --> instance of RawPSDWindow
"""


# ----------------------------------------------------------------------
def _plot_topomap(win, f_index_min, f_index_max, vmax):
    """Plot the topomaps
    """
    win.ui.figure.clear()
    ax = win.ui.figure.add_subplot(1, 1, 1)
    win.cbar_image, _ = win.psd.plot_topomap_band(
                             f_index_min, f_index_max, axes=ax,
                             vmin=win.vmin, vmax=vmax,
                             log_display=win.log)
    _add_colorbar(win, [0.915, 0.15, 0.01, 0.7])
    win.ui.figure.subplots_adjust(top=0.9, right=0.8,
                                  left=0.1, bottom=0.1)
    win.ui.canvas.draw()


# ---------------------------------------------------------------------
def _plot_matrix(win, f_index_min, f_index_max, vmax):
    """Plot the Matrix
    """
    win.ui.figure.clear()
    ax = win.ui.figure.add_subplot(1, 1, 1)
    win.cbar_image = win.psd.plot_matrix(
                           f_index_min, f_index_max, axes=ax,
                           vmin=win.vmin, vmax=vmax,
                           log_display=win.log)
    ax.axis('tight')
    ax.set_title("Matrix", fontsize=15, fontweight='light')
    ax.set_xlabel('Frequencies (Hz)')
    ax.set_ylabel('Channels')
    ax.xaxis.set_ticks_position('bottom')
    _add_colorbar(win, [0.915, 0.15, 0.01, 0.7])
    win.ui.figure.subplots_adjust(top=0.85, right=0.8,
                                  left=0.1, bottom=0.1)
    win.ui.canvas.draw()


# ---------------------------------------------------------------------
def _plot_all_psd(win, f_index_min, f_index_max):
    """Plot all PSDs
    """
    win.ui.figure.clear()
    ax = win.ui.figure.add_subplot(1, 1, 1)
    win.annot = ax.annotate("", xy=(0, 0), xytext=(20, 20),
                            textcoords="offset points",
                            arrowprops=dict(arrowstyle="->"))
    win.annot.set_visible(False)
    win.psd.plot_all_psd(
        f_index_min, f_index_max, axes=ax, log_display=win.log)

    ax.axis = ('tight')
    ax.patch.set_alpha(0)
    ax.set_title("PSD", fontsize=15, fontweight='light')
    ax.set_xlim([win.psd.freqs[f_index_min],
                 win.psd.freqs[f_index_max]])
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power (µV²/Hz)')
    win.ui.figure.subplots_adjust(top=0.85, right=0.9,
                                  left=0.1, bottom=0.1)
    win.ui.canvas.draw()


# ---------------------------------------------------------------------
def _add_colorbar(win, position):
    """ Add colorbar to the plot at correct position
    """
    cax = win.ui.figure.add_axes(position)
    cbar = plt.colorbar(win.cbar_image, cax=cax)
    cbar.ax.get_xaxis().labelpad = 15
    if win.log:
        label = 'PSD (dB)'
    else:
        label = 'PSD (µV²/Hz)'
    cbar.ax.set_xlabel(label)


# ---------------------------------------------------------------------
def set_ax_single_psd(win, ax):
    """Set axes values for a single PSD plot
    """
    ax.set_xlim([win.psd.freqs[0],
                 win.psd.freqs[-1]])
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power (µV²/Hz)')


# ---------------------------------------------------------------------
def _plot_single_psd(win, channel_picked):
    """Plot one single PSD
    """
    plt.close('all')
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(1, 1, 1)
    win.psd.plot_single_psd(channel_picked - 1, axes=ax,
                            log_display=win.log)
    index_ch = win.psd.picks[channel_picked - 1]
    ax.set_title('PSD of channel {}'
                 .format(win.psd.info['ch_names'][index_ch]))
    set_ax_single_psd(win, ax)
    win = fig.canvas.manager.window
    win.setWindowModality(Qt.WindowModal)
    win.setWindowTitle("PSD")
    win.findChild(QStatusBar).hide()
    fig.show()
