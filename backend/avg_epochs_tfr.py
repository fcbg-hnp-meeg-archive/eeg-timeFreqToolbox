class AvgEpochsTFR:
    """
    This class contains the PSD of a set of Epochs. It stores the data of
    the psds of each epoch. The psds are calculated with the Library mne.

    Attributes:
    ============
    picks       (array[int])   : Contains the picked channels
    tfr         (EpochsTFR)    : Contains the EpochsTFR data computed by mne


    Methods:
    ============
    __init__                   : Computes the EpochsTFR data
    plot_time_freq             : Plot the time-frequency display
    plot_freq_ch               : Plot the frequency-channel display
    plot_time_ch               : Plot the time-channel display
    """
    # ------------------------------------------------------------------------
    def __init__(self, epochs, freqs, n_cycles, method='multitaper',
                 time_bandwidth=4., n_fft=512, width=1, picks=None):
        """
        Initialize the class with an instance of EpochsTFR corresponding
        to the method
        """
        self.picks = picks
        self.cmap = 'inferno'
        self.info = epochs.info

        if method == 'multitaper':
            from mne.time_frequency import tfr_multitaper
            self.tfr, _ = tfr_multitaper(epochs, freqs, n_cycles,
                                         time_bandwidth=time_bandwidth,
                                         picks=self.picks)

        if method == 'morlet':
            from mne.time_frequency import tfr_morlet
            self.tfr, _ = tfr_morlet(epochs, freqs, n_cycles,
                                     picks=self.picks)

        if method == 'stockwell':
            from mne.time_frequency import tfr_stockwell
            # The stockwell function does not handle picks like the two other
            # ones ...
            picked_ch_names = [epochs.info['ch_names'][i] for i in self.picks]
            picked = epochs.copy().pick_channels(picked_ch_names)
            self.tfr = tfr_stockwell(picked, fmin=freqs[0], fmax=freqs[-1],
                                     n_fft=n_fft, width=width)

    # ------------------------------------------------------------------------
    def plot_time_freq(self, index_channel, ax, vmax=None):
        """
        Plot the averaged epochs time-frequency plot for a given channel
        """
        from matplotlib.pyplot import imshow

        data = self.tfr.data[index_channel, :, :]
        extent = [self.tfr.times[0], self.tfr.times[-1],
                  self.tfr.freqs[0], self.tfr.freqs[-1]]
        return ax.imshow(data, extent=extent, aspect='auto',
                         origin='lower', vmax=vmax, cmap=self.cmap)

    # ------------------------------------------------------------------------
    def plot_freq_ch(self, time_index, ax, vmax=None):
        """Plot the averaged epochs frequency-channel plot for a given time"""
        from matplotlib.pyplot import imshow

        data = self.tfr.data[:, :, time_index]
        extent = [self.tfr.freqs[0], self.tfr.freqs[-1],
                  .5, len(self.picks)+.5]
        return ax.imshow(data, extent=extent, aspect='auto',
                         origin='lower', vmax=vmax, cmap=self.cmap)

    # ------------------------------------------------------------------------
    def plot_time_ch(self, freq_index, ax, vmax=None):
        """
        Plot the averaged epochs time-channel plot for a given frequency
        range
        """
        from matplotlib.pyplot import imshow

        data = self.tfr.data[:, freq_index, :]
        extent = [self.tfr.times[0], self.tfr.times[-1],
                  .5,                len(self.picks)+.5]
        return ax.imshow(data, extent=extent, aspect='auto',
                         origin='lower', vmax=vmax, cmap=self.cmap)
