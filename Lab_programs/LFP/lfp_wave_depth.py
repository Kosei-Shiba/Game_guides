import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

samplerate = 40000

lfp_wave = pd.read_csv('./Data/after_US.csv', header = 0) # read lfp wave data
lfp_wave = lfp_wave.rename(columns = int) # columns change to int from str
lfp_wave.insert(0, 'time[ms]', np.arange(-50, -50+len(lfp_wave[0])/samplerate*1000, 1000/samplerate))
lfp_wave=lfp_wave.drop([8,9,10,11,12,13,14,15], axis=1) # for 8ch data

num_list = list(lfp_wave.select_dtypes(exclude=object).columns)
depth_list = np.arange(0, 1600, 200)
fig, ax = plt.subplots(len(lfp_wave.T)-1, 1, figsize=(5, 6))

for i in range(len(lfp_wave.T)-1):
    ax[i].plot(lfp_wave['time[ms]'], lfp_wave[num_list[i+1]], c='k')
    ax[i].set_ylabel(depth_list[i], rotation=0, fontsize=12)
    ax[i].yaxis.set_label_coords(-0.06, 0.3)
    ax[i].set_ylim(-300,300)
    #ax[i].set_yticks(np.arange(-2, 3, 2))
    ax[i].set_xlim(-50,350)
    ax[i].spines['right'].set_visible(False)
    ax[i].spines['left'].set_visible(False)
    ax[i].spines['top'].set_visible(False)
    ax[i].spines['bottom'].set_visible(False)
    ax[i].set_xticks([])
    ax[i].set_yticks([])
    ax[i].hlines(y=0, xmin=-50, xmax=350, color='k', alpha=0.2, linestyles='dashed')
    ax[i].vlines(x=0, ymin=-500, ymax=500, color='k', alpha=0.2, linestyles='solid')
    
# set overrall scales and labels
ax_main = ax[-1]
ax_main.plot(lfp_wave['time[ms]'], np.zeros_like(lfp_wave['time[ms]']), visible=False) # add dummy plot for scale
ax_main.set_xticks(np.arange(-50, 360, 50)) # set scale position
ax_main.spines['bottom'].set_position(('outward', 10))
ax_main.spines['bottom'].set_visible(True)
ax_main.tick_params(bottom=True, top=False) # hidden top scale
ax_main.yaxis.tick_right()
ax_main.yaxis.set_label_position("right")
ax_main.set_yticks(np.arange(-200, 300, 200))
ax_main.vlines(x=350, ymin=-200, ymax=200, color='k', alpha=1, linestyles='solid')
fig.supxlabel('Time from Stimulation (ms)', fontsize=16)
fig.text(0, 0.5, 'Depth from Brain Surface (\u03bcm)', va='center', rotation='vertical', fontsize=16)

ax[-1].yaxis.set_label_coords(-0.06, 0.7)
#fig.tight_layout()
plt.subplots_adjust(left=0.15, right=0.9, top=0.95, bottom=0.11, hspace=0.01)
plt.text(375,-50,'\u03bcV')
plt.text(-4.5,4500, '▼ onset')

plt.show()