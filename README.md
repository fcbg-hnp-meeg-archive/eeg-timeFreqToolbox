# EEG Time-Frequency Toolbox GUI

The Time-Frequency toolbox GUI is a graphic user interface designed to interact with the MNE Library, by using its frequency and time-frequency analysis functions. 

[MNE Library Link](https://martinos.org/mne/dev/index.html)

# Installation

To install the dependencies required for this application, change the working directory to the repository and run the line `pip install -r requirements.txt`. You must have `python3 installed`.

To run the application simply run the line `python run_app.py`.

For now, the app can only treat the data to display the power spectrum density of raw eeg files, and epoched eeg files, with the formats `.fif`, `.sef`, `.ep` and `.eph`.

## Quick Tutorial

First import your file which can be either a raw file (format `*.fif` or `*.sef`), or epoched data (format `.epo-fif`).

The application also comes with an handy tool to process raw data files into epochs data with the help of a marker file (of format `*.mrk`). Just click on the `Cut into Epochs` button, and save your epochs data as a `*-epo.fif` file.

 For the topomaps plot you can either choose premade electrode setting from `mne` (If your file comes with corresponding 1005 or 1020 system names), or import the `*.xyz` file containing the 3D coordinates of the data in the electrode labeling menu.

 Then you have two choiceS of data visualization :

 * **PSD (Power Spectrum Density)** : Which computes the power spectrum density of the signal. You can display the results either in the form of a matrix (Simple plot of individual Channels by Frequencies), or as a topomap (Power of electrode represented on the scalp). It is also possible to run across the different epochs if the file is epoched data.

  ![](https://github.com/fcbg-hnp/eeg-timeFreqToolbox/blob/master/assets/psdwindow.png)

 * **Average TFR (Average Time-Frequency)** : Which computes the time-frequency representation of the signal averaged over epochs. *This feature only works on epoched data*. You can either display the results on regular time-frequency representation (Time by Frequency), or displays it in different ways (channels by frequencies, or channels by time).

  ![](https://github.com/fcbg-hnp/eeg-timeFreqToolbox/blob/master/assets/tfrwindow.png )


## Parameters handling

You can easily import parameters using the import button in the app. The parameters are setup in a simple txt file, in the following way :

`param_id = value` or `param_id = value1, value2, ...` if several values are expected.

Check here for a detailed description of parameters : [Click Here !](https://github.com/fcbg-hnp/eeg-timeFreqToolbox/help_parameters.md)
