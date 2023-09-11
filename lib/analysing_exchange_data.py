import pandas as pd
from . import calculations


'''
DEFINITIONS

MORNINGWAP = Average weighted price traded on betfair exchange before 11am

PPWAP = Average weighted price traded on betfair exchange before race starts

MORNINGTRADEDVOL = Volume traded on exchange for selection before 11am

PPTRADEDVOL = Volume traded on exchange for selection before race starts
'''


# compare betfair exchange prices at various times
def compare_exchange_data(df):
    return (calculations.rank_by_race_ascending(df, 'predicted_position_morningwap', 'time', 'MORNINGWAP')
        # predict positions based on PPWAP
        .pipe(calculations.rank_by_race_ascending, 'predicted_position_ppwap', 'time', 'PPWAP')

        # change in price between MORNINGWAP and PPWAP
        .pipe(calculations.calculate_pct_change, 'MORNINGWAP', 'PPWAP', 'wap_change')

        # rank runners on change in price between MORNINGWAP AND PPWAP
        .pipe(calculations.rank_by_race_ascending, 'wap_change_rank', 'time', 'wap_change')

        # rank runners based off volume traded before 11am
        .pipe(calculations.rank_by_race_descending, 'morning_tradedvol_rank', 'time', 'MORNINGTRADEDVOL')

        # average volume traded on selectino before 11am
        .pipe(calculations.mean_value, 'morning_tradedvol_race_average', 'time', 'MORNINGTRADEDVOL')

        # compare race average to selection MORNINGTRADEDVOL
        .pipe(calculations.calculate_pct_change, 'morning_tradedvol_race_average', 'MORNINGTRADEDVOL', 
                                                 'morning_tradedvol_compared_race_average')

        # rank runners based off volume traded before race starts
        .pipe(calculations.rank_by_race_descending, 'total_tradedvol_rank', 'time', 'PPTRADEDVOL')

        # average volume traded on selectino before race
        .pipe(calculations.mean_value, 'total_tradedvol_race_average', 'time', 'PPTRADEDVOL')

        # compare race average to selection PPTRADEDVOL
        .pipe(calculations.calculate_pct_change, 'total_tradedvol_race_average', 'PPTRADEDVOL', 
                                                 'total_tradedvol_compared_race_average')

        # change in volume traded between MORNINGWAP and PPWAP
        .pipe(calculations.calculate_pct_change, 'MORNINGTRADEDVOL', 'PPTRADEDVOL', 'tradedvol_change')

        # rank runners based off volume traded before race
        .pipe(calculations.rank_by_race_descending, 'tradedvol_change_rank', 'time', 'tradedvol_change'))
        
