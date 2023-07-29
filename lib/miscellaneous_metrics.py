import pandas as pd
from functools import reduce

# convert word abs to numbers where horses finish close together
def adjust_distance_behind(df):
    return (df
            .assign(distance_behind=df
                    .distance_behind
                    .where(df.distance_behind != 'hd', 0.20)
                    .where(df.distance_behind != 'nk', 0.25)
                    .where(df.distance_behind != 'nse', 0.05)
                    .where(df.distance_behind != 'sh', 0.10)
                    .where(df.distance_behind != 1, 0)))


# add nearly won if horse came second by less than 0.5 lengths
def get_nearly_won(df):
    df.distance_behind = pd.to_numeric(df.distance_behind, errors='coerce')
    df.position = pd.to_numeric(df.position, errors='coerce')
    return (df
            .assign(nearly_won=1)
            .assign(nearly_won= lambda x: x.nearly_won.where((x.position == 2) & \
                (x.distance_behind < 0.5), None)))


# get total distance behind winning horse not just horse finished ahead
def get_total_distance_behind(df):
    return (df
            .sort_values(['time', 'position'])
            .reset_index(drop=True)
            .assign(total_distance_behind= lambda x: x.groupby(['time'], sort=True) \
                ['distance_behind'].transform(lambda x: x.rolling(40, min_periods=0).sum())))


def get_racetype(df):
    return df.assign(racetype = lambda x: x.EVENT_NAME.str.split(" ", n=1).str[1],
                     race_location = lambda x: x.MENU_HINT.str.split(" ", n=1).str[0])
          

# get minimum, mean and maximum weights, ages, ratings in race
def get_min_mean_max_metrics(df):
    df[['age', 'weight', 'ratings']] = df[['age', 'weight', 'ratings']] \
        .apply(pd.to_numeric, errors='coerce')
    
    min_weight_age_rating = (df
                             .groupby('time')
                             .agg({'time': 'first', 'age': 'min', 'weight': 'min', 'ratings': 'min'})
                             .rename(columns={'age': 'horse_min_age', 'weight': 'horse_min_weight',
                                              'ratings': 'horse_min_rating'})
                             .reset_index(drop=True)
                             .round())

    max_weight_age_rating = (df
                             .groupby('time')
                             .agg({'time': 'first', 'age': 'max', 'weight': 'max', 'ratings': 'max'})
                             .rename(columns={'age': 'horse_max_age', 'weight': 'horse_max_weight',
                                              'ratings': 'horse_max_rating'})
                             .reset_index(drop=True)
                             .round())

    mean_weight_age_rating = (df
                              .groupby('time')
                              .agg({'time': 'first', 'age': 'mean', 'weight': 'mean', 'ratings': 'mean'})
                              .rename(columns={'age': 'horse_mean_age', 'weight': 'horse_mean_weight',
                                               'ratings': 'horse_mean_rating'})
                              .reset_index(drop=True)
                              .round())
    
    data_frames = [min_weight_age_rating, max_weight_age_rating, mean_weight_age_rating]
    metrics = reduce(lambda left, right: pd.merge(left, right, on='time', how='outer'), data_frames) 
    return pd.merge(df, metrics, on='time', how='left').drop(columns=['EVENT_NAME', 'MENU_HINT'])


# main function
def add_other_metrics(df):
    print('Adding final metrics')
    return (df
            .pipe(adjust_distance_behind)
            .pipe(get_nearly_won)
            .pipe(get_total_distance_behind)
            .pipe(get_racetype)
            .pipe(get_min_mean_max_metrics))

