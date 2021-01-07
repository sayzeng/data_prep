# -*- coding: utf-8 -*-
"""
Created on Sat May 26 09:59:03 2018
@author: Sarah Zeng

Browse/prep US motor fuel tax rate data from 2000-2018 (by state, by year)
Source: Compiled by FTA from various sources

Notes:
    INCOMPLETE (stopped after 2002)
    Years 2009 and 2012 are missing
"""

import pandas as pd

# Import ExcelFile
filename = 'raw\\gas_rates_2000-2018.xls'
xl = pd.ExcelFile(filename)
sheets = xl.sheet_names

# Browse relative sizes of each chart
d = {}
print('Year', '(rows, columns)')
for s in sheets:
    d[s] = xl.parse(s)
    print(s, d[s].shape)

#%%
# Housekeeping
key_colnames = {'state':'State',
                'year':'Year',
                'gas_ex':'Gasoline excise tax',
                'gas_ad':'Gasoline additional tax',
                'gas_tot':'Gasoline total tax',
                'ds_ex':'Diesel excise tax',
                'ds_ad':'Diesel additional tax',
                'ds_tot':'Diesel total tax',
                'gsh_ex':'Gasohole excise tax',
                'gsh_ad':'Gasohole additional tax',
                'gsh_tot':'Gasohole total tax',
                'notes':'Notes'}
colnames = list(key_colnames.keys()) #12 columns
mfrates = pd.DataFrame(columns=colnames)
footnote = {}

def append_subchart(year, subchart, chart):
    rates['year'] = int(year)
    chart = chart.append(subchart)

#%%
### YEAR 2000 ###

year = '2000'
df = d[year]

# Housecleaning
df.columns = ['state', 'gas_tot', 'gas_ex', 'gas_ad', 'notes']
rates = df[4:56]
footnote[year] = df[58:].dropna(axis=1, how='all')

# Clean state names
states = rates.state
states = states.str.rsplit(pat='[', n=1, expand=True)
states.columns = ['state', 'note']
states.note = states.note.apply(lambda x: x if x is None else '[' + x)
states.state = states.state.str.strip()
# Replace state column with split/cleaned version
rates = rates.drop(columns = ['state'])
rates = pd.concat([states.state, rates], axis=1)
rates.notes = rates.notes.fillna('') + states.note.fillna('')

# Append annual rates to main df
rates['year'] = int(year)
mfrates = mfrates.append(rates).reset_index(drop=True)

#%%
### YEAR 2001: only has total tax rates with two state columns ###

year = '2001'
df = d[year]

# Housecleaning (stacking columns)
df.columns = ['state', 'gas_tot', 'rank', 'state', 'gas_tot', 'rank']
rates = df[3:29]
rates1 = rates.iloc[:, :3]
rates2 = rates.iloc[:, 3:]
rates = rates1.append(rates2).dropna(how='all').reset_index(drop=True)
rates = rates.drop('rank', axis=1)
footnote[year] = df[29:].dropna(how='all', axis=1)

append_subchart(year, rates, mfrates)

#%%
### YEAR 2002: similar to 2001 ###

year = '2002'
df = d[year]

# Housecleaning (stacking columns)
df.columns = ['state', 'gas_tot', 'rank', 'state', 'gas_tot', 'rank']
rates = df[3:29]
rates1 = rates.iloc[:, :3]
rates2 = rates.iloc[:, 3:]
rates = rates1.append(rates2).dropna(how='all').reset_index(drop=True)
rates = rates.drop('rank', axis=1)
footnote[year] = df[31:].dropna(how='all', axis=1)

append_subchart(year, rates, mfrates)


# Years 2003-2011

# Years 2013-2015

# Years 2016-2018
