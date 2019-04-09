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
