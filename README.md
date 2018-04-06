# coin_trader
Crypto intraday scalp trading, based on 5min data

Scraper used : https://github.com/jchianelli7/crytoscraper
Creates the files inside data/

The code I have written is divided into 5 files:
analysis.py: Read the data from coin_cum.csv which contains 3.5 days price data of the top 300 coins scraped from coinmarketcap, and forms a dictionary

analysis_vol.py: Read the data form vol_cum.csv which contains 3.5 days volume data of the top 300 coins scraped from coinmarketcap, and forms a dictionary

decision.py: Technical analysis based on the data extracted from above files


Sample Output: DOJI pattern identification in real-time data, 
               Sudden increase in price patterns: which notifies me about the coins which are showing the highest increase in value in the recent (past 20 mins) time.

NOW GROWING: Coins growing at a moderate rate, could be a chance to invest
HOT LIST: Coins growing at a big rate, could be a chance to invest if caught early
CONSTANTLY INCREASING IN THE PAST HOUR: Coins with significantly more increase than decrease in the previous hour
