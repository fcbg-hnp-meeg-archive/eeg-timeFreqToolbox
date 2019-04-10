import matplotlib.pyplot as plt
import numpy as np

class Events :
    """
    Events class for handling several events in provenance from an .mrk file

    Attributes :
    ============
    dic        (dic.)           : Dictionnary containing events ({label : [(begin,
                                  end), ...]})

    Methods :
    ============
    __init__                    : Sets up a dictionary with the event names
                                  and occurences

    plot                        : Plot on a new figure the events, with correct axes

    get_labels                  : Returns the labels of the events

    get_events                  : Returns the events corresponding to a label

    mne_events                  : Returns the events in a mne-format
                                  corresponding to a label

    compute_epochs              : Computes epochs from a raw file
    """

    #------------------------------------------------------------------------
    def __init__(self, path, type = 'mrk') :
        """Init mrk values in a dictionnary"""
        if type == 'mrk' :
            stim   = np.loadtxt(path, skiprows = 1, usecols = (0,1),
                                dtype = np.dtype(int))
            labels = np.loadtxt(path, skiprows = 1, usecols = 2,
                                dtype = np.dtype(str))

        if type == "-eve.fif" :
            from mne import read_events
            events = read_events(path)
            stim = np.transpose(np.array([events[:, 0], events[:, 0]]))
            labels = np.array([str(label) for label in events[:, 2]])
        print(stim)

        self.dic = dict.fromkeys(labels)
        for key, _ in self.dic.items() :
            self.dic[key] = []
        for k in range(len(stim)) :
            self.dic[labels[k]].append(stim[k, :])
        return None



    #------------------------------------------------------------------------
    def plot(self) :
        """Plot the events"""
        count = 1
        fig = plt.Figure()
        ax = plt.subplot(1,1,1)

        for key, values in self.dic.items() :
            for begin, end in values :
                #Create a scatter at each boundary of the segment, and a
                # line between the two dots
                ax.hlines(count, begin, end, color='r', alpha = .5)
                ax.scatter(begin, count, color='r', alpha = .5)
                ax.scatter(end, count, color='r', alpha = .5)
            count += 1

        ax.set_ylim(0, count)
        ax.set_xlabel('Samples')
        ax.set_ylabel('Labels')
        ax.set_yticks([i for i in range(1, count)])
        ax.set_yticklabels(self.dic.keys())

    #------------------------------------------------------------------------
    def get_labels(self) :
        """Return the labels"""
        return [key for key, _ in self.dic.items()]

    #------------------------------------------------------------------------
    def get_events(self, label) :
        """Return the events"""
        return self.dic[label]

    #------------------------------------------------------------------------
    def mne_events(self, event_label, anchor = 'beginning', offset = 0) :
        """
        Construct event array to inject in mne function

        anchor    : where we anchor the event (beginning or end)
        offset    : how we offset it
        """
        if anchor == 'beginning' :
            index = 0
        else :
            index = 1
        events = [[event[index] , 0, 0] for event in self.dic[event_label]]
        return np.array(events, dtype = np.dtype(int))

    #------------------------------------------------------------------------
    def compute_epochs(self, label, raw, tmin, tmax) :
        from mne import Epochs
        return Epochs(raw, self.mne_events(label),
                      tmin = tmin, tmax = tmax, preload = True)
