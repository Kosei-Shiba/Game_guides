import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_rel
from scipy import stats

# データの読み込み
data = pd.read_csv("rLFP.csv", header=0)  # 1行目をヘッダーとして読み込み

# 1列目を無視する（2列目以降を抽出）
data_subset = data.iloc[:, 1:]
data_subset = data_subset

#print(data_subset)

#T検定
t_statistic, p_value = ttest_rel(data_subset['sham30'], data_subset['stim30'])
#print(f"T-statistic: {t_statistic}")
#print(f"P-value: {p_value}")

#Mannwhitney U test
u_test = stats.mannwhitneyu(data_subset['sham30'], data_subset['stim30'], alternative='two-sided')
print(u_test)

#boxplotの描画
fig, ax = plt.subplots(figsize=(8, 5.5))
positions = np.arange(0, len(data_subset.T)//2, 1)
sham_positions = positions-0.2
ax.boxplot(data_subset.iloc[:, :len(data_subset.columns)//2].values, positions = sham_positions,
           widths=0.3, patch_artist=True, boxprops=dict(facecolor='gray'), medianprops=dict(color='k'))
tbus_positions = positions+0.2
ax.boxplot(data_subset.iloc[:, len(data_subset.columns)//2:].values, positions = tbus_positions,
           widths=0.3, patch_artist=True, boxprops=dict(facecolor='orange'), medianprops=dict(color='k'))

ax.set_ylabel('LFP Amplitude Change', fontsize=20)
ax.set_xlabel('Time from TB US (min)', fontsize=20)
#ax.set_ylim(-80, 140)
ax.set_xticks(range(len(data_subset.T)//2))
ax.set_xticklabels(['5', '10', '15', '20', '25', '30'], fontsize=16)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
#plt.title('Sound', fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# 凡例を手動で指定
handles = [plt.Rectangle((0, 0), 1, 1, fc='gray', edgecolor='none'), plt.Rectangle((0, 0), 1, 1, fc='orange', edgecolor='none')]
ax.legend(handles, ['Sham', 'TB US'], frameon=False, ncol=1, fontsize=14, loc = "upper left")
# 全体のレイアウト調整
plt.tight_layout()
plt.show()