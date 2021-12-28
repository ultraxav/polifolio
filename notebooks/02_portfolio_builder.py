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
# # Portfolio Builder
#
# This notebook simulates portfolios with historical data from tokens

# %% [markdown]
# ## libs

# %%
from plotly.subplots import make_subplots
from tqdm import tqdm

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

pd.options.display.max_columns = None

data_dir = '../data/01_raw/'

# %% [markdown]
# ## load and filter coin_list

# %%
coin_list = pd.read_csv(data_dir + 'coin_list.csv')
coin_list

# %%
selected_tokens = coin_list[
    (coin_list['available_days'] > 400) & ~coin_list['symbol'].str.contains('USD')
]
selected_tokens

# %% [markdown]
# ## load and filter price_data

# %%
price_data = pd.read_csv(data_dir + 'price_data.csv')
price_data['time'] = price_data['time'] * 1000000
price_data['time'] = pd.to_datetime(price_data['time'])
price_data = price_data.set_index('time')
price_data

# %%
price_data = price_data[selected_tokens['id']]
price_data.dropna(inplace=True)
price_data

# %% [markdown]
# ## daily returns

# %%
daily_returns = price_data.pct_change().dropna()
daily_returns

# %% [markdown]
# ## correlation matrix

# %%
corr_matrix = daily_returns.corr()
corr_matrix.style.background_gradient(cmap='coolwarm')

# %% [markdown]
# ## annualized returns

# %%
ind_er = price_data.resample('Y').last().pct_change().mean()
round(ind_er * 100, 2)

# %% [markdown]
# ## annualized variance

# %%
ann_sd = price_data.pct_change().std().apply(lambda x: x * np.sqrt(365))
round(ann_sd * 100, 2)

# %% [markdown]
# ## annualized sharpe ratios

# %%
assets = pd.concat([ind_er, ann_sd], axis=1)
assets.columns = ['Returns', 'Volatility']
assets['Sharpe'] = assets['Returns'] / assets['Volatility']
assets = assets.sort_values(by='Sharpe', ascending=False)
round(assets, 4)

# %%
assets = assets[assets['Sharpe'] > 1]
assets = assets[assets['Volatility'] < 2.31]
assets
