import csv
import os
import json
from functools import reduce
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance as fin
from funcs import *

#read the data from files into the dicts
cum_price_dict,vol_dict = read_files_into_dicts()

#call calculate_diff
changes4h_price_dict, changes1h_price_dict, changes4h_vol_dict, changes1h_vol_dict = calculate_diff(cum_price_dict, vol_dict);
    #print(changes1h_price_dict["WABI"])

#Calculate the 5point fit slopes for the above changes dicts
fit_lines_to_data(cum_price_dict);

#Weight based on the 5point slopes of changes1h dict

#Weight based on the slope of line fit for 2h data
fit_line_1h_dict = fit_line_1h_data(changes1h_price_dict, changes4h_price_dict, vol_dict); 
print("\nCONSTANTLY INCREASING IN THE PAST HOUR:")
print(fit_line_1h_dict)

#Coins which have constantly grown by 1% over the last half an hour
constant_growth_list , great_growth_list= constant_growth(changes1h_price_dict,vol_dict)
print("\nNOW GROWING:")
print(constant_growth_list)
print("\nHOT LIST:")
print(great_growth_list)

#call fall_of_a_prince
prince_list = fall_of_a_prince(cum_price_dict, vol_dict);
    #print("\nFALL OF A PRINCE:")
    #print(prince_list)

#plot_vol_and_price_graph(cum_price_dict, vol_dict);
#plot_macd_graph(cum_price_dict)

#Candlestick analysis
ochl_analysis(cum_price_dict)


#Identify a crash; if 80% of the top 50 coins are on the down trend for a period, then it is a crash, Might not be necessary as I am planning to day trade

#Add a check for more than 10% sudden increase in volume, and check the next 2,3 consecutive changes in volume. Will be hard to buy as soon as the vol increases. But there is still hope.. On the other hand, if this happens to the coin you hold, time to sell and buy it after it falls.
#function owned_raise()

#function check_raise()
