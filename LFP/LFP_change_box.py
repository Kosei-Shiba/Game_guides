import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# データの読み込み
data = pd.read_csv("LFP_plasticity_US.csv", header=0)  # 1行目をヘッダーとして読み込み

# 1列目を無視する（2列目以降を抽出）
data_subset = data.iloc[:, 1:]
print(data_subset.columns)

# 箱ひげ図の描画
fig, ax = plt.subplots(figsize=(4, 5))
print(data_subset.iloc[:, len(data_subset.columns)//2:].values.T)
positions = np.arange(1,+1*len(data_subset.T),2)
print(positions)
# Shamの箱ひげ図
sham_positions = positions-0.25
ax.boxplot(data_subset.iloc[:, :len(data_subset.columns)//2].values, sym='', positions = sham_positions,
           widths=0.4, patch_artist=True, boxprops=dict(facecolor='gray'), medianprops=dict(color='k'))

# tbUSの箱ひげ図
tbus_positions = positions+0.25
ax.boxplot(data_subset.iloc[:, len(data_subset.columns)//2:].values, sym='', positions = tbus_positions,
           widths=0.4, patch_artist=True, boxprops=dict(facecolor='orange'), medianprops=dict(color='k'))

ax.set_ylabel('LFP Amplitude (mV)', fontsize=16)
ax.set_xlabel('Time from tbUS (min)', fontsize=16)

ax.set_xticks([1, 3, 5])
ax.set_xticklabels(['-5', '5', '15'], fontsize=12)  # 各条件ごとにラベルを設定
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 凡例を手動で指定
handles = [plt.Rectangle((0, 0), 1, 1, fc='gray', edgecolor='none'), plt.Rectangle((0, 0), 1, 1, fc='orange', edgecolor='none')]
ax.legend(handles, ['Sham', 'tbUS'], frameon=False, ncol=2, fontsize=10)

# 全体のレイアウト調整
plt.tight_layout()
plt.show()