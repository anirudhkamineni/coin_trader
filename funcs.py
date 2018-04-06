import csv
import os
import json
from functools import reduce
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance as fin
import talib as ta


def read_files_into_dicts():
    cuml_prices_file = open("./data/coin_cum.csv","r")
    vol_file = open("./data/vol_cum.csv","r")
    cum_price_dict = {}
    vol_dict = {}
    coin_index = {}

    #Read prices from CSV into dictionary
    read_csv1 = csv.reader(cuml_prices_file)
    prices_cuml = [rows for rows in read_csv1]
    read_csv2 = csv.reader(vol_file)
    vol_cuml = [rows for rows in read_csv2]

    if prices_cuml[0][0] == "Symbol":
        del prices_cuml[0]
    if vol_cuml[0][0] == "Symbol":
        del vol_cuml[0]
    
    for currency in prices_cuml:
        cum_price_dict[currency[0]]=list(map(float,currency[1:]))
    for currency in vol_cuml:
        vol_dict[currency[0]]=list(map(float,currency[1:]))

    return cum_price_dict,vol_dict

    
#Calculate the changes dictionary for the top 100 values
def calculate_diff(cum_price_dict,vol_dict): 
    changes4h_vol_dict = {}
    changes1h_vol_dict = {}
    #changes1h_relative_price_dict = {}
    #changes4h_relative_price_dict = {}
    changes4h_price_dict = {}
    changes1h_price_dict = {}
    for currency in reduce(lambda x, y: set(x.keys()).union(y.keys()), [cum_price_dict,vol_dict]):
        #EDIT: gotta change this to differences between Moving average list. Moving average list over 5 values, might iron out the volatility.
            #put if checks for keys in dicts
        list4h = cum_price_dict[currency][-40:]
        list1h = cum_price_dict[currency][-12:]
        if currency in cum_price_dict and all(list4h):
            changes4h_price_dict[currency] = [(list4h[n]-list4h[n-1])*100/list4h[n-1] for n in range(1,len(list4h))] 
            changes1h_price_dict[currency] = [(list1h[n]-list1h[n-1])*100/list1h[n-1] for n in range(1,len(list1h))]
            #changes1h_relative_price_dict[currency] = [(list1h[n]-list1h[0])*100/list1h[0] for n in range(1,len(list1h))]
            #changes4h_relative_price_dict[currency] = [(list4h[n]-list4h[0])*100/list4h[0] for n in range(1,len(list4h))]
            
        list4h = vol_dict[currency][-50:]
        list1h = vol_dict[currency][-12:]
        if currency in vol_dict and all(list4h):
            changes4h_vol_dict[currency] = [(list4h[n]-list4h[n-1])*100/list4h[n-1] for n in range(1,len(list4h))] 
            changes1h_vol_dict[currency] = [(list1h[n]-list1h[n-1])*100/list1h[n-1] for n in range(1,len(list1h))]

    #return all the stuff
    return changes4h_price_dict, changes1h_price_dict, changes4h_vol_dict, changes1h_vol_dict


#Add a check for popular coins being within 20% of thier lowest price in 5days, they will definitely raise
def fall_of_a_prince(cum_price_dict, vol_dict):
    prince_list = []
    fall_file_pointer = open('./data/coinlist.csv')
    for columns in (raw.replace("\"","").split(",") for raw in fall_file_pointer):  
         prince_list.append(columns[0])
    prince_list = prince_list[1:]
    prince_list = prince_list[:200]
    
    for currency in prince_list:
        if (cum_price_dict[currency][-1] > 1.2 *min(cum_price_dict[currency]) or min(cum_price_dict[currency]) == 0):
              prince_list.remove(currency)
    
    return(prince_list)

def fit_lines_to_data(cum_price_dict):
    return 

def constant_growth(changes1h_price_dict, vol_dict):
    constant_growth_list = []
    great_growth_list = []
    if not os.path.exists("./data/growth_coins.txt"):
        os.mknod("./data/growth_coins.txt")
    growth_file = open("./data/growth_coins.txt","r")
    prev_growth_list = growth_file.read().splitlines()
    growth_file.close() 

    for currency in changes1h_price_dict:
        if(len(changes1h_price_dict[currency]) == 11):
            if (   (sorted(changes1h_price_dict[currency][-6:])[1] > 0.05 and min(changes1h_price_dict[currency][-6:]) > -0.2 and vol_dict[currency][-1] > 1000000)
                or (sorted(changes1h_price_dict[currency][-7:-1])[1] > 0.05 and min(changes1h_price_dict[currency][-7:-1]) > -0.2 and vol_dict[currency][-1] > 1000000)
                or (sorted(changes1h_price_dict[currency][-8:-2])[5] > 0.5 and sorted(changes1h_price_dict[currency][-8:-2])[1] > 0.1 and min(changes1h_price_dict[currency][-8:-2]) > -0.2 and vol_dict[currency][-1] > 1000000)):
