import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

from supermarket_analysis.drawing_plots import *
from supermarket_analysis.preparing_data import *
from supermarket_analysis.constants import *

# Reading df

df = pd.read_csv('supermarket_sales - Sheet1.csv')
df = preprocess_data(df)

# Constants based on df

NUM_OF_DAYS_IN_PERIOD = {'Weekend': get_number_of_days(df, 'Week', start=5,
                                                       end=7),
                         'Monday-Thursday': get_number_of_days(df, 'Week',
                                                               start=0,
                                                               end=4),
                         'Beginning': get_number_of_days(df, 'Month',
                                                         start=1, end=10),
                         'Middle': get_number_of_days(df, 'Month',
                                                      start=10, end=19),
                         'Ending': get_number_of_days(df, 'Month',
                                                      start=19, end=32)}

# Countplots of categories

fig, ax = plt.subplots(nrows=2, ncols=3, figsize=MEDIUM_PLOT)
fig.suptitle('Number of sales per category', fontsize=FONTSIZE)

draw_countplot(df, 'Gender', fig, ax, row=0, col=0, title='Gender of customer')
draw_countplot(df, 'Payment', fig, ax, row=0, col=1, title='Payment type')
draw_countplot(df, 'City', fig, ax, row=0, col=2, palette='tab20')
draw_countplot(df, 'Customer type', fig, ax, row=1, col=0, palette='pastel')
draw_countplot(df, 'Product line', fig, ax, row=1, col=1, rotation=90)
draw_countplot(df, 'Rounded rating', fig, ax, row=1, col=2, title='Rating (rounded)',
               palette='mako', add_fig_legend=True)
plt.show()

# Average daily income in time for all data

hour_data = prepare_data_for_lineplot(df, 'Hour', start=STORE_OPENING, stop=STORE_CLOSURE, mode='sum')
day_data = prepare_data_for_lineplot(df, 'Day of week', start=0, stop=7, mode='sum')
week_data = prepare_undivided_period_data(df, 'Period of week',
                                          NUM_OF_DAYS_IN_PERIOD, 'sum')
month_data = prepare_undivided_period_data(df, 'Period of month',
                                           NUM_OF_DAYS_IN_PERIOD, 'sum')

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=MEDIUM_PLOT)
fig.suptitle('Daily income in time', fontsize=FONTSIZE)

draw_time_lineplot(hour_data, 'Hour', ax, row=0, col=0, palette='mako')
draw_time_lineplot(day_data, 'Day of week', ax, row=0, col=1,
                     xlabels=WEEK_DAY_NAMES, palette='mako')
draw_undivided_period_plot(week_data, 'Period od week', ax, row=1, col=0,
                             palette='mako')
draw_undivided_period_plot(month_data, 'Period od month', ax, row=1, col=1,
                             palette='mako')

plt.show()

# Average daily number of sales for all data

hour_data = prepare_data_for_lineplot(df, 'Hour', start=STORE_OPENING, stop=STORE_CLOSURE,
                                      mode='count')
day_data = prepare_data_for_lineplot(df, 'Day of week', start=0, stop=7,
                                     mode='count')
week_data = prepare_undivided_period_data(df, 'Period of week',
                                          NUM_OF_DAYS_IN_PERIOD, 'count')
month_data = prepare_undivided_period_data(df, 'Period of month',
                                           NUM_OF_DAYS_IN_PERIOD, 'count')

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=MEDIUM_PLOT)
fig.suptitle('Daily number of sales in time', fontsize=FONTSIZE)

draw_time_lineplot(hour_data, 'Hour', ax, row=0, col=0, palette='mako')
draw_time_lineplot(day_data, 'Day of week', ax, row=0, col=1,
                     xlabels=WEEK_DAY_NAMES, palette='mako')
draw_undivided_period_plot(week_data, 'Period od week', ax, row=1, col=0,
                             palette='mako')
draw_undivided_period_plot(month_data, 'Period od month', ax, row=1, col=1,
                             palette='mako')

plt.show()

