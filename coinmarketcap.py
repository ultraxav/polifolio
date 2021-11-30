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
# # CoinMarketCap Data Scrapper

# %% [markdown]
# ## libs

# %%
import pandas as pd
import yaml

from coinsta.core import Current

pd.options.display.max_columns = None

# %% [markdown]
# ## import configs

# %%
config = yaml.load(open('config.yml'), Loader=yaml.FullLoader)

# %% [markdown]
# ## initialize API

# %%
cur = Current(api_key=config['cmc_api_key'])

# %% [markdown]
# ## get current market information on a specified crypto

# %%
btc_current = cur.get_current('btc')

# %%
btc_current

# %% [markdown]
# ## get global overview of crypto markets

# %%
glo_info = cur.global_info()

# %%
glo_info

# %% [markdown]
# ## get the top 1000 cryptos (in terms of market cap)

# %%
current_1000 = cur.top_100(
    limit=1000
)  # Default limit is 100 but can be increased as a user wishes

# %%
current_1000

# %%
current_1000.to_csv('coinmarketcap1000.csv', index=False)
