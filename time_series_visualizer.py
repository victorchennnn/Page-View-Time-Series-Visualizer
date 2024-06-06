import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')


# Clean data
value_upper = df['value'].quantile(0.975)
value_lower = df['value'].quantile(0.025)
df = df[(df['value'] >= value_lower) & (df['value'] <= value_upper)]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df["value"], color="r")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.resample('M').mean()
    df_bar["months"] = df_bar.index.month_name()
    df_bar["year"] = df_bar.index.year

    # Draw bar plot
    df_bar = df_bar.pivot(index="year", columns="months", values="value")
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
               "October", "November", "December"]
    df_bar = df_bar[months]

    fig, ax = plt.subplots(figsize=(10, 7))
    df_bar.plot(kind='bar', xlabel="Years", ylabel="Average Page Views", ax=ax)
    ax.legend(title="Months")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig



def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]


    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2, figsize=(25, 10))
    sns.color_palette("hls", 9)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    ax[0] = sns.boxplot(data=df_box, x="year", y="value", hue="year", palette="tab10", legend=False,
                         ax=ax[0])
    ax[0].set_title("Year-wise Box Plot (Trend)")
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel("Page Views")


    ax[1] = sns.boxplot(data=df_box, x="month", y="value", hue="month", palette="hls", order=months,
                         legend=False, ax=ax[1])
    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("Page Views")


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
