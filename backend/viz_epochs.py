from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt

"""
This file contains several utilitary functions to work with the
visualization of epochs psd

win --> instance of EpochsPSDWindow
"""


# ---------------------------------------------------------------------
def _plot_topomaps(win):
    """Plot the topomaps
    """
    win.ui.figure.clear()
    _topomaps_adjust(win)
    _add_colorbar(win, [0.915, 0.15, 0.01, 0.7])
    win.ui.figure.subplots_adjust(top=0.9, right=0.8,
                                  left=0.1, bottom=0.1)
    win.ui.canvas.draw()


# ---------------------------------------------------------------------
def _plot_matrix(win):
    """Plot the Matrix
    """
    win.ui.figure.clear()
    _matrix_adjust(win)
    _add_colorbar(win, [0.915, 0.15, 0.01, 0.7])
    win.ui.figure.subplots_adjust(top=0.85, right=0.8,
                                  left=0.1, bottom=0.1)
    win.ui.canvas.draw()


# ---------------------------------------------------------------------
def _plot_all_psd(win):
    """Plot all the PSD
    """
    win.ui.figure.clear()
    _plot_all_psd_adjust(win)
    win.ui.figure.subplots_adjust(top=0.9, right=0.9,
                                  left=0.1, bottom=0.1)
    win.ui.canvas.draw()


# ---------------------------------------------------------------------
def _add_colorbar(win, position):
    """Add colorbar to the plot at correct position
    """
    if (win.ui.showSingleEpoch.checkState()
            or win.ui.showMean.checkState()):
        # plot a common colorbar for both representations
        cax = win.ui.figure.add_axes(position)
        cbar = plt.colorbar(win.cbar_image, cax=cax)
        cbar.ax.get_xaxis().labelpad = 15
        if win.log:
            label = 'PSD (dB)'
        else:
            label = 'PSD (µV²/Hz)'
        cbar.ax.set_xlabel(label)


# Adjusting the plots
# =====================================================================
def _topomaps_adjust(win):
    """Plot the good number of subplots and update cbar_image instance
    """

    if (win.ui.showMean.checkState()
            and win.ui.showSingleEpoch.checkState()):
        nbFrames = 2
    else:
        nbFrames = 1

    # Plot single epoch if showSingleEpoch is checked
    if win.ui.showSingleEpoch.checkState():
        ax = win.ui.figure.add_subplot(1, nbFrames, 1)
        win.cbar_image, _ = win.psd.plot_topomap_band(
                                win.epoch_index,
                                win.f_index_min, win.f_index_max,
                                axes=ax, vmin=win.vmin, vmax=win.vmax,
                                log_display=win.log)
        ax.set_title('Epoch {}'.format(win.epoch_index + 1),
                     fontsize=15, fontweight='light')

    # plot average data if showMean is checked
    if win.ui.showMean.checkState():
        ax = win.ui.figure.add_subplot(1, nbFrames, nbFrames)
        win.cbar_image, _ = win.psd.plot_avg_topomap_band(
                                win.f_index_min, win.f_index_max, axes=ax,
                                vmin=win.vmin, vmax=win.vmax,
                                log_display=win.log)
        ax.set_title('Average', fontsize=15, fontweight='light')


# ---------------------------------------------------------------------
def _matrix_adjust(win):
    """Plot the matrix and update cbar_image instance
    """
    if (win.ui.showMean.checkState()
            and win.ui.showSingleEpoch.checkState()):
        nbFrames = 2
    else:
        nbFrames = 1

    # plot single epoch data uf showSingleEpoch is checked
    if win.ui.showSingleEpoch.checkState():
        ax = win.ui.figure.add_subplot(1, nbFrames, 1)
        win.cbar_image = win.psd.plot_matrix(
                              win.epoch_index,
                              win.f_index_min, win.f_index_max,
                              vmin=win.vmin, vmax=win.vmax,
                              axes=ax, log_display=win.log)
        ax.axis('tight')
        ax.set_title('Matrix for epoch {}'.format(win.epoch_index + 1),
                     fontsize=15, fontweight='light')
        ax.set_xlabel('Frequencies (Hz)')
        ax.set_ylabel('Channels')
        ax.xaxis.set_ticks_position('bottom')

    # plot average data if showMean is checked
    if win.ui.showMean.checkState():
        ax = win.ui.figure.add_subplot(1, nbFrames, nbFrames)
        win.cbar_image = win.psd.plot_avg_matrix(
                              win.f_index_min, win.f_index_max, axes=ax,
                              vmin=win.vmin, vmax=win.vmax,
                              log_display=win.log)
        ax.axis('tight')
        ax.set_title('Average Matrix', fontsize=15,
                     fontweight='light')
        ax.set_xlabel('Frequencies (Hz)')
        ax.set_ylabel('Channels')
        ax.xaxis.set_ticks_position('bottom')


