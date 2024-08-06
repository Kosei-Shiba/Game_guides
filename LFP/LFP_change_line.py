import pandas as pd
import matplotlib.pyplot as plt

# データの読み込み
# ここでは"your_data.csv"を適切なファイル名に変更してください
data = pd.read_csv("LFP_plasticity_US.csv", header=0)  # 1行目をヘッダーとして読み込み

# 1列目を無視する（2列目以降を抽出）
data_subset = data.iloc[:, 1:]


# 平均と標準偏差を計算
means = data_subset.mean()
std = data_subset.std()

# サブプロットの作成
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(4, 4))
plo_d = [0.2, 0.5, 0.8]
# shamのプロット
us_plot = axes[0].errorbar(plo_d, means[:len(means)//2], yerr=std[:len(means)//2], fmt='o', capsize=5, markersize=8, color='k')
axes[0].set_ylabel('LFP Amplitude',fontsize=16)
axes[0].set_title('sham',fontsize=16)
axes[0].set_xticks(plo_d)
axes[0].set_xticklabels(['Pre', 'T5', 'T15'], fontsize=12)

# tbUSのプロット
sham_plot = axes[1].errorbar(plo_d, means[len(means)//2:], yerr=std[len(means)//2:], fmt='o', capsize=5, markersize=8, color='k')
axes[1].set_title('tbUS',fontsize=16)
axes[1].set_xticks(plo_d)
axes[1].set_xticklabels(['Pre', 'T5', 'T15'], fontsize=12)

min_value = min(min(means[:len(means)//2] - std[:len(means)//2]), min(means[len(means)//2:] - std[len(means)//2:]))
max_value = max(max(means[:len(means)//2] + std[:len(means)//2]), max(means[len(means)//2:] + std[len(means)//2:]))
for ax in axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(min_value-(max_value-min_value)*0.1, max_value+(max_value-min_value)*0.1)

axes[0].plot(plo_d, means[:len(means)//2], linestyle='-', marker='o', color='k')
axes[1].plot(plo_d, means[len(means)//2:], linestyle='-', marker='o', color='k')

axes[0].plot([0,0.5,1], means[:len(means)//2], linestyle='-', marker='o', color='k', alpha=0) 
axes[1].plot([0,0.5,1], means[len(means)//2:], linestyle='-', marker='o', color='k', alpha=0)

# 全体のレイアウト調整
plt.tight_layout()
plt.show()