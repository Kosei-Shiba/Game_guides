"""
created on June 9th 2023
created by Shiba Kosei
purpose:calculate Zscore by ABR
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Srate = 4e-2 # sampling cycle(ms)
dataN = 487 # time data
statime = -10 #　measurement start（trigger is 0）
abr_wave = pd.read_csv('abr_20240307_A_click.csv', usecols=[*range(48, 48+dataN)])

df = abr_wave.T
# setting columns
if len(abr_wave) == 7:
    df.columns = [ '80dB', '70dB', '60dB', '50dB', '40dB', '30dB', '20dB']
elif len(abr_wave) == 15:
    df.columns = [ '80dB SPL', '75dB SPL', '70dB SPL', 
              '65dB SPL', '60dB SPL', '55dB SPL', '50dB SPL', '45dB SPL', 
              '40dB SPL', '35dB SPL', '30dB SPL', '25dB SPL', '20dB SPL',
             '15dB SPL', '10dB SPL']
else:
    """
    set solumns each time
    """
    df.columns = ['Pre', 'tb1', 'tb2', 'T5', 'T15']
    #df.columns = ['tbUS']
df.insert(0, 'time[ms]', np.arange(statime, Srate*dataN+statime, Srate))

# calculate statistics
ave = df[(df['time[ms]'] <= 0) & (df['time[ms]']>=-10)].mean()
sd = df[(df['time[ms]'] <= 0) & (df['time[ms]']>=-10)].std()
#df = df.abs()
#df['time[ms]'] = np.arange(statime, Srate*dataN+statime, Srate)
response = df[(df['time[ms]'] >= 0.5) & (df['time[ms]'] <= 2.5)].max()
z_score = (response-ave)/sd
#print(df[(df['time[ms]'] >= 0.5) & (df['time[ms]'] <= 2.5)].idxmax())
print(z_score.iloc[1:len(z_score)])