# ---------------------------------------------------------------------
def _plot_all_psd_adjust(win):
    """Plot all the PSD
    """
    if (win.ui.showMean.checkState()
            and win.ui.showSingleEpoch.checkState()):
        nbFrames = 2
    else:
        nbFrames = 1

    # plot single epoch data uf showSingleEpoch is checked
    if win.ui.showSingleEpoch.checkState():
        ax = win.ui.figure.add_subplot(1, nbFrames, 1)
        win.psd.plot_all_psd(
            win.epoch_index, win.f_index_min, win.f_index_max,
            axes=ax, log_display=win.log)
        ax.axis('tight')
        ax.set_title('PSD for epoch {}'.format(win.epoch_index + 1),
                     fontsize=15, fontweight='light')
        ax.set_xlabel('Frequencies (Hz)')
        ax.set_ylabel('Power')
        win.annot_epoch = ax.annotate('', xy=(0, 0), xytext=(20, 20),
                                      textcoords='offset points',
                                      arrowprops=dict(arrowstyle='->'))
        win.annot_epoch.set_visible(False)

    # plot average data if showMean is checked
    if win.ui.showMean.checkState():
        ax = win.ui.figure.add_subplot(1, nbFrames, nbFrames)
        win.psd.plot_all_avg_psd(
            win.f_index_min, win.f_index_max,
            axes=ax, log_display=win.log)
        ax.axis('tight')
        ax.set_title('Average PSD', fontsize=15,
                     fontweight='light')
        ax.set_xlabel('Frequencies (Hz)')
        ax.set_ylabel('Power')
        win.annot_avg = ax.annotate('', xy=(0, 0), xytext=(20, 20),
                                    textcoords='offset points',
                                    arrowprops=dict(arrowstyle='->'))
        win.annot_avg.set_visible(False)


# ---------------------------------------------------------------------
def _plot_single_psd(win, epoch_picked, channel_picked):
    """Plot one single PSD
    """
    plt.close('all')
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(1, 1, 1)
    win.psd.plot_single_psd(epoch_picked, channel_picked - 1,
                            axes=ax, log_display=win.log)

    index_ch = win.psd.picks[channel_picked - 1]
    ax.set_title('PSD of Epoch {}, channel {}'.format(epoch_picked + 1,
                 win.psd.info['ch_names'][index_ch]))
    _set_ax_single_psd(win, ax)
    win = fig.canvas.manager.window
    win.setWindowModality(Qt.WindowModal)
    win.setWindowTitle('PSD')
    win.findChild(QStatusBar).hide()
    fig.show()


# ---------------------------------------------------------------------
def _plot_single_avg_psd(win, channel_picked):
    """Plot one single averaged PSD
    """
    plt.close('all')
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(1, 1, 1)
    win.psd.plot_single_avg_psd(
        channel_picked - 1, axes=ax, log_display=win.log)

    index_ch = win.psd.picks[channel_picked - 1]
    ax.set_title('Average PSD of channel {}'.format(
                 win.psd.info['ch_names'][index_ch]))
    _set_ax_single_psd(win, ax)
    win = fig.canvas.manager.window
    win.setWindowModality(Qt.WindowModal)
    win.setWindowTitle('PSD')
    win.findChild(QStatusBar).hide()
    fig.show()


# ---------------------------------------------------------------------
def _set_ax_single_psd(win, ax):
    """Set axes values for a single PSD plot
    """
    ax.set_xlim([win.psd.freqs[0],
                 win.psd.freqs[-1]])
    ax.set_xlabel('Frequency (Hz)')
    if win.log:
        ax.set_ylabel('Power (dB)')
    else:
        ax.set_ylabel('Power (µV²/Hz)')
