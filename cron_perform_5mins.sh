#!/bin/bash

cd /nobackup/akaminen/files/coin_prices-master/coinmarketcap-scrapper-master
/router/bin/npm install
/router/bin/npm run start
wait
if [ ! -f ./data/coin_cum.csv ]; then
    cd data
    cut -d, -f2 --complement coinlist.csv > coin_cum.csv
    cd ..
fi
if [ ! -f ./data/vol_cum.csv ]; then
    cd data
    cut -d, -f3 --complement coinlist.csv > vol_cum.csv
    cd ..
fi
python analysis.py
wait
python analysis_vol.py
echo "done analysis";
