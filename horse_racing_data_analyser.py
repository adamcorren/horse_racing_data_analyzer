import datetime
import pandas as pd
from functools import reduce
import sys

from collect import collect_bf, collect_spr

from lib import non_runner_adjustments, key_time_data, predicting_positions, comparing_prices_times, \
                adding_outcomes, analysing_exchange_data, miscellaneous_metrics

def main():
    try:
        while True:
            # set day you want data from
            year_pick = int(input('Select Year (2010) : '))
            month_pick = int(input('Select Month (1-12) : '))
            day_pick = int(input('Select Day (1-31) : '))

            day = datetime.datetime(year_pick, month_pick, day_pick)
            file_format = (day.strftime("%Y-%m-%d"))

            # import hourly data
            try:
                hourly_odds = pd.read_csv(
                    f"daily_data/{file_format}/Odds/Odds.csv")
                hourly_odds['logged'] = hourly_odds['logged'].str.split(' ', expand=True)[1].str[:-3]
                break
            except:
                print('Invalid date or hourly data unavailble, try again...')
                continue

        # import exchange and bookmaker data
        try:
            race_data = pd.read_csv(f"daily_data/{file_format}/exchange_bookie_data.csv")
        except FileNotFoundError:
            bf_data = collect_bf.get_bf_data(day)
            spr_data = collect_spr.get_spr_data(day)

            # merge exchange and bookmaker data and export to csv file
            race_data = pd.merge(bf_data, spr_data, left_on='Name', right_on='names').drop('names', axis=1)
            race_data.to_csv(f"daily_data/{file_format}/exchange_bookie_data.csv", index=False)

        # get non runner price adjustments
        price_deductions = non_runner_adjustments.get_non_runner_adjustments(race_data, hourly_odds)

        # get 1, 6, 10 am summary data from hourly prices and adjust prices with price deductions
        key_times = key_time_data.get_key_time_data(hourly_odds, price_deductions)
        key_time_with_race = pd.merge(key_times, race_data,left_on='name', right_on='Name', how='right').drop('Name', axis=1)

        # add other data points from imported modules
        final_data = (key_time_with_race
                      # predict position based on prices at various times
                      .pipe(predicting_positions.get_price_predictions)
            
                      # compare price changes between bookmaker, exchange, starting prices
                      .pipe(comparing_prices_times.compare_prices)
                        
                      # add betting results for all prices if they were taken
                      .pipe(adding_outcomes.get_results)
                        
                      # compare betfair exchange data
                      .pipe(analysing_exchange_data.compare_exchange_data)
                        
                      # add other miscellaneous metrics
                      .pipe(miscellaneous_metrics.add_other_metrics))

        # clean data
        final_data.sort_values(by='time', inplace=True)
        final_data['date'] = file_format
        final_data = final_data[final_data.name.notna()]

        # export daily file daily folder and master data csv
        final_data.to_csv(f"daily_data/{file_format}/final_data.csv", index=False, header=True)
        final_data.to_csv(f"daily_data/ALL.csv", index=False, header=True, mode='a')

        print('Data exported successfully')
    except FileNotFoundError:
        print('Error, data not collected. Check required hourly data has been collected...')


if __name__ == '__main__':
    main()
        
    # asks user if they want to get data from other days
    while True:
        answer = input('Do you want to collect more data? (yes/no): ')
        if answer == 'yes':
            main()
        elif answer == 'no':
            sys.exit()
        elif answer > 0:
            continue
        else:
            print('Answer not valid')
            continue
