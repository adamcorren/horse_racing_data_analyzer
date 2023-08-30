import pandas as pd
from . import calculations

# get percentage change of bookmaker prices between key time prices
def get_morning_book_price_changes(df):
    times_compare = [['1', '6'], ['1', '10'], ['6', '10']]
    for t in times_compare:
        df = df.pipe(calculations.calculate_pct_change_time,  f'{t[0]}_mean_book_NR',
            f'{t[1]}_mean_book_NR', 'change_book_NR', str(t[0]+'_'+t[1])) 
    return df


# rank changes in bookmaker prices between key times, negative percentage changes better as price has decreased
def get_morning_book_price_change_ranks(df):
    times_compare = ['1_6', '1_10', '6_10']
    for t in times_compare:
        df = df.pipe(calculations.rank_by_race_ascending_time,  'change_book_NR_rank', 'time', 
            f'change_book_NR_{t}', t)
    return df

# get percentage change of price between key time bookmaker prices and starting prices
def get_morning_book_starting_price_changes(df):
    times_compare = [['1', 'isp'], ['1', 'BSP'],['6', 'isp'], ['6', 'BSP'], ['10', 'isp'], ['10', 'BSP']]
    for t in times_compare:
        df = df.pipe(calculations.calculate_pct_change_time,  f'{t[0]}_mean_book_NR', t[1],
            'change_book_NR', str(t[0]+'_'+t[1])) 
    return df

# rank changes in price between key times bookmaker prices and starting prices
def get_morning_book_starting_price_change_ranks(df):
    times_compare = ['1_isp', '1_BSP', '6_isp', '6_BSP', '10_isp', '10_BSP']
    for t in times_compare:
        df = df.pipe(calculations.rank_by_race_ascending_time,  'change_book_NR_rank', 'time',
            f'change_book_NR_{t}', t)
    return df

# same process for exchange prices instead of bookmaker prices
def get_morning_ex_price_changes(df):
    times_compare = [['1', '6'], ['1', '10'], ['6', '10']]
    for t in times_compare:
        df = df.pipe(calculations.calculate_pct_change_time,  f'{t[0]}_ex_NR',
            f'{t[1]}_ex_NR', 'change_ex_NR', str(t[0]+'_'+t[1])) 
    return df


def get_morning_ex_price_change_ranks(df):
    times_compare = ['1_6', '1_10', '6_10']
    for t in times_compare:
        df = df.pipe(calculations.rank_by_race_ascending_time,  'change_ex_NR_rank', 'time', 
            f'change_ex_NR_{t}', t)
    return df


def get_morning_ex_starting_price_changes(df):
    times_compare = [['1', 'isp'], ['1', 'BSP'],['6', 'isp'], ['6', 'BSP'], ['10', 'isp'], ['10', 'BSP']]
    for t in times_compare:
        df = df.pipe(calculations.calculate_pct_change_time,  f'{t[0]}_ex_NR', t[1],
            'change_ex_NR', str(t[0]+'_'+t[1])) 
    return df


def get_morning_ex_starting_price_change_ranks(df):
    times_compare = ['1_isp', '1_BSP', '6_isp', '6_BSP', '10_isp', '10_BSP']
    for t in times_compare:
        df = df.pipe(calculations.rank_by_race_ascending_time,  'change_ex_NR_rank', 'time',
            f'change_ex_NR_{t}', t)
    return df

# get difference between bookmaker and exchange
def get_book_exchange_differences(df):
    times_compare = ['1', '6', '10']
    for t in times_compare:
        df = df.pipe(calculations.calculate_pct_change,  f'{t}_ex_NR', f'{t}_mean_book_NR'
            , f'{t}_diff_book_ex',) 
    return df

# compare isp and bsp
def compare_starting_prices(df):
    df = df.pipe(calculations.calculate_pct_change,  'isp', 'BSP', 'isp_bsp_change')
    return df

# check if horse is favourite at least in one time logged
def check_if_fave_any(df):
    return (df
            .assign(any_fave=1)
            .assign(any_fave=lambda df : df.any_fave.where(
                df.loc[:, ['fave_1', 'fave_6', 'fave_10', 'fave_isp', 'fave_BSP']].max(axis=1) == 1 , 0)))


# is horse favourite at every time logged
def all_fave(df):
    return (df
        .assign(all_fave=1)
        .assign(all_fave=lambda df : df.all_fave.where(
            df.loc[:, ['fave_1', 'fave_6', 'fave_10', 'fave_isp', 'fave_BSP']].sum(axis=1) == 5 , 0)))


# main function
def compare_prices(df):
    print('Comparing prices completed...')
    return (get_morning_book_price_changes(df)
        .pipe(get_morning_book_price_change_ranks)
        .pipe(get_morning_book_starting_price_changes)
        .pipe(get_morning_book_starting_price_change_ranks)
        .pipe(get_morning_ex_price_changes)
        .pipe(get_morning_ex_price_change_ranks)
        .pipe(get_morning_ex_starting_price_changes)
        .pipe(get_morning_ex_starting_price_change_ranks)
        .pipe(get_book_exchange_differences)
        .pipe(compare_starting_prices)
        .pipe(check_if_fave_any)
        .pipe(all_fave))