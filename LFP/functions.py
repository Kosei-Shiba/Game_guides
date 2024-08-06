import numpy as np
from scipy import signal
import scipy.io
from numpy import zeros
from scipy import interpolate
import json

#青コネクタ16ch　
def load_mat(mat_name):
    mat = scipy.io.loadmat(mat_name)
    return mat

def load_json(json_name):
    json_open = open(json_name, 'r')
    json_load = json.load(json_open)
    return json_load

def get_channel_data(mat, channel_kazu, kinds_of_channel, magical_channel_data):
    print(mat)
    channel_name = []
    for i in range(channel_kazu):
        kazu_name = f'{i+1:02}'
        
        channel_name.append(kinds_of_channel + kazu_name)
        data = (mat[channel_name[i]])
        print(data)
        N = data.size
        data = data.reshape((N,))
        print(data)
        if i == 0:
            data_all = data
            continue
        elif i == 1:
            data_all = np.vstack((data_all, data))
        else:
            data_all = np.vstack((data_all, data))

    data_all_final = data_all[magical_channel_data, :]
    return data_all_final, N
    #11,9,13,5,7,15,3,1,0,2,14,6,4,12,8,10
    #↑青チャンネル

def lowpass(data_all, samplerate, fp, fs, filt_type, channel_kazu, event_gap):
    gpass = 3 # 通過域端最大損失[dB]
    gstop = 40 # 阻止域端最小損失[dB]

    fn = samplerate / 2   #ナイキスト周波数
    wp = fp / fn  #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn  #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  #オーダーとバタワースの正規化周波数を計算
    b, a = signal.butter(N, Wn, filt_type)            #フィルタ伝達関数の分子と分母を計算
    for i in range(channel_kazu):
        y = signal.filtfilt(b, a, data_all[i])                  #信号に対してフィルタをかける
        z = np.concatenate((event_gap[i], y), axis=None)

        if i == 0:
            filt_all = z
            continue
        elif i == 1:

            filt_all = np.append([filt_all], [z], axis=0)
        else:
            filt_all = np.append(filt_all, [z], axis=0)
    return filt_all

def load_event_data(mat, event_name):
    event = (mat[event_name])
    return event

def each_event_waveform(filt_all, event, samplerate, before_event, after_event, channel_kazu):
    N_event = event.size

    each_event_response = zeros([channel_kazu, N_event, int((-before_event+after_event)*samplerate)+1])  #+1はt=0の時

    for i, x in enumerate(event):
        first = int((x*samplerate) + before_event*samplerate)
        last = int((x*samplerate) + after_event*samplerate)
        for k in range(channel_kazu):
            j = 0
            while 1:
                each_event_response[k, i, j] = filt_all[k, first+j]
                j += 1
                if first+j > last:
                    break
    t_ave = np.arange(before_event, after_event, 1.0/samplerate)
    t_ave = np.append(t_ave, after_event)
    return N_event, each_event_response, t_ave

def average(each_event_response: np.ndarray, event, samplerate, before_event, after_event, channel_kazu):
    N_event = event.size

    sum_all = zeros([channel_kazu, int((-before_event+after_event)*samplerate)+1])
    for k in range(channel_kazu):
        for i, _ in enumerate(sum_all[k]):
            for j, _ in enumerate(event):
                sum_all[k, i] += each_event_response[k, j, i]

    
        average = sum_all[k] / float(N_event)
        if k == 0:
            ave_all = average
            continue
        elif k == 1:
            ave_all = np.append([ave_all], [average], axis=0)
        else:
            ave_all = np.append(ave_all, [average], axis=0)

    for i in range(channel_kazu):
        if i == 0:
            mov_ave = np.convolve(ave_all[i], np.ones(5), mode='valid')/5
        else:
            temp = np.convolve(ave_all[i], np.ones(5), mode='valid')/5
            mov_ave = np.vstack((mov_ave, temp))
    return mov_ave

def CSD(ave_all, channel_space, channel_kazu, samplerate, before_event, after_event):
    list_lfp = []
    for i in range(channel_kazu):
        list_lfp.append(ave_all[i])
    
    csd = - 0.3 * np.gradient(np.gradient(list_lfp, axis=0), axis=0) / 0.05**2
    #csd = -0.3 * np.gradient(np.gradient(ave_all, axis=0), axis=0)/(0.05**2)
    return csd

def CSD_mesh(ave_all, channel_space, channel_kazu, samplerate, before_event, after_event):
    list_lfp = []
    for i in range(channel_kazu):
        list_lfp.append(ave_all[i])
    x = np.linspace(50, (channel_kazu*50), channel_kazu)
    
    list_lfp = list_lfp[::-1]
    csd = - 0.3 * np.gradient(np.gradient(list_lfp, axis=0), axis=0) / 0.05**2
    csd_y_itp = interpolate.interp1d(x, csd, kind='slinear', axis=0)
    X = np.linspace(x[0],x[-1],num=100,endpoint=True)
    #csd = -0.3 * np.gradient(np.gradient(ave_all, axis=0), axis=0)/(0.05**2)
    return csd_y_itp, X