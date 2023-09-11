from datetime import timedelta
import requests
import pandas as pd
import io

def get_bf_data(day):
    print('Getting exchange data..')
    # we need data from both uk and ireland races, which are stored in two seperate files
    betfair_format = day + timedelta(days=1)
    betfair_format = (betfair_format.strftime("%d%m%Y"))
    betfair_urls = [
        f"https://promo.betfair.com/betfairsp/prices/dwbfpricesukwin{betfair_format}.csv",
        f"https://promo.betfair.com/betfairsp/prices/dwbfpricesirewin{betfair_format}.csv"
        ]

    # write data from each file to global data frame
    all_betfairex_data = pd.DataFrame([])
    for url in betfair_urls:
        try:
            req = requests.get(url)
            data = req.content
            data = pd.read_csv(io.StringIO(data.decode('utf-8')))
            data.drop(['EVENT_ID', 'EVENT_DT', 'SELECTION_ID'], axis=1, inplace=True)
            all_betfairex_data = pd.concat([all_betfairex_data, data])
        except (requests.exceptions.RequestException, pd.errors.EmptyDataError) as e:
            print(f"Error: {e}")

    # clean data
    print('Exchange data collected!...')
    return (all_betfairex_data
            .applymap(lambda x: x.strip() if isinstance(x, str) else x)
            .assign(SELECTION_NAME=all_betfairex_data
                    .SELECTION_NAME
                    .str.replace("'", "")
                    .str.title())
            .reset_index(drop=True)
            .drop_duplicates()
            .rename({'SELECTION_NAME': 'Name'}, axis=1))