#                or (sorted(changes1h_price_dict[currency][-9:-3])[1] > 0.2 and min(changes1h_price_dict[currency][-9:-3]) > -0.2)
#                or (sorted(changes1h_price_dict[currency][-10:-4])[1] > 0.2 and min(changes1h_price_dict[currency][-10:-4]) > -0.2)
#               or (sorted(changes1h_price_dict[currency][-11:-5])[1] > 0.2 and min(changes1h_price_dict[currency][-11:-5]) > -0.2)):

                constant_growth_list.append(currency)
                if (sorted(changes1h_price_dict[currency][-6:])[2] > 0.2 and min(changes1h_price_dict[currency][-6:]) > 0 and vol_dict[currency][-1] > 1000000 and (currency in constant_growth_list)):
                    constant_growth_list.remove(currency)
                    great_growth_list.append(currency)
    if (set(prev_growth_list) != set(constant_growth_list)):
        growth_filew = open("./data/growth_coins.txt","w")
        growth_filew.write('\n'.join(constant_growth_list))
        growth_filew.close()
    return constant_growth_list, great_growth_list




def fit_line_1h_data(changes1h_price_dict, changes4h_price_dict, vol_dict):
    fit_growth_dict = {}
    if not os.path.exists("./data/fit_coins.txt"):
        os.mknod("./data/fit_coins.txt")
    growth_file = open("./data/fit_coins.txt","r")
    if os.stat("./data/fit_coins.txt").st_size == 0:
        prevfit_growth_dict = {}
    else:
        prevfit_growth_dict = json.loads(growth_file.read()) 
    growth_file.close() 

    for currency in changes1h_price_dict:
        if(len(changes1h_price_dict[currency]) == 11):
            count = 0
            if(sum(changes1h_price_dict[currency])/11 > 0.1 and vol_dict[currency][-1] > 10000000 ):
                for i in range(28):
                    if (sum(changes4h_price_dict[currency][i:i+11])/11 > 0.1):
                        count = count + 1    
                fit_growth_dict[currency]=count

    if (bool(prevfit_growth_dict) and set(prev_growth_dict.keys()) != set(fit_growth_dict.keys())):
        growth_filew = open("./data/fit_coins.txt","w")
        growth_filew.write(dumps.dumps(fit_growth_dict))
        growth_filew.close()
    return fit_growth_dict
    

def plot_vol_and_price_graph(cum_price_dict, vol_dict):
    idx = range(1000)
    data = pd.DataFrame(data = {'price':cum_price_dict["ETH"],'volume':vol_dict["ETH"]}, index=idx)
    fig , ax = plt.subplots(nrows=2, sharex=True, figsize=(15,8))
    ewm = pd.DataFrame.ewm(data.price,span=12)
    ax[0].plot(data.index, ewm.mean())
    ax[0].plot(data.index,pd.rolling_mean(data.price,7),'g-')
    ax[1].plot(data.index, data.volume)
    plt.show()
    
def plot_macd_graph(cum_price_dict):
    data_frame = pd.DataFrame(cum_price_dict["ETH"])
    
    ewma_data = pd.DataFrame.ewm(data_frame,span=35)
    #print(len(ewma_data))
    ax = data_frame.plot(style='w')
    ewma_data.mean().plot(style='k--', ax=ax)
#    (ewma_data.mean()+2*ewma_data.std()).plot(style='g--',ax=ax)
#    (ewma_data.mean()-2*ewma_data.std()).plot(style='g--',ax=ax)
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()
    
def ochl_analysis(cum_price_dict):
    data_frame = pd.DataFrame(cum_price_dict["VEN"])
    data_frame.index = pd.to_datetime(data_frame.index, unit='s')    
    ewma_data = pd.DataFrame.ewm(data_frame,span=12)
    ewm_frame = ewma_data.mean()
    ewm_frame.index = pd.to_datetime(ewm_frame.index, unit='s')
    cd_data = data_frame.resample('6S').ohlc()  
    #mom_frame = momentum_analysis(cd_data,data_frame,ewm_frame) 
    candle_analysis(cd_data,data_frame)


def candle_analysis(cd_data,data_frame):
    #print(cd_data)
    #print(cd_data[0][-5:])
    a = (ta.CDL3BLACKCROWS(cd_data[0].open,cd_data[0].high,cd_data[0].low,cd_data[0].close))
    print(a[a != 0.0].index)
    fig, ax = plt.subplots()
    fin.candlestick2_ochl(ax, cd_data[0].open,cd_data[0].close,cd_data[0].high,cd_data[0].low,colorup='g',colordown='r')
    #plt.plot(np.linspace(1,1000/6,1000),ewm_frame)
    #plt.plot(data_frame)
    #plt.scatter(a[a != 0].index,data_frame[0][a[a != 0].index],marker='o',c='r')
    plt.show()
    #end

def momentum_analysis(cd_data,data_frame,ewm_frame):
    a = ta.TEMA(cd_data[0].close,timeperiod=6)
    #print(a)
    #fig, ax = plt.subplots()
    #ax.plot(data_frame)
    #ax1 = ax.twinx()
    #ax1.plot(a,color='r')
    #plt.show()
    return a


    