#---------------------------------------------------------------------
def xyz_to_montage(path) :
    """Reads and convert xyz positions to a mne montage type"""
    from mne.channels import Montage
    import numpy as np

    n = int(open(path).readline().split(' ')[0])
    coord = np.loadtxt(path, skiprows = 1, usecols = (0,1,2), max_rows = n)
    names = np.loadtxt(path, skiprows = 1, usecols = 3, max_rows = n,
                       dtype = np.dtype(str))
    names = names.tolist()
    return Montage(coord, names, 'standard_1005',
                   selection = [i for i in range(n)])

#---------------------------------------------------------------------
def eeg_to_montage(eeg) :
    """Returns an instance of montage from an eeg file"""
    from numpy import array, isnan
    from mne.channels import Montage

    pos = array([eeg.info['chs'][i]['loc'][:3]
                 for i in range(eeg.info['nchan'])
          ])
    if not isnan(pos).all() :
        selection = [i for i in range(eeg.info['nchan'])]
        montage = Montage(pos, eeg.info['ch_names'],
                          selection = selection, kind = 'custom')
        return montage
    else :
        return None

#---------------------------------------------------------------------
def float_(value) :
    """float with handle of none values"""
    if value is None :
        return None
    else :
        return float(value)

#---------------------------------------------------------------------
def int_(value) :
    """int with handle of none values"""
    if value is None :
        return None
    else :
        return int(value)

#---------------------------------------------------------------------
def blockPrint():
    import sys, os
    sys.stdout = open(os.devnull, 'w')

#---------------------------------------------------------------------
def enablePrint():
    import sys, os
    sys.stdout = sys.__stdout__

#---------------------------------------------------------------------
def preview(mne_data, figure) :
    """
    Plot a quick preview of the data with the first 5 channels on figure
    """
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    data = mne_data.get_data()
    times = mne_data.times
    if len(data.shape) == 3 :
        data = np.mean(data, axis = 0)
    data = data[0:5, :]
    if data.shape[1] > 1000 :
        data = data[:, 0:1000]
        times = times[0:1000]
    color = cm.rainbow(np.linspace(0,1,5))

    for i,c in zip(range(5), color) :
        ax = figure.add_subplot(5, 1, i+1)
        ax.plot(times, data[i, :], c = c)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.axis('off')
    plt.subplots_adjust(wspace=0, hspace=0, top = 1, right = 1,
                                   left = 0, bottom = 0)

#---------------------------------------------------------------------
def init_info_string(eeg_data) :
    """Init a string with informations about data"""
    sfreq      = eeg_data.info["sfreq"]
    n_channels = eeg_data.info["nchan"]
    infos1     = (("<li><b>Sampling Frequency:</b> {}Hz"
                  + "<li><b>Number of Channels:</b> {}")
                  .format(sfreq, n_channels))
    if len(eeg_data.get_data()) == 2 :
        n_times = eeg_data.n_times
        infos2 = "<li><b>Time points:</b> {}</li>".format(n_times)
        infos3 = ("<li><b>Duration of the signal:</b> {0:.2f}s </li>"
                  .format((n_times / sfreq)))

    else :
        times  = eeg_data.times
        infos2 = ("<li><b>Time points per Epoch:</b> {} </li>"
                 .format(len(times)))
        infos3 = ("<li><b>Duration of the signal:</b> {0:.2f}s </li>"
                  .format(times[-1] - times[0]))

    infos = infos1 + infos2 + infos3
    return "<ul>" + infos + "</ul>"
