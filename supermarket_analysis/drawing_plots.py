import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from constants import TOTAL


def draw_countplot(df: pd.DataFrame, counted_variable: str, fig, ax,
                     row: int, col: int = None, title: str = None, palette: str =
                     'hls', divided_by: str = None, division_order: list =
                     None, rotation: int = 0, add_fig_legend=False):
    """Draws a count plot of a chosen variable, optionally separately for the records
    with a different values of the variable 'divided_by'"""
    title = counted_variable if title is None else title
    if col is None:
        position = ax[row]
    else:
        position = ax[row, col]
    plot = sns.countplot(x=counted_variable, data=df, ax=position,
                         palette=palette, hue=divided_by, hue_order=division_order)
    plot.set_title(title)
    position.set_ylabel('Number of sales')
    position.set_xlabel('')
    plot.xaxis.set_tick_params(rotation=rotation)
    if divided_by is not None:
        plot.get_legend().remove()
    if add_fig_legend:
        handles, labels = plot.get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center')


def draw_time_lineplot(df: pd.DataFrame, time_var: str, ax, row: int, col: int,
                         divided_by: str = None, xlabels: list = None,
                         palette: str = 'hls'):
    """Draws a line plot of a chosen variable, optionally separately for the records
    with a different values of the variable 'divided_by'"""
    plot = sns.lineplot(data=df, x=time_var, y='Average amount',
                        hue=divided_by, ax=ax[row, col], palette=palette,
                        marker='o', markerfacecolor='black')
    plot.legend([], [], frameon=False)
    # used for week days only
    if xlabels is not None:
        plot.set_xticks(range(len(xlabels)))
        plot.set_xticklabels(xlabels)
        plot.xaxis.set_tick_params(rotation=45)


def draw_divided_period_plot(df: pd.DataFrame, fig, ax, row: int, col: int,
                               divided_by: str,
                               kind_of_period: str = 'Period of week',
                               palette: str = 'hls',
                               add_fig_legend: bool = False):
    """Draws a bar plot of a chosen variable for a certain period of time (period
    of month or period of week) separately for the records with a different values
    of the variable 'divided_by'"""
    plot = sns.barplot(data=df, x=kind_of_period,
                       y='Average daily income', hue=divided_by,
                       ax=ax[row, col], palette=palette)
    plot.get_legend().remove()
    if add_fig_legend:
        handles, labels = plot.get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center')


def draw_undivided_period_plot(df: pd.DataFrame, kind_of_period: str, ax, row: int,
                                 col: int, palette: str = 'hls'):
    """Draws a bar plot of a chosen variable for a certain period of time (period
    of month or period of week)."""
    plot = sns.barplot(data=df.reset_index(), x='index',
                       y=TOTAL, ax=ax[row, col],
                       palette=palette)
    plot.set_xlabel(kind_of_period)
    plot.set_ylabel('Average number of sales per day')


def draw_mean_std_barplot(table: pd.DataFrame, fig, ax, row: int, x_label: str,
                            y_label: str):
    """Draws a bar plot of a chosen variable showing its mean and standard
    deviation."""
    plot = sns.barplot(data=table.reset_index(), x='index', y='Mean',
                       ax=ax[row], palette='hls')
    plot.set_xlabel(x_label)
    plot.set_ylabel(y_label)
    plt.errorbar(table.index, table['Mean'], table['Std'],
                 fmt='.', color='Black', elinewidth=4, capthick=20, errorevery=1,
                 alpha=1, ms=4, capsize=2)

    handles, labels = plot.get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center')


def draw_total_income_barplots(df: pd.DataFrame, ax, row: int, divided_by: str,
                                 suffix: str, palette: str = 'hls', hour_of_interest:
        int = None):
    """Draws a bar plot of a chosen variable for the records with a different values of 
    the variable 'divided_by'. Might be used for all data or only for data filtered 
    by chosen hour."""
    if hour_of_interest is not None:
        end_hour = hour_of_interest + 1
        if hour_of_interest > 12:
            hour_of_interest -= 12
        if end_hour > 12:
            end_hour -= 12
        hours = f' between {hour_of_interest} and {end_hour} pm'
    else:
        hours = ''
    plot = sns.barplot(data=df.reset_index(), x='index', y=TOTAL,
                       ax=ax[row], palette=palette)
    plot.set_xlabel(divided_by)
    plot.set_ylabel('Total income')
    plot.set_title(f'Total income{hours} by {suffix}')