# Gender plots

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=BIG_PLOT)
fig.suptitle('Customer\'s gender comparisons divided by category', fontsize=FONTSIZE)

draw_countplot(df, 'Payment', fig, ax, row=0, col=0, divided_by='Gender',
                 division_order=VAR_UNIQUES['Gender'])
draw_countplot(df, 'City', fig, ax, row=0, col=1, divided_by='Gender',
                 division_order=VAR_UNIQUES['Gender'])
draw_countplot(df, 'Customer type', fig, ax, row=1, col=0, divided_by='Gender',
                 division_order=VAR_UNIQUES['Gender'])
draw_countplot(df, 'Rounded rating', fig, ax, row=1, col=1, divided_by='Gender',
                 division_order=VAR_UNIQUES['Gender'], title='Rating (rouned)',
                 add_fig_legend=True)

plt.show()

gender_product_table = prepare_stat_table(df, 'Product line', 'Gender')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=SMALL_PLOT)
fig.suptitle('Product\'s line vs. customer\'s gender', fontsize=FONTSIZE)
draw_countplot(df, 'Product line', fig, ax, row=0, divided_by='Gender',
                 division_order=VAR_UNIQUES['Gender'], rotation=45)
draw_mean_std_barplot(gender_product_table, fig, ax, row=1, x_label='Gender',
                        y_label='Average number of sales per product line')
plt.show()

hour_data = prepare_data_for_lineplot(df, 'Hour', start=STORE_OPENING, stop=STORE_CLOSURE,
                                      mode='sum', divided_by='Gender')
day_data = prepare_data_for_lineplot(df, 'Day of week', start=0, stop=7,
                                     mode='sum', divided_by='Gender')
week_data = prepare_divided_period_data(df, 'Period of week',
                                        NUM_OF_DAYS_IN_PERIOD, divided_by='Gender',
                                        mode='sum')
month_data = prepare_divided_period_data(df, 'Period of month',
                                         NUM_OF_DAYS_IN_PERIOD, divided_by='Gender',
                                         mode='sum')

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=MEDIUM_PLOT)
fig.suptitle('Daily income in time divided by gender', fontsize=FONTSIZE)

draw_time_lineplot(hour_data, 'Hour', ax, row=0, col=0, divided_by='Gender')
draw_time_lineplot(day_data, 'Day of week', ax, row=0, col=1,
                     divided_by='Gender', xlabels=WEEK_DAY_NAMES)
draw_divided_period_plot(week_data, fig, ax, row=1, col=0, divided_by='Gender',
                           kind_of_period='Period of week')
draw_divided_period_plot(month_data, fig, ax, row=1, col=1, divided_by='Gender',
                           kind_of_period='Period of month', add_fig_legend=True)
plt.show()

total_income_gender_data = prepare_total_income_data(df, divided_by='Gender')
hour_income_gender_data = prepare_total_income_data(df, divided_by='Gender',
                                                    hour_of_interest=13)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=MEDIUM_PLOT)
fig.suptitle('Total income divided by gender', fontsize=FONTSIZE)
draw_total_income_barplots(total_income_gender_data, ax, row=0, divided_by='Gender',
                             suffix='customer\'s gender')
draw_total_income_barplots(hour_income_gender_data, ax, row=1, divided_by='Gender',
                             suffix='customer\'s gender', hour_of_interest=13)
plt.show()

data13 = df[df['Hour'] == 13]
print(stats.ttest_ind(data13[data13['Gender'] == 'Male'][TOTAL],
                      data13[data13['Gender'] == 'Female'][TOTAL]))


# Payment method plots


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=SMALL_PLOT)
fig.suptitle('Payment method comparisons divided by category', fontsize=FONTSIZE)

draw_countplot(df, 'City', fig, ax, row=0, divided_by='Payment')
draw_countplot(df, 'Customer type', fig, ax, row=1, divided_by='Payment',
                 add_fig_legend=True)
plt.show()


