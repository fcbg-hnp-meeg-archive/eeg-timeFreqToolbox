#---------------------------------------------------------------------
def _read_data(self) :
    """Reads the data from path"""
    index = self.ui.dataFilesBox.currentIndex()
    try :
        if self.filePaths[index].endswith('-epo.fif') :
            from mne import read_epochs
            self.type = 'epochs'
            self.data = read_epochs(self.filePaths[index])
            print("Epoch file initialized")

        elif self.filePaths[index].endswith('.fif') :
            from mne.io import read_raw_fif
            self.type = 'raw'
            self.data = read_raw_fif(self.filePaths[index])
            print("Raw file initialized")

        elif self.filePaths[index].endswith('.sef') :
            from backend.read import read_sef
            self.type = 'raw'
            self.data = read_sef(self.filePaths[index])
            print("Raw file initialized")

        else :
            raise ValueError('Extension not handled')

    except :
        print("Can't read the file")

    else :
        self.processed_data = self.data
        # Write down the informations
        from backend.util import init_info_string
        from backend.util import eeg_to_montage

        if eeg_to_montage(self.data) is not None :
            self.ui.montageBox.addItem('Imported from file')
            self.ui.montageBox.setCurrentIndex(3)

        self.ui.informationLabel.setText(
            init_info_string(self.data))
        # Draw the little preview
        from backend.util import preview
        self.ui.figurePreview.clear()
        preview(self.data, self.ui.figurePreview)
        self.ui.preview.draw()
        self.read_montage()


#---------------------------------------------------------------------
# Apply all the preprocessing
#---------------------------------------------------------------------
def _apply_preprocess(self) :
    """Apply all the checked preprocessing units"""
    data = self.data.copy()
    # Just make sure the new bads selected are added to the original data
    bads = self.processed_data.info['bads']
    data.info['bads'] = bads

    data.load_data()
    if self.ui.filterPanel.isChecked() :
        _apply_filter(self, data)

    if self.ui.montagePanel.isChecked() :
        data.set_montage(self.montage)

    if self.ui.interpPanel.isChecked() :
        data.interpolate_bads(reset_bads = False,
                              mode = self.ui.interpBox.currentText())

    if self.ui.refPanel.isChecked() :
        data.set_eeg_reference(ref_channels = 'average')

    self.processed_data = data

#---------------------------------------------------------------------
def _apply_filter(self, data) :
    from backend.util import float_
    low = float_(self.ui.lowFilter.text())
    high = float_(self.ui.highFilter.text())
    data.filter(low, high)

#---------------------------------------------------------------------
def _apply_referencing(self, data) :
    if self.ui.refBox.currentText() == 'No referencing' :
        data.set_eeg_reference(ref_channels = [])
    elif self.ui.refBox.currentText() == 'average' :
        data.set_eeg_reference(ref_channels = 'average')
    else :
        data.set_eeg_reference(ref_channels = [])
