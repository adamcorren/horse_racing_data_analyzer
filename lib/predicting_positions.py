import pandas as pd
from . import calculations
  
# get fave and predicted positions for morning/'key time' prices (1,6,10 am)
def get_price_predictions(df):
    times = ['1', '6', '10', 'BSP', 'isp']
    col_names = ['1_mean_book', '6_mean_book', '10_mean_book', 'BSP', 'isp']
    for t, n in zip(times, col_names):
        df = (df
            .pipe(calculations.rank_by_race_ascending_time,  'predicted_position', 'time', n, t) 
            .pipe(calculations.get_favourite,  'fave', f"predicted_position_{t}", t) )
    print('Predicted positions completed...')
    return df


