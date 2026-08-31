# EEG alpha rhythm — eyes open vs eyes closed

### what is it ?

Basically a learning project. I wanted to lock in the theory of how EEG actually
works, try Fourier on real live data instead of textbook examples, and see what
comes out the other end.

To check that my code actually works, I picked one of the most well-established
and easiest-to-spot effects in all of EEG. I took two `.edf` recordings of the
same person — one with the eyes open, one with the eyes closed — and looked at
the power in the alpha band. And the result speaks for itself: **alpha power
went up ~13× after closing the eyes.**

That's the Berger effect, described back in 1929. Nice to see it fall out of my
own 100 lines of Python.

![alpha power comparison](./Screenshot%202026-08-31%20at%2011.37.37.png)

### the numbers

Channel **O1** (occipital — alpha is strongest at the back of the head),
integrating the Welch PSD over 8–13 Hz:

| run | condition | alpha power |
|-----|-----------|-------------|
| R01 | eyes open | 287.5 µV² |
| R02 | eyes closed | **3732.7 µV²** |
| | | **×12.98** |

With the eyes closed a sharp peak shows up at exactly **10 Hz** — textbook alpha.
With the eyes open there's basically nothing there.

### how it works

1. Load the `.edf` with MNE, keep only the occipital channels `O1 / Oz / O2`.
2. Take one channel as a plain 1-D signal.
3. Welch PSD — Hann window, 320 samples (2 s), 50 % overlap, `fs = 160 Hz`.
4. Integrate the spectrum over 8–13 Hz with the trapezoid rule → that single
   number is the alpha power.
5. Do the same for both runs, compare.

### the data

[PhysioNet EEG Motor Movement/Imagery Dataset](https://physionet.org/content/eegmmidb/1.0.0/),
subject S001. 64 channels, 160 Hz, ~1 minute per run.

- `data/S001R01.edf` — baseline, eyes open
- `data/S001R02.edf` — baseline, eyes closed

### requirements

Python 3.9+ and:

```
mne==1.8.0
numpy==2.0.2
scipy==1.13.1
matplotlib==3.9.4
```

```bash
python -m venv venv
source venv/bin/activate
pip install mne numpy scipy matplotlib
```

### running it

```bash
python analysis.py      # prints the two alpha-power values
python plot_alpha.py    # opens the comparison plot
```

`plot_alpha.py` doesn't recompute anything — it imports `analysis.py` and plots
the values that are already in there (`Pxx_R01`, `Pxx_R02`, `alpha_power_R01`,
`alpha_power_R02`). So if you change the analysis, the plot follows on its own.


