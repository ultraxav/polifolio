# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Data Ingestion
#
# This notebook downloads the top 250 token from CoinGecko https://www.coingecko.com/, matches that data with the list of tradeable tokens on Binance https://www.binance.com/.
#
# Finally downloads the OHLC historical from those tokens

# %% [markdown]
# ## libs

# %%
from binance import Client
from pycoingecko import CoinGeckoAPI
from tqdm import tqdm

import pandas as pd
import time
import yaml

creds_dir = '../creds/'
data_dir = '../data/01_raw/'

# %% [markdown]
# ## import configs

# %%
config = yaml.safe_load(open(creds_dir + 'config.yml'))


# %% [markdown]
# ## support func

# %%
def get_hist_prices(symbol):
    df = cg.get_coin_market_chart_by_id(symbol, 'usd', 'max')
    df = pd.DataFrame(df['prices'])
    df.columns = ['time', symbol]
    df.set_index('time', inplace=True)
    df = df[:-1]
    return df


# %% [markdown]
# ## Binance

# %% [markdown]
# ### init API

# %%
client = Client(config['bnc_api_key'], config['bnc_api_secret'])

# %% [markdown]
# ## download symbols

# %%
symbols = {
    symbol['symbol']: symbol
    for symbol in client.get_exchange_info()['symbols']
    if symbol['isSpotTradingAllowed']
}

for ticker in client.get_ticker():
    if ticker['symbol'] in symbols:
        symbols[ticker['symbol']]['quoteVolume'] = ticker['quoteVolume']

# %%
all_tokens = pd.DataFrame(symbols).transpose()
all_tokens = all_tokens[all_tokens['status'] == 'TRADING']
all_tokens

# %%
unique_tokens = all_tokens['baseAsset'].unique()
unique_tokens

# %% [markdown]
# ## Coingecko

# %% [markdown]
# ### init API

# %%
cg = CoinGeckoAPI()

# %% [markdown]
# ### download top250 tokens

# %%
coin_list = pd.DataFrame(cg.get_coins_markets(vs_currency='usd', per_page=250))
coin_list = coin_list[['id', 'symbol']]
coin_list['symbol'] = coin_list['symbol'].str.upper()
coin_list

# %% [markdown]
# ### filter tokens

# %%
coin_list = coin_list[coin_list['symbol'].isin(unique_tokens)]
coin_list

# %% [markdown]
# ## Download data

# %%
price_data = None
i = 1

for symbol in tqdm(coin_list['id']):
    if i == 1:
        price_data = get_hist_prices(symbol=symbol)
    else:
        price_data = price_data.join(get_hist_prices(symbol=symbol))
    i += 1
    time.sleep(1.5)

# %%
price_info = pd.DataFrame(price_data.notnull().sum()).reset_index()
price_info.columns = ['id', 'available_days']
price_info = coin_list.merge(price_info)
price_info.to_csv(data_dir + 'coin_list.csv', index=False)
price_info

# %%
price_data.to_csv(data_dir + 'price_data.csv')
