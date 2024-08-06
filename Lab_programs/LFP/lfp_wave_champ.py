import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

samplerate = 40000

lfp_wave = pd.read_csv('./Data/after_US.csv', header = 0) # read lfp wave data
lfp_wave = lfp_wave.rename(columns = int) # columns change to int from str
lfp_wave.insert(0, 'time[ms]', np.arange(-50, -50+len(lfp_wave[0])/samplerate*1000, 1000/samplerate))
lfp_wave=lfp_wave.drop([8,9,10,11,12,13,14,15], axis=1) # for 8ch data

depth = 5
lfp_wave.plot(x='time[ms]',y=depth, c='k', xlim=[-50,250], figsize=(4,3))
#plt.title('LFP US stim 900 \u03bcm', fontsize=16)
#plt.title('Ultra Sound 247 kPa', fontsize=16)
plt.xlabel('Time (ms)', fontsize=16)
plt.ylabel('Volt (\u03bcV)', fontsize=16)
plt.ylim(-300, 100)
plt.vlines(x=0, ymin=-300, ymax=150, color='k', alpha=0.2, linestyles='solid')

plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.vlines(x=0, ymin=-0.2, ymax=0.05, color='k', alpha=0.2, linestyles='dotted')
plt.hlines(y=lfp_wave[depth][(lfp_wave['time[ms]'] >= -5) & (lfp_wave['time[ms]'] <= 0)].mean(),
 xmin=-50, xmax=350, color='k', alpha=0.2, linestyle='dashed')
dimension = True
if dimension == True:
    plt.vlines(x=250, ymin=-250, ymax=-150, color='k', lw=4)
    plt.hlines(y=-250, xmin=200, xmax=250, color='k', lw=2)
    #plt.text(350, -250, '100 \u03bcV', rotation=270, fontsize=20)
    #plt.text(250,-300,'100 ms', fontsize=20)
#plt.hlines(y=[-0.02], xmin=-50, xmax=200, color='k', alpha=0.8, linestyle='dotted')
#plt.axvspan(xmin=0, xmax=100, color='r', alpha=0.2)
plt.axis('off')

plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)

plt.legend().remove()
plt.show()