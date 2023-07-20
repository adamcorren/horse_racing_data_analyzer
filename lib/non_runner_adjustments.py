import pandas as pd

# getting all the names of the days non runners
def get_non_runners(race_data):
    return (race_data[['non_runners']]
        .drop_duplicates()
        .dropna()
        .assign(non_runners=race_data.non_runners
                .str.replace("[", "")
                .str.replace("", "")
                .str.replace("'","")
                .str.replace("]","")
                .str.strip()
                .str.split(', '))
        .explode('non_runners')
        .reset_index(drop=True))


# getting last price of non runners (if price over 15 no deductions apply)
def get_non_runners_price(race_data, hourly_odds):
    return (pd.merge(race_data, hourly_odds, left_on='non_runners', right_on='name', how='left')
            .groupby('non_runners',as_index=False)
            .agg({'time': 'first', 'location': 'first', 'non_runners': 'first',
                  'logged': 'last', 'spr': 'last'})
            .astype({'spr': 'float16'})
            .dropna()
            .query('spr < 15')
            .reset_index(drop=True))

    
# getting deductions to remaining runners based on last price of non runner
def get_non_runners_deductions(race_data):
    prices, deductions = [
        [0.00, 1.11, 1.18, 1.25, 1.30, 1.40, 1.53, 1.62, 1.80, 1.95,
         2.20, 2.50, 2.75, 3.39, 4.00, 5.00, 6.50, 10.00, 14.99, 1000],
                          [0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50, 0.45,
                           0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10, 0.05, 0.00]]
    return (race_data
            .assign(deduction=pd.cut(race_data.spr, bins=prices, labels=deductions).astype('float'))
            .groupby(['time', 'logged'], as_index=False)
            .agg({'time': 'first', 'logged': 'first', 'deduction': 'sum'})
            .loc[:, ['time', 'logged', 'deduction']])
    

def get_non_runner_adjustments(race_data, hourly_odds):
    print('Non runner price adjustments complete...')
    return (get_non_runners(race_data)
            .pipe(get_non_runners_price, hourly_odds)
            .pipe(get_non_runners_deductions))


