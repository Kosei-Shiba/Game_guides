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

half_len = len(means) // 2
means_first_half = means[:half_len].mean()
sem_first_half = means[:half_len].std()/np.sqrt(len(data))
means_last_half = means[half_len:].mean()
sem_lst_half = means[:half_len:].std()/np.sqrt(len(data))
#print(means_first_half, sem_first_half, means_last_half, sem_lst_half)
#Wilcoxon signed-rank sum test
first_half = means[:half_len]
last_half = means[half_len:]
#u_test = stats.mannwhitneyu(first_half, last_half, alternative='two-sided')
#print(u_test)

group_size = 40
group_mean = [[] for _ in range(len(means)//group_size)]
i = 0
for i in range(len(means)//group_size):
    group_mean[i] = means[i*group_size:(i+1)*group_size]
    i += 1
data = pd.DataFrame({f'Group_{i+1}': group for i, group in enumerate(group_mean)})
# データをmeltしてフォーマット
data_melted = data.melt(var_name='groups', value_name='values')
# Steel-Dwass test
result_steel_dwass = sp.posthoc_dscf(data_melted, val_col='values', group_col='groups')
# 結果の表示
print(result_steel_dwass)

means.plot(boxprops=dict(facecolor='gray'), medianprops=dict(color='k'))
plt.fill_between(means.index, means - sem, means + sem, color='gray', alpha=0.3, label='Standard Deviation')
plt.xlabel('Bursts', fontsize=16)
plt.ylabel('LFP Amplitude (\u00B5V)', fontsize=16)
plt.xlim(-10,410)
#plt.ylim(-0.45,0)
#plt.xticks(np.arange(0, 500, 50))
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.hlines(y=0, xmin=350, xmax=400, color='k', lw=2)
plt.text(360,4,'10 s')

plt.tight_layout()
plt.show()