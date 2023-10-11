import pandas as pd
import numpy as np
from supermarket_analysis.constants import *


def preprocess_data(df: pd.DataFrame):
    """Adds columns 'Hour', 'Date', 'Day of week', 'Period of week', 'Day of month',
    'Period of month' and 'Rounded rating' to the dataframe."""
    df['Hour'] = df['Time'].str[:2].astype('int32')
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df['Day of week'] = df['Date'].dt.dayofweek

    def get_period_of_week(day: int):
        if day in range(0, 4):
            return 'Monday-Thursday'
        if day in range(5, 7):
            return 'Weekend'

    df['Period of week'] = df['Day of week'].apply(get_period_of_week)

    df['Day of month'] = df['Date'].apply(lambda date: date.day)

    def get_period_of_month(day_of_month: int):
        if day_of_month <= 9:
            return 'Beginning'
        elif 9 < day_of_month <= 18:
            return 'Middle'
        else:
            return 'Ending'

    df['Period of month'] = df['Day of month'].apply(get_period_of_month)
    df['Rounded rating'] = df['Rating'].apply(round)

    return df


def get_number_of_days(df: pd.DataFrame, by: str = None, start: int = None,
                       end: int = None):
    """Returns number of days belonging to the certain period of month, period od
    week or being a certain day of week. If parameter 'by' is left empty,
    the function returns number of days in a whole dataframe."""
    first_day = min(df['Date'])
    last_day = max(df['Date'])
    dates = pd.date_range(start=first_day, end=last_day)
    if by == 'Week':
        dates = dates[(dates.dayofweek >= start) & (dates.dayofweek < end)]
    elif by == 'Month':
        dates = dates[(dates.day >= start) & (dates.day < end)]
    elif by == 'Day of week':
        dates = dates[dates.dayofweek == start]
    return len(dates)


def prepare_data_for_lineplot(df: pd.DataFrame, time_var: str, start: int,
                              stop: int, mode: str, divided_by: str = None):
    """Returns dataframe including as it's columns time (hour or day of week),
    number representing sale effectiveness in that time per day (average number of
    sales or average income) and - if 'divided_by' is not None - the name of group
    for which the number is calculated."""
    lists_to_make_df = []
    groups = {}
    if divided_by is None:
        groups['df'] = df
    else:
        group_names = df[divided_by].unique()
        for group_name in group_names:
            groups[group_name] = df[df[divided_by] == group_name]
    for group_data in groups.values():
        for moment in range(start, stop):
            moment_data = group_data[group_data[time_var] == moment].reset_index()
            data_for_modes = {'sum': moment_data[TOTAL].sum(),
                              'count': moment_data[TOTAL].count()}
            mode_amount = data_for_modes[mode]
            nums_of_days = {'Hour': get_number_of_days(df),
                            'Day of week': get_number_of_days(df, 'Day of week',
                                                              moment)}
            number_of_days = nums_of_days[time_var]
            if divided_by is not None:
                lst = [moment_data[divided_by][0], moment_data[time_var][0],
                       mode_amount / number_of_days]
                # In moment_data all the records have the same value of 'divided_by'
                # and 'time_var' variables. Hence, we can use 0 as well as any other
                # index to get the value.
                col_names = [divided_by, time_var, 'Average amount']
            else:
                lst = [moment_data[time_var][0], mode_amount / number_of_days]
                col_names = [time_var, 'Average amount']
            lists_to_make_df.append(lst)
    df = pd.DataFrame(lists_to_make_df, columns=col_names)
    return df


def prepare_undivided_period_data(df: pd.DataFrame, kind_of_period: str,
                                  num_of_days_in_period: dict, mode: str):
    """Returns dataframe grouped by 'Period of week' or 'Period of month'. Data is
    summed or counted and divided by the number of days in a certain period."""
    df = df[[TOTAL, 'Period of week', 'Period of month']]
    if mode == 'sum':
        period_data = df.groupby(kind_of_period).sum()
    elif mode == 'count':
        period_data = df.groupby(kind_of_period).count()
    period_data = period_data.reindex(POSSIBLE_PERIODS[kind_of_period])

    for period in period_data.index:
        num_of_days = num_of_days_in_period[period]
        period_data[TOTAL][period] = period_data[TOTAL][
                                         period] / num_of_days

    period_data.index = POSSIBLE_PERIODS[kind_of_period]
    return period_data


def prepare_divided_period_data(df: pd.DataFrame, kind_of_period: str,
                                num_of_days_in_period: dict, divided_by: str,
                                mode: str):
    """Returns dataframe including as it's columns period (might be a period of month
    or a period of week),  number representing sale effectiveness in that time per day
    (average number of sales or average income) and the name of group for which the
    number is calculated."""
    periods = POSSIBLE_PERIODS[kind_of_period]

    groups = {}
    group_names = df[divided_by].unique()
    for group_name in group_names:
        for period in periods:
            groups[f'{group_name}|{period}'] = df.loc[
                (df[divided_by] == group_name) & (df[kind_of_period] == period)]

    period_table = []
    for group in groups:
        if mode == 'sum':
            avg_amount = groups[group][TOTAL].sum()
        elif mode == 'count':
            avg_amount = groups[group][TOTAL].count()
        dividing_var, period = group.split(sep='|')
        if period != 'None':
            number_of_days = num_of_days_in_period[period]
            period_table.append(
                [dividing_var, period, avg_amount / number_of_days])

    df = pd.DataFrame(period_table, columns=[divided_by, kind_of_period,
                                             'Average daily income'])
    return df


def prepare_stat_table(df: pd.DataFrame, measured_variable: str, divided_by: str):
    """Divides data into two groups based on a chosen variable and returns a
    dataframe with a mean and a standard deviation of a measured variable for each
    group."""
    group1_name, group2_name = df[divided_by].unique()
    group1_data = df[df[divided_by] == group1_name]
    group2_data = df[df[divided_by] == group2_name]
    group1_counts = []
    group2_counts = []
    for measured_var_level in df[measured_variable].unique():
        group1_counts.extend(group1_data[group1_data[measured_variable] ==
                                         measured_var_level].count())
        group2_counts.extend(group2_data[group2_data[measured_variable] ==
                                         measured_var_level].count())
    measured_var_stats = {'Mean': {group1_name: np.mean(group1_counts), group2_name:
        np.mean(group2_counts)},
                          'Std': {group1_name: np.std(group1_counts), group2_name:
                              np.std(group2_counts)}}
    measured_var_stats = pd.DataFrame.from_dict(measured_var_stats)
    return measured_var_stats


def prepare_total_income_data(df: pd.DataFrame, divided_by: str, hour_of_interest:
int = None):
    """Returns dataframe of groups and it's total income. Data might be filter by a 
    chosen hour."""
    if hour_of_interest is not None:
        df = df[df['Hour'] == hour_of_interest]
    df = df[[divided_by, TOTAL]].groupby(divided_by).sum()
    print(df.index)
    df = df.reindex(VAR_UNIQUES[divided_by])
    df.index = VAR_UNIQUES[divided_by]  # bez tego nie działa - czemu?
    return df
