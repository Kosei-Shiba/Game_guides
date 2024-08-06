import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel
from scipy import stats

# データの読み込み
data = pd.read_csv("rLFP.csv", header=0)  # 1行目をヘッダーとして読み込み

# 1列目を無視する（2列目以降を抽出）
data_subset = data.iloc[:, 1:]
data_subset.insert(0, 'sham_pre', 1)  # 1列目に0の行を挿入
data_subset.insert(7, 'stim_pre', 1)  # 4列目に0の行を挿入
data_subset = data_subset

print(data_subset)

#T-test
t_statistic, p_value = ttest_rel(data_subset['sham30'], data_subset['stim30'])
print(f"T-statistic: {t_statistic}")
print(f"P-value: {p_value}")

#Wilcoxon signed-rank test
w_test = stats.wilcoxon(data_subset['sham5'], data_subset['stim5'], alternative='two-sided')
print(w_test)

#折れ線グラフの描画
fig, ax = plt.subplots(figsize=(4, 5))
data_subset.iloc[:, :len(data_subset.columns)//2].T.plot(ax=ax, color='gray', linestyle='-', marker='^')
data_subset.iloc[:, len(data_subset.columns)//2:].T.plot(ax=ax, color='orange', linestyle='-', marker='o')

ax.set_ylabel('LFP Amplitude Change (\u03bcV)', fontsize=16)
ax.set_xlabel('Time from TB US (min)', fontsize=16)
#ax.set_ylim(-80, 120)
ax.set_xticks(range(len(data_subset.T)//2))
#ax.set_xticklabels(['-5', '5', '15'], fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=[handles[0], handles[-1]], labels=['Sham', 'TB US'], frameon=False, ncol=1, fontsize=11, loc = "upper left")
#ax.get_legend().remove()
#plt.title('Sham', fontsize=16)
# 全体のレイアウト調整
plt.tight_layout()
plt.show()