fig, ax = plt.subplots(figsize=SMALL_PLOT)
fig.suptitle('Rounded rating by payment method', fontsize=FONTSIZE)
rating_plot = sns.countplot(x='Rounded rating', data=df, hue='Payment',
                            palette='hls')
rating_plot.set_xlabel('Rating (rounded)')
rating_plot.set_ylabel('Number of sales rated with specific value')
rating_plot.set_title('Rounded rating by payment method')
plt.show()


hour_data = prepare_data_for_lineplot(df, 'Hour', start=STORE_OPENING, stop=STORE_CLOSURE,
                                      mode='sum', divided_by='Payment')
day_data = prepare_data_for_lineplot(df, 'Day of week', start=0, stop=7,
                                     mode='sum', divided_by='Payment')
week_data = prepare_divided_period_data(df, 'Period of week',
                                        NUM_OF_DAYS_IN_PERIOD, divided_by='Payment',
                                        mode='sum')
month_data = prepare_divided_period_data(df, 'Period of month',
                                         NUM_OF_DAYS_IN_PERIOD, divided_by='Payment',
                                         mode='sum')

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=MEDIUM_PLOT)
fig.suptitle('Daily income in time divided by payment', fontsize=FONTSIZE)

draw_time_lineplot(hour_data, 'Hour', ax, row=0, col=0, divided_by='Payment')
draw_time_lineplot(day_data, 'Day of week', ax, row=0, col=1,
                     divided_by='Payment', xlabels=WEEK_DAY_NAMES)
draw_divided_period_plot(week_data, fig, ax, row=1, col=0, divided_by='Payment',
                           kind_of_period='Period of week')
draw_divided_period_plot(month_data, fig, ax, row=1, col=1, divided_by='Payment',
                           kind_of_period='Period of month', add_fig_legend=True)
plt.show()

total_income_payment_data = prepare_total_income_data(df, divided_by='Payment')
hour_income_payment_data = prepare_total_income_data(df, divided_by='Payment',
                                                    hour_of_interest=10)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=MEDIUM_PLOT)
fig.suptitle('Total income divided by payment method', fontsize=FONTSIZE)
draw_total_income_barplots(total_income_payment_data, ax, row=0, divided_by='Payment',
                             suffix='payment method')
draw_total_income_barplots(hour_income_payment_data, ax, row=1, divided_by='Payment',
                             suffix='payment method', hour_of_interest=10)
plt.show()

data10 = df[df['Hour'] == 10]
print(stats.f_oneway(data10[data10['Payment'] == 'Cash'][TOTAL],
                    data10[data10['Payment'] == 'Credit card'][TOTAL],
                     data10[data10['Payment'] == 'Ewallet'][TOTAL]))

# City plots


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=SMALL_PLOT)
fig.suptitle('City comparisons divided by category', fontsize=FONTSIZE)

draw_countplot(df, 'Customer type', fig, ax, row=0, divided_by='City', palette='tab20')
draw_countplot(df, 'Rounded rating', fig, ax, row=1, divided_by='City', palette='tab20',
               title='Rating (rounded)', add_fig_legend=True)
plt.show()

hour_data = prepare_data_for_lineplot(df, 'Hour', start=STORE_OPENING,
                                      stop=STORE_CLOSURE,
                                      mode='sum', divided_by='City')
day_data = prepare_data_for_lineplot(df, 'Day of week', start=0, stop=7,
                                     mode='sum', divided_by='City')
week_data = prepare_divided_period_data(df, 'Period of week',
                                        NUM_OF_DAYS_IN_PERIOD, divided_by='City',
                                        mode='sum')
month_data = prepare_divided_period_data(df, 'Period of month',
                                         NUM_OF_DAYS_IN_PERIOD, divided_by='City',
                                         mode='sum')

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=BIG_PLOT)
fig.suptitle('Sale comparisons in time divided by city', fontsize=FONTSIZE)

draw_time_lineplot(hour_data, 'Hour', ax, row=0, col=0, divided_by='City',
                   palette='tab20')
draw_time_lineplot(day_data, 'Day of week', ax, row=0, col=1, divided_by='City',
                   palette='tab20', xlabels=WEEK_DAY_NAMES)
