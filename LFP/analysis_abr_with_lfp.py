# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 13:57:41 2020

@author: masaaki sakagami
purpose: plot lfp data and abr data to analysis conparative
guide:
    1.jsonファイルを用いたlfp波形の取得する
    2.abr_with_some_moduleのプログラムを用いて各刺激における計測データを取得する
    3.(1,2)のグラフを作成し、対応するabrとlfpの描画
    4.描画した波形を.png形式で保存
    5.
    
"""
# In[1]:


import json
import os
import glob
# In[7]
import glia
import numpy as np
import pandas 
import matplotlib.pyplot as plt
import tath
import piag
import OpenEphys
import scipy
from scipy import stats
from scipy import signal
import cosnail
# In[13]:


print(os.getcwd())


# In[14]:

if not(os.path.exists("./waveform")):
    os.mkdir("./waveform")


# In[2]:
#jsonによるmatchingファイルの作成
dir_path="./plx"
files=os.listdir(dir_path)
dir_names= [f for f in files if os.path.isdir(os.path.join(dir_path, f))]

result_path="./json"
files=os.listdir(result_path)
result_names= [f for f in files if "result" in f]
#result_names=glob.glob(result_path)
"""
for filenames in result_names:
    for j in range(0,8):
        filenames=filenames.lstrip()
