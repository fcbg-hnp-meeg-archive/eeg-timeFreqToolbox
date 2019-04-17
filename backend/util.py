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
def init_info_string(eeg_data) :
    """Init a string with informations about data"""
    sfreq      = eeg_data.info["sfreq"]
    n_channels = eeg_data.info["nchan"]
    infos1     = (("<li><b>Sampling Frequency:</b> {}Hz"
                  + "<li><b>Number of Channels:</b> {}")
                  .format(sfreq, n_channels))
    if len(eeg_data.get_data().shape) == 2 :
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
