import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# データの読み込み
# ここでは"your_data.csv"を適切なファイル名に変更してください
data = pd.read_csv("LFP_plasticity_sound.csv", header=0)  # 1行目をヘッダーとして読み込み

# 1列目を無視する（2列目以降を抽出）
data_subset = data.iloc[:, 1:]

#Wilcoxon signed-rank sum test
w_test = stats.wilcoxon(data_subset['sham_pre'], data_subset['sham_T15'], alternative='two-sided')
print(w_test)

# 平均と標準偏差を計算
means = data_subset.mean()
std = data_subset.std()

# サブプロットの作成
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(4, 4))
plo_d = [1, 3, 5]
# shamのプロット
sham_positions = [0.75, 2.75, 4.75]
sham_plot = axes[0].boxplot(data_subset.iloc[:, :len(data_subset.columns)//2].values, positions = sham_positions,
           widths=1, patch_artist=True, boxprops=dict(facecolor='gray'), medianprops=dict(color='k'))
axes[0].set_ylabel('LFP Amplitude',fontsize=16)
axes[0].set_title('sham',fontsize=16)
axes[0].set_xticks(plo_d)
axes[0].set_xticklabels(['Pre', 'T5', 'T15'], fontsize=12)

# tbUSのプロット
tbus_positions = [1.25, 3.25, 5.25]
tbus_plot = axes[1].boxplot(data_subset.iloc[:, len(data_subset.columns)//2:].values,positions = tbus_positions,
           widths=1, patch_artist=True, boxprops=dict(facecolor='orange'), medianprops=dict(color='k'))
axes[1].set_title('tbUS',fontsize=16)
axes[1].set_xticks(plo_d)
axes[1].set_xticklabels(['Pre', 'T5', 'T15'], fontsize=12)

sham_whiskers = sham_plot['whiskers']
tbus_whiskers = tbus_plot['whiskers']
sham_q1 = sham_whiskers[0].get_ydata()[1]
sham_q3 = sham_whiskers[1].get_ydata()[1]
tbus_q1 = tbus_whiskers[0].get_ydata()[1]
tbus_q3 = tbus_whiskers[1].get_ydata()[1]
min_value = min(sham_q1, tbus_q1)
max_value = max(sham_q3, tbus_q3)
for ax in axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(min_value-(max_value-min_value)*0.05, max_value+(max_value-min_value)*0.2)

axes[0].plot([0,3,6], means[:len(means)//2], linestyle='-', marker='o', color='k', alpha=0) 
axes[1].plot([0,3,6], means[len(means)//2:], linestyle='-', marker='o', color='k', alpha=0)

# 全体のレイアウト調整
plt.tight_layout()
plt.show()