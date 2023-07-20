import pandas as pd

# calculate percentage change between two columns
def calculate_pct_change(data, numerator_col, denominator_col, col_name):
    return data.assign(**{col_name: lambda x: x[[numerator_col, denominator_col]].pct_change(axis=1)[denominator_col]})


# calculate percentage change between two columns and change column name based on time argument 
def calculate_pct_change_time(data, numerator_col, denominator_col, col_name, time):
    return (data
        .assign(**{col_name: lambda x: x[[numerator_col, denominator_col]].pct_change(axis=1)[denominator_col]})
        .rename(columns={col_name: f'{col_name}_{time}'}))


# rank metric comapred to other runners in race
def rank_by_race_ascending(data, col_name, group, metric):
    return data.assign(**{col_name: lambda x: x.groupby([group])[metric].rank(ascending=True, method='min')})


# get mean value in group
def mean_value(data, col_name, group, metric):
    return data.assign(**{col_name: lambda x: x.groupby([group])[metric].transform('mean')})


# rank metric comapred to other runners in race and change column name based on time argument 
def rank_by_race_ascending_time(data, col_name, group, metric, time):
    return (data
        .assign(**{col_name: lambda x: x.groupby([group])[metric].rank(ascending=True, method='min')})
        .rename(columns={col_name: f'{col_name}_{time}'}))


# rank metric comapred to other runners in race descending
def rank_by_race_descending(data, col_name, group, metric):
    return data.assign(**{col_name: lambda x: x.groupby([group])[metric].rank(ascending=False, method='min')})


# rank metric comapred to other runners in race descending and change column name based on time argument 
def rank_by_race_descending_time(data, col_name, group, metric, time):
    return (data
        .assign(**{col_name: lambda x: x.groupby([group])[metric].rank(ascending=False, method='min')})
        .rename(columns={col_name: f'{col_name}_{time}'}))


# get favourite based on current price
def get_favourite(data, col_name, metric, time):
    return (data
            .assign(**{col_name:0})
            .assign(**{col_name:lambda x : x[col_name].where(x[metric] != 1, 1)})
            .rename(columns={col_name: f'{col_name}_{time}'}))

