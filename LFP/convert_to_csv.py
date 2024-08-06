import functions
import os
import glob
from tkinter import filedialog
import pandas as pd
import numpy as np
import scipy
from scipy import signal

# ch setting
number_of_ch = 16
kinds_of_channel = 'WB'
samplerate = 40000
ch_map = [8,7,9,6,12,3,11,4,14,1,15,0,13,2,10,5]
# blue cord：8,7,9,6,12,3,11,4,14,1,15,0,13,2,10,5
# red cord：7,8,6,9,3,12,4,11,1,14,0,15,2,13,5,10
# 一応置いてる：11,9,13,5,7,15,3,1,0,2,14,6,4,12,8,10
# 8ch blue:8,7,9,6,13,2,10,5,12,3,11,4,14,1,15,0
"""
ch_map number = data sheet number - 1 (1~16 → 0~15)
8ch blue [8,7,9,6,13,2,10,5] = data sheet[9,8,10,7,14,3,11,6]
"""
event_name = 'EVT01'

# filter setting
fp = 300 # passband edge frequency (Hz)
fs = 600 # stopband edge frequency (Hz)
filt_type = "low"        # high or low

# slice range (s), trigger is 0
before_event = -0.04
after_event = 1.0

# get path
dir_path = filedialog.askdirectory(initialdir = dir) 
file_list = glob.glob(os.path.join(dir_path, '*.mat'))

def channel_data(mat, number_of_ch, kinds_of_channel, ch_map):
    print(mat)
    channel_name = []
    for i in range(number_of_ch):
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

    data_all_final = data_all[ch_map, :]
    return data_all_final, N
    
def lowpass(data_all, samplerate, fp, fs, filt_type, channel_kazu, event_gap):
    gpass = 3 # maximum loss in passband (dB)
    gstop = 40 # maximum loss in stopband (dB)

    fn = samplerate / 2   # Nyquist frequency
    wp = fp / fn  # normalize passband edge frequency by frequency
    ws = fs / fn  # normalize stopband edge frequency by frequency
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  # calculate normalized frequency of order and butterworth
    b, a = signal.butter(N, Wn, filt_type)            # calculate numerator and denominator of filter transfer function
    for i in range(channel_kazu):
        y = signal.filtfilt(b, a, data_all[i]) # filtering
        z = np.concatenate((event_gap[i], y), axis=None)

        if i == 0:
            filt_all = z
            continue
        elif i == 1:

            filt_all = np.append([filt_all], [z], axis=0)
        else:
            filt_all = np.append(filt_all, [z], axis=0)
    return filt_all

# create csv file name by file path
def extract_between_chars(input_string, start_char, end_char):
    start_index = input_string.find(start_char)
    end_index = input_string.find(end_char)
    
    # exception handling
    if start_index == -1 or end_index == -1 or start_index >= end_index:
        return ''
    
    return input_string[start_index + 1:end_index]

all_data = False # amount of data is too large, don't save all_wave data except when necessary

# do not modify the contents of the for loop
for file_path in file_list:
    mat = scipy.io.loadmat(file_path)
    # create matrix of ch and time
    data_all, N = channel_data(mat, number_of_ch, kinds_of_channel, ch_map)

    # calculate event gaps（correction process is performed through filtering）
    event_gap_name = []
    for i in range(number_of_ch):
        kazu_name = f'{i+1:02}'
        
        event_gap_name.append(kinds_of_channel + kazu_name + '_ts')

        if i == 0:
            event_gap_time = (mat[event_gap_name[i]])
            continue
        else:
            event_gap_time = np.vstack((event_gap_time, mat[event_gap_name[i]]))

    for i in range(number_of_ch):
        if i == 0:
            event_gap = np.zeros(int(event_gap_time[i]*samplerate))
        else:
            event_gap = np.vstack((event_gap, np.zeros(int(event_gap_time[i]*samplerate))))
    
    # low pass filter
    filt_all = lowpass(data_all, samplerate, fp, fs, filt_type, number_of_ch, event_gap)
    
    # event data
    event = (mat[event_name])

    # slice data for each event
    N_event = event.size

    each_event_response = np.zeros([number_of_ch, N_event, int((-before_event+after_event)*samplerate)+2])

    for i, x in enumerate(event):
        first = int((x*samplerate) + (before_event*samplerate)) # wrap with samplerate, value is change (rounding involved?)
        last = int((x*samplerate) + (after_event*samplerate))
        for k in range(number_of_ch):
            j = 0
            while 1:
                each_event_response[k, i, j] = filt_all[k, first+j]
                j += 1
                if first+j > last:
                    break
    t_ave = np.arange(before_event, after_event, 1.0/samplerate)
    t_ave = np.append(t_ave, after_event)

    # wave data of each ch
    mean = np.mean(each_event_response, axis=1)
    lfp_wave = pd.DataFrame(mean)
    lfp_wave = lfp_wave.T
    lfp_wave = lfp_wave*1000 # mV to µV

    # convert to csv
    start_char = '\\'
    end_char = '.mat'
    csv_name = extract_between_chars(file_path, start_char, end_char) # extract file name from path name
    print(csv_name)
    if all_data == True:
        all_wave = pd.DataFrame(filt_all)
        all_wave.to_csv(f'./Data/all_{csv_name}.csv', sep = ',', header = True, index = False)
    lfp_wave.to_csv(f'./Data/{csv_name}.csv', sep = ',', header = True, index = False)
    
