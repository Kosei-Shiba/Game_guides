import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import scikit_posthocs as sp
from scipy.stats import rankdata
#from statsmodels.stats.multicomp import pairwise_tukeyhsd

data = pd.read_csv("tbLFP.csv", header=0)  # 1行目をヘッダーとして読み込み

# 1列目を無視する（2列目以降を抽出）
data_subset = data.iloc[:, 1:]
data_subset = -data_subset * 1000

means = data_subset.mean()
sems = data_subset.std() / 4
means.index = range(1, len(means) + 1)
sems.index = range(1, len(sems) + 1)

group_size = 50
group_mean = [[] for _ in range(len(means) // group_size)]
group_sem = [[] for _ in range(len(means) // group_size)]
i = 0
for i in range(len(means) // group_size):
    mean_group = np.mean(means[i*group_size:(i+1)*group_size])
    group_mean[i] = mean_group
    #sem_group = np.std(means[i*group_size:(i+1)*group_size])/np.sqrt(group_size) #標準誤差で描画
    sem_group = np.std(means[i*group_size:(i+1)*group_size]) #標準偏差で描画
    group_sem[i] = sem_group
    i += 1
#data = pd.DataFrame({f'Group_{i + 1}': group for i, group in enumerate(group_mean)})
#data_sem = pd.DataFrame({f'Group_{i + 1}': group for i, group in enumerate(group_sem)})
print('done')

fig, ax = plt.subplots(figsize=(8, 5))

# 上のグラフにプロット
means.plot(color='k', ax=ax, zorder=1)
ax.fill_between(means.index, means - sems, means + sems,
                 color='gray', alpha=0.3, label='Standard Deviation')

ax.set_xlabel('Bursts', fontsize=20)
ax.set_ylabel('LFP Amplitude (\u00B5V)', fontsize=20)
ax.set_xlim(-10, 410)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.hlines(y=0, xmin=350, xmax=400, color='k', lw=4)
ax.text(360, 5, '10 s', fontsize=12)

# 下のグラフにerrorbarをプロット
positions = [25, 75, 125, 175, 225, 275, 325, 375]
eb = ax.errorbar(positions, group_mean, yerr=group_sem, color='r', fmt='o', markersize=10, ecolor='orange', lw=5, capsize=10, capthick=3, zorder=2)
ml = ax.plot(positions, group_mean, color='r')

ax.set_ylabel('LFP Amplitude (\u03bcV)', fontsize=20)
ax.set_ylim(0, 500)
ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.grid(False)
ax.set_xticks(range(0, 450, 50))
ax.set_xticklabels(range(0, 450, 50))

plt.tight_layout()
plt.show()