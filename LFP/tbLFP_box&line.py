import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import scikit_posthocs as sp
from scipy.stats import rankdata
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data = pd.read_csv("tbLFP.csv", header=0)  # 1行目をヘッダーとして読み込み

# 1列目を無視する（2列目以降を抽出）
data_subset = data.iloc[:, 1:]
data_subset = -data_subset * 1000

means = data_subset.mean()
sem = data_subset.std() / 4
means.index = range(1, len(means) + 1)
sem.index = range(1, len(sem) + 1)

group_size = 50
mean_group = []
group_mean = [[] for _ in range(len(means) // group_size)]
i = 0
for i in range(len(means) // group_size):
    mean_group[0:50] = means[i*group_size:(i+1)*group_size]
    group_mean[i] = mean_group[0:50]
    print(len(group_mean[i]))
    i += 1
data = pd.DataFrame({f'Group_{i + 1}': group for i, group in enumerate(group_mean)})
# データをmeltしてフォーマット
data_melted = data.melt(var_name='groups', value_name='values')
# Steel-Dwass test
result_steel_dwass = sp.posthoc_dscf(data_melted, val_col='values', group_col='groups')
# 結果の表示
print(result_steel_dwass)
#print(data)
fig, ax = plt.subplots(figsize=(8, 5))

# 上のグラフにプロット
means.plot(color='k', ax=ax, zorder=1)
ax.fill_between(means.index, means - sem, means + sem,
                 color='gray', alpha=0.3, label='Standard Deviation')

ax.set_xlabel('Bursts', fontsize=20)
ax.set_ylabel('LFP Amplitude (\u00B5V)', fontsize=20)
ax.set_xlim(-10, 410)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.hlines(y=0, xmin=350, xmax=400, color='k', lw=4)
ax.text(360, 5, '10 s', fontsize=12)

# 下のグラフにboxplotをプロット
boxprops = dict(linestyle='-', linewidth=1, color='gray', facecolor='lightblue')
medianprops = dict(color='r')
whiskerprops = dict(color='r')
capprops = dict(color='r')
positions = [25, 75, 125, 175, 225, 275, 325, 375]
bp = ax.boxplot(data.values, patch_artist=True, boxprops=boxprops, showfliers=True, medianprops=medianprops,
            whiskerprops=whiskerprops, capprops=capprops, positions=positions, widths=10, zorder=2)
#for box in bp['boxes']:
    #box.set_facecolor('lightblue')

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