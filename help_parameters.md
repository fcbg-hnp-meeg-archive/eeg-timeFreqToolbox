# Parameters Detailed Description

You can also checkout the documentation from MNE to gain knowledge about the different techniques and methods implemented. See the Time and Frequency-Domain part. [Link Here !](https://martinos.org/mne/stable/documentation.html)

## Power Spectrum Density Parameters

`fmin` : Minimum frequency (Hz)

`fmax` : Maximum Frequency (Hz)

`tmin` : Low Boundary of the time Interval (s)

`tmax` : High Boundary of the time Interval (s)

##### Multitaper Method

`bandwidth` : Time-Bandwidth product. *A high Time-Bandwidth product enables more smoothing, and a better frequency precision.*

##### Welch Method


`n_fft` : Number of points used to compute the FFT.

`n_per_seg` : Number of points in a segment.

`n_overlap` : Number of points of overlapping between two segments.

We typically aim for 3 to 6 segments with 50% of overlapping to have a good result. If the signal is N points, we would take N/2 points per segment, and an overlapping of N/4 points to have 3 segments total.




## Time-Frequency Parameters

`fmin` : Minimum frequency (Hz)

`fmax` : Maximum Frequency (Hz)

`freq_step` : Frequency step (Hz)

##### Multitaper & Morlet

You can either work with a variable time-window by choosing a fixed n_cycles (number of cycle in the wavelet) parameters to have a multi-resolution, or work with a fixed time-window by choosing a time-window. The default is set to fixed time-window, equal to 0.5s.

`time_window` : Time-Window. *This controls the length of the time interval on which the STFT is used (for Multitaper), or the temporal length of the wavelet (for Morlet method). A large time-window enables to have a good frequecy resolution.*

`n_cycles` : Number of cycles. *This enables to control the frequency precision. A higher number of cycles means a better frequency precision. Be careful, because if too much cycles are used, it can be an issue for lower frequencies as it will require a very long signal to fit.*

##### Multitaper Method

`time_bandwidth` : Time-Bandwidth product. *A high Time-Bandwidth product enables more smoothing, and a better frequency precision. It is equal to the product of the time-window by the bandwidth*

##### Stockwell Method

`width` : Controls the width of the windows for the STFT. A width > 1 means an increased frequency precision, while a width < 1 means an increased time precision.
