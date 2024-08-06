"""
created on June 7th 2023
created by Shiba Kosei
purpose: plot ABR wave
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Srate = 4e-2 # sampling cycle(ms)
dataN = 487 # time data
statime = -10 # measurement start（trigger is 0）
abr_wave = pd.read_csv('abr_20240222_A_tone2k.csv', usecols=[*range(48, 48+dataN)])

df = abr_wave.T
# setting columns
if len(abr_wave) == 7:
    df.columns = [ '80 dB SPL', '70 dB SPL', '60 dB SPL', '50 dB SPL', '40 dB SPL', '30 dB SPL', '20 dB SPL']
elif len(abr_wave) == 15:
    df.columns = [ '80 dB SPL', '75 dB SPL', '70 dB SPL', 
              '65 dB SPL', '60 dB SPL', '55 dB SPL', '50 dB SPL', '45 dB SPL', 
              '40 dB SPL', '35 dB SPL', '30 dB SPL', '25 dB SPL', '20 dB SPL',
             '15 dB SPL', '10 dB SPL']
else:
    """
    set solumns each time
    """
    df.columns = ['Sound\n(Pre)', 'TBUS 1', 'TBUS 2', 'Sound\n(Post5)', 'Sound\n(Post15)']
    #df.columns = ['tbUS']

df.insert(0, 'time[ms]', np.arange(statime, Srate*dataN+statime, Srate))

# plot each wave
fig_shape = (5,10)
num_list = list(df.select_dtypes(exclude=object).columns)
fig, ax = plt.subplots(len(num_list)-1, 1, figsize=fig_shape)

for i in range(len(num_list)-1):
    ax[i].plot(df['time[ms]'], df[num_list[i+1]], c='k')
    ax[i].set_ylabel(num_list[i+1], rotation=0, fontsize=12)
    ax[i].yaxis.set_label_coords(-0.15, 0.5)
    ax[i].set_ylim(-3,3)
    #ax[i].set_yticks(np.arange(-2, 3, 2))
    ax[i].set_xlim(-3,10)
    ax[i].spines['right'].set_visible(False)
    ax[i].spines['left'].set_visible(False)
    ax[i].spines['top'].set_visible(False)
    ax[i].spines['bottom'].set_visible(False)
    ax[i].set_xticks([])
    ax[i].yaxis.tick_right()
    ax[i].set_yticks(np.arange(-1, 2, 1))
    ax[i].vlines(x=10, ymin=-1, ymax=1, color='k', alpha=1, linestyles='solid')
    ax[i].hlines(y=0, xmin=-5, xmax=Srate*dataN+statime, color='k', alpha=0.2, linestyles='dashed')
    ax[i].vlines(x=0, ymin=-5, ymax=5, color='k', alpha=0.2, linestyles='solid')
    
    
    
    
# set overrall scales and labels
ax_main = ax[-1]
ax_main.plot(df['time[ms]'], np.zeros_like(df['time[ms]']), visible=False)  # add dummy plot for scale
ax_main.set_xticks(np.arange(-2, 10, 2))  # set scale position
ax_main.spines['bottom'].set_position(('outward', 10))
ax_main.spines['bottom'].set_visible(True)
ax_main.tick_params(bottom=True, top=False)  # hidden top scale
ax_main.yaxis.tick_right()
ax_main.yaxis.set_label_position("right")
ax_main.set_yticks(np.arange(-1, 2, 1))
ax_main.vlines(x=10, ymin=-1, ymax=1, color='k', alpha=1, linestyles='solid')
fig.supxlabel('Time (ms)', fontsize=16)


#fig.tight_layout()
plt.subplots_adjust(left=0.2, right=0.9, top=0.95, bottom=0.1, hspace=0.01)
plt.text(11,0,'\u00B5V')
plt.text(-0.20,88.0, '▼ onset')

plt.show()
