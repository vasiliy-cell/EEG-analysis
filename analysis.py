import mne
import numpy as np
from scipy.signal import welch


raw_R01 = mne.io.read_raw_edf("data/S001R01.edf", preload=True)  #
raw_R01.pick(["O1..", "Oz..", "O2.."])               
data = raw_R01.get_data()          # numpy-массив (n_channels, n_samples), в ВОЛЬТАХ
data, times = raw_R01.get_data(return_times=True)  # + ось времени

x_R01 = data[0]              # 1-D массив ОДНОГО канала — это и есть "сигнал"
N_R01 = len(x_R01)               # длина x в отсчётах (напр. 9600 = 60 c × 160)

from scipy.signal import welch
f_R01, Pxx_R01 = welch(x_R01, fs=160, window="hann", nperseg=320, noverlap=160, scaling="density")

np.set_printoptions(suppress=True, precision=3)   # без «e», 3 знака

mask = (f_R01 >= 8) & (f_R01 <= 13)
alpha_power_R01 = np.trapz(Pxx_R01[mask], f_R01[mask])
print(alpha_power_R01)      


# ==========================================================================================
# ==========================================================================================
# ==========================================================================================


raw_R02 = mne.io.read_raw_edf("data/S001R02.edf", preload=True)  #
data = raw_R02.get_data()        
raw_R02.pick(["O1..", "Oz..", "O2.."])               
data, times = raw_R02.get_data(return_times=True)  # + ось времени

x_R02 = data[0]              

from scipy.signal import welch
f_R02, Pxx_R02 = welch(x_R02, fs=160, window="hann", nperseg=320, noverlap=160, scaling="density")

np.set_printoptions(suppress=True, precision=3)   # без «e», 3 знака

mask = (f_R02 >= 8) & (f_R02 <= 13)
alpha_power_R02 = np.trapz(Pxx_R02[mask], f_R02[mask])
print(alpha_power_R02) 
