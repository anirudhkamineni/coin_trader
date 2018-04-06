# coin_trader
Crypto intraday scalp trading, based on 5min data

Scraper used : https://github.com/jchianelli7/crytoscraper .
This scraper parses the website https://coinmarketcap.com/all/views/all/ the stores the price and volume data inside the folder data/


data/ folder description:
  coin_cum.csv: The 3.5 day prices data of the top 300 cryptocurrencies
  vol_cum.csv : The 3.5 day volume data of the top 300 cryptocurrencies


python files description:
  analysis.py: Read the data from coin_cum.csv which contains 3.5 days price data of the top 300 coins scraped from coinmarketcap, and forms a dictionary

  analysis_vol.py: Read the data form vol_cum.csv which contains 3.5 days volume data of the top 300 coins scraped from coinmarketcap, and forms a dictionary

  decision.py: Technical analysis based on the data extracted from above files


Output: 
  Graph indicating the occurence of DOJI pattern in the time series, 
  Sudden increase in prices: notifications about the coins which show the highest increase in value in the recent (past 20 mins) time.
      NOW GROWING: Coins growing at a moderate rate, could be a chance to invest
      HOT LIST: Coins growing at a big rate, could be a chance to invest if caught early
      CONSTANTLY INCREASING IN THE PAST HOUR: Coins with significantly more increase than decrease in the previous hour
