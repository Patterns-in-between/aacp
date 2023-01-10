
# Paper: Dance Tempo Estimation Using a Single Leg-Attached 3D Accelerometer 
"Our tempo estimation method is based on enhanced multiple resonators, implemented with comb feedback filters."
https://www.mdpi.com/1424-8220/21/23/8066/htm

# 'madmom' tempo estimation library:
https://madmom.readthedocs.io/en/v0.16.1/modules/features/tempo.html
tests: https://github.com/CPJKU/madmom/blob/main/tests/test_features_tempo.py

# Example of use of madmom tempo:
In aligning two audio files for mashups
https://github.com/MilenMMinev/mmp/blob/ac2e3b2bda79d2f7bbef3b17815713a02a9683c1/mmg.ipynb
https://www.youtube.com/watch?v=Xc99NvCjAXI

        beat_act = RNNBeatProcessor()((self.decoded_f))
        tempo_hist = interval_histogram_comb(beat_act, alpha=SMOOTHING_ALPHA, min_tau=TAU_MIN, max_tau=TAU_MAX)
        smooth_hist = smooth_histogram(tempo_hist, smooth=7)
        tempi_and_strengths = detect_tempo(smooth_hist, fps=100)
        self.tempo = tempi_and_strengths[0][0]

RNN = recurrent neural network

can it be used online?
Here it says "For online processing, online must be set to ‘True’.", but then the example is a .wav file
https://madmom.readthedocs.io/en/v0.16.1/modules/features/beats.html

Aha, here's an online example:
    https://groups.google.com/g/madmom-users/c/yYtp6Y43yWQ?pli=1
    archived: https://web.archive.org/web/20230106093934/https://groups.google.com/g/madmom-users/c/yYtp6Y43yWQ?pli=1

but ! this is all based on audio.. The paper describing RNNBeatProcessor:
http://recherche.ircam.fr/pub/dafx11/Papers/31_e.pdf
It seems it's trained on a standard ISMIR audio dataset

and does dance sensor data really have 'beats' in a similar way?

# Back to sensor data..

Here they apply a low-pass filter to accelerometer data then measure time between peaks:
http://roberto.martinezmaldonado.net/wp-content/uploads/2018/05/moco-beat-accelerometer_2018-05-14.pdf

They have a different task though, of measuring dance tempo against known music tempo

# Autocorrelation
When I asked on twitter a while ago, rebecca fiebrink and others suggested autocorrelation
https://www.investopedia.com/terms/a/autocorrelation.asp

So maybe we just try a low-pass filter going into autocorrelation and see what happens

Some different ways of implementing it, including pure python and numpy:
https://scicoding.com/4-ways-of-calculating-autocorrelation-in-python/

these examples are with testing a small set of lags.

Here is an example for a range of 2000 lags, for pitch detection:
https://scicoding.com/pitchdetection/

It uses statsmodels for the autocorrelation, and scipy to find 'peaks'
* acf: https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.acf.html
* find_peaks https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html

It takes the first peak in the data as the fundamental frequency.

# Approach

* do some preprocessing to clean the data, like a LPF. The output from machine learning might not need this
* do the acf to look for repetitions in the range we're interested in
* take the first peak, or maybe the biggest one?
* If the peak isn't over a threshold, ignore it as uncertain
* convert to Hz based on sample rate
* somehow add smoothing to the result to adjust the tempo, probably using link

Previous approach using FFT is here: https://github.com/Patterns-in-between/aacp/blob/main/py/tempo/tempo.py

Either adapt this or refactor/simplify/rewrite based on statsmodels example above.

# Running tempo.py with test data

in aacp/zmq:

* python ./proxy.py
* python ./playback.py adjusted-20210701-132910.txt

In aacp/py/tempo/:

* python ./tempo.py

