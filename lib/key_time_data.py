import datetime
from datetime import timedelta
import pandas as pd
from functools import reduce

# getting the hours prices, if not available uses nearest available time
def get_odds(hourly_odds, time, t2):
    cols = ['time', 'name', 'logged','spr', 'william_hill', 'bet_victor', 'betfair_sportsbook', 
            'paddy_power', '888_sports','sky_bet', 'betfair_exchange']
    price_info = hourly_odds.query(f'logged == "{t2}"').loc[:, cols]

    # try the hour before if data not available
    if len(price_info) == 0:
        price_info = hourly_odds.query(f'logged == "0{time-1}:00"').loc[:, cols]
        # try the hour after if data not available
        if len(price_info) == 0:
            price_info = hourly_odds.query(f'logged == "0{time+1}:00"').loc[:, cols]


    
    # make sure prices are numeric
    columns_to_convert = price_info.columns[3:10]
    price_info[columns_to_convert] = price_info[columns_to_convert].apply(pd.to_numeric, errors='coerce')
    
    # adding columns showing the mean, max, min prices and bookmakers with best and worst prices
    return (price_info
            .assign(max_book=price_info.iloc[:, 3:10].max(axis=1),
                    max_book_name=price_info.iloc[:, 3:10].idxmax(axis=1),
                    min_book=price_info.iloc[:, 3:10].min(axis=1),
                    min_book_name=price_info.iloc[:, 3:10].idxmin(axis=1),
                    mean_book=price_info.iloc[:, 3:10].mean(axis=1),
                    ex=price_info.betfair_exchange))


# getting price deductions based on time price was collected, the time of withdrawal will effect 
# which prices need to be adjusted
def get_deductions(time, price_deductions):
    if time == 1:
        return price_deductions[['time', 'deduction']].groupby('time',as_index=False)['deduction'].sum()
    if time == 6:
        return price_deductions.query('logged > "06:00"')[['time', 'deduction']] \
            .groupby('time',as_index=False)['deduction'].sum()
    if time == 10:
        return price_deductions.query('logged > "10:00"')[['time', 'deduction']] \
            .groupby('time',as_index=False)['deduction'].sum()
               

# adjusting prices with the correct price adjustments
def adjust_prices(odds, deductions, time):
    price_final = pd.merge(odds, deductions, on='time', how='left')
    return (price_final
            .assign(deduction=price_final.deduction .where(price_final.deduction.notna(), 0))
            # adjust prices
            .assign(max_book_NR=lambda x:(((x.max_book-1)*( 1-x.deduction))+1),
                    min_book_NR=lambda x:(((x.min_book-1)*(1-x.deduction))+1),
                    mean_book_NR=lambda x:(((x.mean_book-1)*(1-x.deduction))+1),
                    ex_NR=lambda x:(((x.ex-1)*(1-x.deduction))+1))
            .loc[:, ['name', 'time', 'max_book','max_book_name', 'min_book','min_book_name',
                     'mean_book', 'ex', 'deduction', 'max_book_NR','min_book_NR', 'mean_book_NR', 'ex_NR']]
            # add time lables
            .add_prefix(f'{time}_')
            .rename(columns={f'{time}_name': 'name', f'{time}_time': 'time',f'{time}_bsp': 'bsp',
                             f'{time}_horse_isp': 'isp' , f'{time}_position': 'position'}))


# gets key time data and adjusts prices for 1am, 6am and 10am prices
def get_key_time_data(hourly_odds, price_deductions):
    times = [1, 6, 10]
    times_2 = ['01:00', '06:00', '10:00']
    data_frames = []
    for time, t2 in zip(times, times_2):
        time_am_data  = adjust_prices(get_odds(hourly_odds,time, t2), get_deductions(time, price_deductions),time)
        data_frames.append(time_am_data)
    print('Key time data extracted...')
    return reduce(lambda left, right: pd.merge(left, right,on=['name', 'time'], how='outer'), data_frames) 
       
