"""
作成日：
作成者：
目的：matファイルを読み込んでLFP波形を描画する
"""


import matplotlib.pyplot as plt
import numpy as np

import tkinter as tk
from tkinter import filedialog
import scipy.io
from scipy import signal



## matファイル読み込み
root = tk.Tk()
root.withdraw()

mat_file = filedialog.askopenfilename(title="Open matlab file.", filetypes=[("matlab file", "*.mat")])
print(mat_file)

mat = scipy.io.loadmat(mat_file)

## 変数設定
sampling_rate = 4*10**4

ch_num = 16
ch_cate = "WB"
ch_map = [8,7,9,6,12,3,11,4,14,1,15,0,13,2,10,5]
#青：8,7,9,6,12,3,11,4,14,1,15,0,13,2,10,5
#赤：7,8,6,9,3,12,4,11,1,14,0,15,2,13,5,10

## chごとの時間列データに成形
ch_name = []
for i in range(ch_num):
    num_name = f"{i+1:02}"

    ch_name.append(ch_cate + num_name)
    data = (mat[ch_name[i]])
    N = data.size
    if i == 0:
        all_data = data
        continue
    else:
        all_data = np.vstack((all_data, data))
ana_data = all_data[ch_map, :]
print(ana_data)
## eventのずれを求める（補正はフィルタ時に行う）
event_gap_name = []
for i in range(ch_num):
        num_name = f'{i+1:02}'
        
        event_gap_name.append(ch_cate + num_name + '_ts')

        if i == 0:
            event_gap_time = (mat[event_gap_name[i]])
            continue
        else:
            event_gap_time = np.vstack((event_gap_time, mat[event_gap_name[i]]))

#print(event_gap_time*sampling_rate)

for i in range(ch_num):
    if i == 0:
        event_gap = np.zeros(int(event_gap_time[i]*sampling_rate))
    else:
        event_gap = np.vstack((event_gap, np.zeros(int(event_gap_time[i]*sampling_rate))))

## Low Pass Filter
filt_type = "low"
fp = 300 # 通過域端周波数[Hz]
fs = 600 # 阻止域端周波数[Hz]

gpass = 3 # 通過域端最大損失[dB]
gstop = 40 # 阻止域端最小損失[dB]

def lowpass(ana_data, samplerate, fp, fs, filt_type, channel_kazu, event_gap):
    
    fn = samplerate / 2   #ナイキスト周波数
    wp = fp / fn  #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn  #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  #オーダーとバタワースの正規化周波数を計算
    b, a = signal.butter(N, Wn, filt_type)            #フィルタ伝達関数の分子と分母を計算
    padlen = max(len(a), len(b))
    for i in range(channel_kazu):
        y = signal.filtfilt(b, a, ana_data[i], padlen=padlen)                  #信号に対してフィルタをかける
        z = np.concatenate((event_gap[i], y), axis=None)

        if i == 0:
            filt_all = z
            continue
        elif i == 1:

            filt_all = np.append([filt_all], [z], axis=0)
        else:
            filt_all = np.append(filt_all, [z], axis=0)
    return filt_all

filt_data = lowpass(ana_data, sampling_rate, fp, fs, filt_type, ch_num, event_gap)

print(filt_data)

## eventデータ取得