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

def float_(value) :
    """float with handle of none values"""
    if value is None :
        return None
    else :
        return float(value)

def int_(value) :
    """int with handle of none values"""
    if value is None :
        return None
    else :
        return int(value)

def batch_process_epochs(path, **parameters) :
    """This function batch processes a serie of eeg files, and saves it as a
    PSD of format out. This take an argument a path leading to a folder
    containing all the files of epochs of format epo-fif"""

    import os
    from backend.epochs_psd import EpochsPSD
    from mne import read_epochs

    # Init a value files with all the paths of the files to process
    if path.endswith('-epo.fif') :
        files_path = [path]
    else :
        files = [path + file for file in os.lisdir(path)]

    for file in files :
        epochs = read_epochs(file)
        psd = EpochsPSD(epochs, **parameters)
        psd.save_avg_matrix_sef()

def blockPrint():
    import sys, os
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    import sys, os
    sys.stdout = sys.__stdout__

def preview(mne_data, figure) :
    """
    Plot a quick preview of the data with the first 5 channels on figure
    """
    import numpy as np
    import matplotlib.pyplot as plt

    data = mne_data.get_data()
    times = mne_data.times
    if len(data.shape) == 3 :
        data = np.mean(data, axis = 0)
    data = data[0:5, :]
    if data.shape[1] > 1000 :
        data = data[:, 0:1000]
        times = times[0:1000]

    for i in range(5) :
        ax = figure.add_subplot(5, 1, i+1)
        ax.plot(times, data[i, :])
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.axis('off')
    plt.subplots_adjust(wspace=0, hspace=0, top = 1, right = 1,
                                   left = 0, bottom = 0)