"""
matching=dict(zip(dir_names,result_names))
print(matching)

# In[3]:

#jsonファイルに辞書を成型して出力
#ensure...日本語出力可能
with open('matching.json', 'w') as f:
    json.dump(matching, f, ensure_ascii=False)


# In[31]:


#print(f)



# In[6]
abr_path="./abr"
files=os.listdir(abr_path)
csv_names=[f for f in files if ".csv" in f]

# In[9]
filelist = list(tath.selectively('.+\\.csv',tath.listup("C:/Users/student/programming/2020_03_23_USStim/abr")))
datas={}
#csvファイルに記載されたデータをwaveform型のデータとして取得
for filename in filelist:
    datas[tath.Path(filename).body]=cosnail.read_abrcsv(filename,add_dict_key_ID=False)
#各csvファイル内に存在する刺激の種類を配列として取得
wave_status={}
stim_label=["c","us","usm"]
for filename in filelist:
    wave_status_key=tath.Path(filename).body
    wave_status[wave_status_key]=[]
    for stim_name in stim_label:
        for i in range(0,100):
            for j in range(0,100):
                 if stim_name+str(i)+"-"+str(j) in filename and i<j:
                    for k in range(i,j+1):
                        wave_status[wave_status_key].append(stim_name+str(k))
                 elif stim_name+str(i)+".csv" in filename:
                    wave_status[wave_status_key].append(stim_name+str(i))
                    break

wave_dict={}
for wave_dictname in wave_status.keys():
    #対応するwave_statusのものとdictを作成        
    data_dict=dict(zip(wave_status[wave_dictname],datas[wave_dictname].values()))
    wave_dict[wave_dictname]=data_dict


# In[11]
#{lfp_file:[json_filename,wave_dict[lfp_file]]}を取得
all_matching={}
all_matching=dict(zip(dir_names,list(zip(result_names,wave_dict.values()))))
# In[6]:


def lowpass(x, samplerate, fp, fs, gpass, gstop):
    fn = samplerate / 2                           #ナイキスト周波数
    wp = fp / fn                                  #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn                                  #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  #オーダーとバターワースの正規化周波数を計算
    b, a = signal.butter(N, Wn, "low")           #フィルタ伝達関数の分子と分母を計算
    y = signal.filtfilt(b, a, x)                  #信号に対してフィルタをかける
    return y

with open("matching.json",encoding = "utf-8") as json_fp:
    rec_stim_matching = json.load(json_fp)
reload = False

os.makedirs("./waveform_with_abr/",exist_ok=True)

for i in rec_stim_matching.keys():
    dir_path="./waveform_with_abr/"+i
    os.makedirs(dir_path,exist_ok=True)
    print("Processing " + i + "\n")
    #    channel_map = [8,7,4,5,2,1,3] #9,11,6,10,13,12,15,16,14
    channel_map = [9,8,10,7,13,4,12,5,15,2,16,1,14,3,11,6]
    time_width = glia.milliseconds(300)
    offset = glia.milliseconds(50)
    duration = glia.milliseconds(400)
    filename = i
    jsonfile = rec_stim_matching[filename]
    filename_name=filename
    filename = "plx/" + filename
    with open("json/"+jsonfile[:14]+"Settings.json",encoding="utf-8") as json_fp:
        stim_setting = json.load(json_fp)
    if not reload and os.path.isfile("./waveform/"+filename[4:-4]+".lfp") and os.path.isfile("./waveform/"+filename[4:-4]+".trig"):
        print("Load lfp, trig")
    else:
        wave = []
        for j in channel_map:
            tmp = OpenEphys.loadContinuous(filename + "/101_CH"+str(j)+".continuous")
            #gliaの形式にそってローパスフィルタをかけた波形の出力
            wave.append(glia.nucleus.Waveform(lowpass(tmp["data"],30000,450,600,10,30),rate=glia.Frequency(30000)))
            timestamp = tmp["timestamps"][0]
    events = OpenEphys.loadEvents(filename+"/all_channels.events")
    e_tmp = (events["timestamps"] - timestamp)[0::2]
    trigger = []
    for i in (e_tmp/30):
        trigger.append(glia.millisecond(i))
    trigger = np.array(trigger)
    glia.save("./waveform/"+filename[4:]+".lfp",wave)
    glia.save("./waveform/"+filename[4:]+".trig",trigger)
    if not reload and os.path.isfile("./waveform/"+filename[4:-4]+".stimorder"):
        print("Load stimorder")
    else:
        with open("json/"+jsonfile,encoding="utf-8") as json_fp:
            stim_pattern = json.load(json_fp)
    #pandas配列に刺激パターンを格納
    table = pandas.DataFrame(stim_pattern)
    glia.save("./waveform/"+filename[4:]+".stimorder",table)
    result = {}
    if not reload and os.path.isfile("./waveform/"+filename[4:-4]+".lfps"):
        print("Load lfps")
    else:
        if stim_setting["Mode"] == 'ABR Mode(TDT)':
            print("Mode TDT")
            for i in range(len(table["name"].values)):
                timing = trigger[(i*350+i*2):(i*350+i*2+350)]
                ret = [glia.average(glia.base(glia.extract(x, timing - offset, duration), offset*0.5), axis=1) for x in wave]
                result[table["name"].values[i]] = ret
        else:
            for key, blob in table.groupby("name"):
                timing = trigger[blob.index]
                ret = [glia.average(glia.base(glia.extract(x, timing - offset, duration), offset*0.5), axis=1) for x in wave]
                result[key] = ret
        glia.save("./waveform/"+filename[4:]+".lfps",result)
            
    with open("waveform/"+filename[4:]+".lfps") as lfp_1:
        lfp_data = lfp_1
    reload = False
        
    lfp_data = glia.load("waveform/"+filename[4:]+".lfps")
    depth = 45
    
    wave_status=["p10","p11","p12","p13"]
    for num in range(14):
        click_adi_status="c"+str(num)
        wave_status.append(click_adi_status)
    for num in range(54):
        usm_adi_status="usm"+str(num)
        wave_status.append(usm_adi_status)
    for num in range(4):
        us_adi_status="us"+str(num)
        wave_status.append(us_adi_status)
    for stim_wave in wave_status:
        #網羅的に刺激波形があるか探索・該当刺激があるときに波形描画
        if stim_wave in lfp_data.keys():
            fig = plt.figure(figsize=(16,9),dpi=64)
            if stim_wave in all_matching[filename_name][1]:
                #lfp波形描画
                ax1 = fig.add_subplot(121)
                lfp_sampling_rate=30000
                lfp_timespan=1000
                for i, x in enumerate(lfp_data[stim_wave]):
                    ax1.plot(-x + i*depth)    
                plt.title(filename[4:]+"-"+stim_wave)
                ax1.set_ylim(800,-100)
                ax1_xticks=[xl*50*30 for xl in range(len(11))]
                ax1.set_xticks(ax1_xticks)
                ax1.set_xticklabels((ax1_xticks/30)-50)
                #abr波形描画
          
                ax2=fig.add_subplot(122)
                sampling_rate=25000
                timespan=1000
                abr_x=[xl/(sampling_rate/timespan) for xl in range(len(all_matching[filename_name][1][stim_wave]))]
                abr_y=all_matching[filename_name][1][stim_wave]
                ax2.plot(abr_x,abr_y)
                ax2.set_xlim(0,20)
                ax2.set_ylim(-1500,1500)
            else:
                ax=fig.add_subplot(111)
                for i, x in enumerate(lfp_data[stim_wave]):
                    ax.plot(-x + i*depth)    
                plt.title(filename[4:]+"-"+stim_wave)
                ax.set_ylim(800,-100)
                ax.set_ylabel("depth[um]")
            fig.savefig(os.path.join(dir_path,filename[4:]+"-"+stim_wave+".png"))
            plt.close()
    """        
        for num in range(len(wave_status)):
            if wave_status[num] in lfp_data.keys():
                for i, x in enumerate(lfp_data[wave_status[num]]):
                    ax1.plot(x - i*depth)
                fig.savefig("./waveform/"+filename[4:]+".png")
    """
