
import mne
import matplotlib.pyplot as plt

# загружаем файл
raw = mne.io.read_raw_edf("data/S001R01.edf", preload=True)

# достаём данные
data = raw.get_data()

# берём 1 канал
signal = data[0]

# рисуем
plt.plot(signal)
plt.title("EEG signal (channel 1)")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.show()