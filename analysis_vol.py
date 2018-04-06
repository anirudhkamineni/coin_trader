import csv

current_prices_file = open("./data/coinlist.csv", "r")
cuml_prices_file = open("./data/vol_cum.csv","r")

read_csv1 = csv.reader(current_prices_file)
prices = [rows for rows in read_csv1]
del prices[0]
read_csv2 = csv.reader(cuml_prices_file)
prices_cuml = [rows for rows in read_csv2]
if prices_cuml[0][0] == "Symbol":
    del prices_cuml[0]

curr_price_dict = {}
cum_price_dict = {}

for currency in prices:
    curr_price_dict[currency[0]]=float(currency[1])        
      
for currency_series in prices_cuml:
    cum_price_dict[currency_series[0]]=list(map(float,currency_series[1:]))

#print(len(cum_price_dict["QLC"]))
for token in curr_price_dict:
    if token in cum_price_dict:
        if(len(cum_price_dict[token]) > 1000):
            del cum_price_dict[token][0]
        cum_price_dict[token].append(curr_price_dict[token])
    else:
        cum_price_dict[token] = [curr_price_dict[token]]

for token1 in cum_price_dict:
    if(len(cum_price_dict[token1]) > 1000):
        del cum_price_dict[token1][0]
    if token1 not in curr_price_dict:
        cum_price_dict[token1].append(0)
#for token2 in list(cum_price_dict):
#    print((cum_price_dict[token2]))
token_list = []
#print(cum_price_dict)
for token2 in list(cum_price_dict):
    if (sum(cum_price_dict[token2]) == 0):
        del cum_price_dict[token2]
    else:
        temp = cum_price_dict[token2]
        temp.insert(0,token2)
        token_list.append(temp)
#print(token_list)
write_csv2 = csv.writer(open("./data/vol_cum.csv", "w")) 
write_csv2.writerows(token_list)
