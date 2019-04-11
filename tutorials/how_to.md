# How to use the Time-Frequency Toolbox

## Import your files

First assure yourself that the data you want to visualize is of correct format (see list below) :

* `*.fif`, `*.epo-fif`
* `*.sef` (cartool native format)
* `*.ep` or `*.eph` (txt files with one eeg channel per column)

The First step is to import the data into the software, by selecting the path. If it loaded successfully, you should be able to see the informations of the data displayed below, with a quick overview of the 5 first channels.

It is also possible to import several files in order to batch process them. Simply click the save PSD button, and it will compute and save all the files that you selected. Beware that you will only be able to visualize the first one if you click Visualize.

## Visualize the data

In the preview window, you can see an overview of the 5 first channels, and open the interactive window in order to see the entirety of the signal. You can adapt the scale by pressing the keys + or - if the scale is not to your liking.

## Select the channels

If you only want to represent or save a restricted number of channels, you can go in the channels window, to select all the channels that you want to keep in the frequency analysis.

## Electrode Convention

To be able to plot the topomaps, you have to select an electrode convention that is suiting the names of your channels, if it is not already in your data. To visualize the convention, click the see Montage button, to have an overview of the convention.

## Power Spectrum Density

To open the Power Spectrum Density interactive window, you have to select your parameters and click Visualize PSD. If you only want to save the result without seeing it in the interactive window, simply click the save PSD button.

The parameters of the computing can be changed by changing the value in the text editor. If you want, you can also import a txt file with the same shape as the one displayed.

For more informations about the parameters, check out the detailed explanation here !.

## Time-Frequency

To open the time-frequency interactive window, simply edit the parameters to your liking, and click on the button Visualize Time-Frequency. Note that for the moment you can only visualize Epoched data with this tool. If you only have raw data, you can cut it with the Raw to Epochs Converter if you have the corresponding marker file. It is for now not possible to save the time-frequency representation.
