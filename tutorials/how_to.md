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

### Interactive Power Spectrum Density Window

In this window, you will be able to visualize all the power spectrum density. The first view mode is the matrix, where all the power spectrum densities are displayed in a stacked way, channel by channel. If you selected a montage, you can also visualize the topomap of a frequency range.

The frequency range controls the boundaries if the interval of the matrix, or the boundaries of the frequency band for the topomap plot.

You can also slide through every single frequency point by using the slider below the frequency values.

If the data was epoched, you can also decide to show the average over epochs, or each single epoch.

If you want to have the same scale across every plot, simply put a value different from 0 on the scale value. This is helpful when comparing the values of different plots while sliding through frequencies or epochs.

Finally, you can also interact with the plot by double clicking on the plot to display the power spectrum density of the particular channel, and the name of the channel. This works either for the matrix plot or the topomap plot.

## Time-Frequency

To open the time-frequency interactive window, simply edit the parameters to your liking, and click on the button Visualize Time-Frequency. Note that for the moment you can only visualize Epoched data with this tool. If you only have raw data, you can cut it with the Raw to Epochs Converter if you have the corresponding marker file. It is for now not possible to save the time-frequency representation.

### Interactive Time-Frequency Window

For the moment, you can simply switch between 3 matrix representations of time-frequency. It can either be Time-Frequency (the most popular), Time-Channel or Frequency-Channel. The slider enables you to slide through the third dimension (ie for Time-Frequency, the slider enables you to switch from one channel to one another)

You can also select a common scale by putting a value different from 0 in the scaling value.
