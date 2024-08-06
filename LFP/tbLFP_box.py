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
data_subset = -data_subset*1000

means = data_subset.mean()
sem = data_subset.std()/4
means.index = range(1, len(means) + 1)
sem.index = range(1, len(sem) + 1)

group_size = 50
group_mean = [[] for _ in range(len(means)//group_size)]
i = 0
for i in range(len(means)//group_size):
    group_mean[i] = means[i*group_size:(i+1)*group_size]
    print(len(group_mean[i]))
    i += 1
data = pd.DataFrame({f'{i+1}': group for i, group in enumerate(group_mean)})
# データをmeltしてフォーマット
data_melted = data.melt(var_name='groups', value_name='values')
# Steel-Dwass test
result_steel_dwass = sp.posthoc_dscf(data_melted, val_col='values', group_col='groups')
# 結果の表示
print(result_steel_dwass)

#data.plot.box(color='b', figsize=(6,4))
boxprops = dict(linestyle='-', linewidth=1, color='gray', facecolor='lightblue')
medianprops = dict(color='r')
whiskerprops = dict(color='k')
capprops = dict(color='k')
bp = data.boxplot(patch_artist=True, boxprops=boxprops, showfliers=True,
                  medianprops=medianprops, whiskerprops = whiskerprops, capprops = capprops, figsize=(6,4))
for box in bp.artists:
    box.set_facecolor('lightblue')
plt.xlabel('Groups', fontsize=20)
plt.ylabel('LFP Amplitude (\u03bcV)', fontsize=20)
#plt.xlim(-10,410)
plt.ylim(0, 500)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.grid(False)
#plt.hlines(y=-0.44, xmin=350, xmax=400, color='k', lw=4)
#plt.text(360,-0.43,'10 s')

plt.tight_layout()
plt.show()