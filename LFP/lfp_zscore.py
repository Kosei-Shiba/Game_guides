import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

samplerate = 40000

lfp_wave = pd.read_csv('./Data/1ms_0%.csv', header = 0) # read lfp wave data
lfp_wave = lfp_wave.rename(columns = int) # columns change to int from str
lfp_wave.insert(0, 'time[ms]', np.arange(-50, -50+len(lfp_wave[0])/samplerate*1000, 1000/samplerate))
#lfp_wave=lfp_wave.drop([8,9,10,11,12,13,14,15], axis=1) # for 8ch data

ave = lfp_wave[(lfp_wave['time[ms]'] >= -5) & (lfp_wave['time[ms]'] <= 0)].mean()
sd = lfp_wave[(lfp_wave['time[ms]'] >= -5) & (lfp_wave['time[ms]'] <= 0)].std()
response = lfp_wave[(lfp_wave['time[ms]'] >= 0) & (lfp_wave['time[ms]'] <= 100)].min() # calculate LFP amplitude (N20)
lfp_amp = (response-ave)
z_score = (response-ave)/sd

print(lfp_amp)
