import mne
import matplotlib.pyplot as plt
import numpy as np

raw = mne.io.read_raw_edf("data/S001R01.edf", preload=True)

data = raw.get_data()

signal = data[0] * 1e6  # перевод в микровольты

sfreq = raw.info['sfreq']  # частота дискретизации

time = np.arange(len(signal)) / sfreq

plt.plot(time, signal)
plt.title("EEG signal (channel 1)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (µV)")
plt.show()