import functions
import matplotlib.pyplot as plt
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog
import json
import pandas as pd
from scipy.fft import fft
from scipy import signal
import csv


samplerate = 40000

data_all = pd.read_csv('./Data/after_US.csv', header = 0)
data_all = data_all.rename(columns = int)
data_all.insert(0, 'time[ms]', np.arange(-50, -50+len(data_all[0])/samplerate*1000, 1000/samplerate))
data_all=data_all.drop([8,9,10,11,12,13,14,15], axis=1)

F = np.fft.fft(data_all[7], n=None)
dt = 1/samplerate
N = len(F)
freq = np.fft.fftfreq(N, dt)

Amp = np.abs(F/(N/2)) 

fig, ax = plt.subplots()
ax.plot(freq[1:int(N/2)], Amp[1:int(N/2)], color='k')
ax.set_xlabel("Freqency (Hz)")
ax.set_ylabel("Amplitude")
ax.set_xlim(0,30)
plt.show()