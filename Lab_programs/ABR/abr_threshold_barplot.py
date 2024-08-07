import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# read csv
abr_th_before = pd.read_csv('ABR_threshold_20240222.csv', header=0)
abr_th_after = pd.read_csv('20240307_threshold_change.csv', header=0)

headers_before = abr_th_before.columns.tolist()
headers_after = abr_th_after.columns.tolist()

mean_before = abr_th_before.iloc[:, 1:].mean(axis=1)
std_before = abr_th_before.iloc[:, 1:].std(axis=1)
mean_after = abr_th_after.iloc[:, 1:].mean(axis=1)
std_after = abr_th_after.iloc[:, 1:].std(axis=1)

fig, ax = plt.subplots()

x = abr_th_before['Frequency']
width = x * 0.2
ax.bar(x=x-width/2, height=mean_before, yerr=std_before, width=width*0.8, capsize=5, label='Before')
ax.bar(x=x+width/2, height=mean_after, yerr=std_after, width=width*0.9, capsize=5, label='After')

#ax.set_title('ABR Threshold', fontsize=16)
ax.set_xlabel('Frequency (kHz)', fontsize=16)
ax.set_ylabel('Sound Pressure Level (dB SPL)', fontsize=16)
ax.set_xscale('log')
ax.set_xticks([2, 4, 8, 16, 32]) # freqency
ax.set_xticklabels(['2', '4', '8', '16', '32'])
ax.tick_params(axis='x', which='both', bottom=True)
ax.tick_params(axis='x', which='minor', bottom=False)
ax.set_yticks([0, 20, 40, 60, 80])
ax.set_ylim(0, 90)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.legend(ncol=2, fontsize=14)

plt.tight_layout()
plt.show()