draw_divided_period_plot(week_data, fig, ax, row=1, col=0, divided_by='City',
                         palette='tab20', kind_of_period='Period of week')
draw_divided_period_plot(month_data, fig, ax, row=1, col=1, divided_by='City',
                         palette='tab20', kind_of_period='Period of month',
                         add_fig_legend=True)
plt.show()

total_income_payment_data = prepare_total_income_data(df, divided_by='City')
hour_income_payment_data = prepare_total_income_data(df, divided_by='City',
                                                     hour_of_interest=18)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=MEDIUM_PLOT)
fig.suptitle('Total income divided by city', fontsize=FONTSIZE)
draw_total_income_barplots(total_income_payment_data, ax, row=0, divided_by='City',
                           palette='tab20', suffix='city')
draw_total_income_barplots(hour_income_payment_data, ax, row=1, divided_by='City',
                           palette='tab20', suffix='city', hour_of_interest=18)
plt.show()

data18 = df[df['Hour'] == 18]
print(stats.f_oneway(data18[data18['City'] == 'Mandalay'][TOTAL],
                     data18[data18['City'] == 'Naypyitaw'][TOTAL],
                     data18[data18['City'] == 'Yangon'][TOTAL]))

# Customer type plots

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=SMALL_PLOT)
fig.suptitle('Rounded rating through members vs. other customers', fontsize=FONTSIZE)

rating_plot = sns.countplot(x='Rounded rating', data=df, hue='Customer type',
                            palette='pastel')
rating_plot.set_xlabel('Rating (rounded)')
rating_plot.set_ylabel('Number of sales rated with specific value')
plt.show()

hour_data = prepare_data_for_lineplot(df, 'Hour', start=STORE_OPENING,
                                      stop=STORE_CLOSURE,
                                      mode='sum', divided_by='Customer type')
day_data = prepare_data_for_lineplot(df, 'Day of week', start=0, stop=7,
                                     mode='sum', divided_by='Customer type')
week_data = prepare_divided_period_data(df, 'Period of week', NUM_OF_DAYS_IN_PERIOD,
                                        divided_by='Customer type', mode='sum')
month_data = prepare_divided_period_data(df, 'Period of month', NUM_OF_DAYS_IN_PERIOD,
                                         divided_by='Customer type', mode='sum')

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=BIG_PLOT)
fig.suptitle('Sale comparisons in time divided by customer type', fontsize=FONTSIZE)

draw_time_lineplot(hour_data, 'Hour', ax, row=0, col=0, divided_by='Customer type',
                   palette='pastel')
draw_time_lineplot(day_data, 'Day of week', ax, row=0, col=1,
                   divided_by='Customer type', palette='pastel', xlabels=WEEK_DAY_NAMES)
draw_divided_period_plot(week_data, fig, ax, row=1, col=0, divided_by='Customer type',
                         palette='pastel', kind_of_period='Period of week')
draw_divided_period_plot(month_data, fig, ax, row=1, col=1, divided_by='Customer type',
                         palette='pastel', kind_of_period='Period of month',
                         add_fig_legend=True)
plt.show()

total_income_payment_data = prepare_total_income_data(df, divided_by='Customer type')
hour_income_payment_data = prepare_total_income_data(df, divided_by='Customer type',
                                                     hour_of_interest=20)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=MEDIUM_PLOT)
fig.suptitle('Total income divided by customer type', fontsize=FONTSIZE)
draw_total_income_barplots(total_income_payment_data, ax, row=0,
                           divided_by='Customer type', palette='pastel', suffix='city')
draw_total_income_barplots(hour_income_payment_data, ax, row=1,
                           divided_by='Customer type', palette='pastel', suffix='city',
                           hour_of_interest=20)
plt.show()

data20 = df[df['Hour'] == 20]
print(stats.ttest_ind(data20[data20['Customer type'] == 'Member'][TOTAL],
                      data20[data20['Customer type'] == 'Normal'][TOTAL]))
