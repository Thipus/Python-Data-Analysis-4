import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import warnings
warnings.filterwarnings("ignore")

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',parse_dates=True,index_col='date')
#print(df.index.size)
#print(df[(df['value']>df['value'].quantile(0.025))].index.size)
#print(df[(df['value']<df['value'].quantile(0.975))].index.size)
#print(df[(df['value']<df['value'].quantile(0.975)) & (df['value']>df['value'].quantile(0.025))].index.size)

# Clean data
df = df[(df['value']<df['value'].quantile(0.975)) & (df['value']>df['value'].quantile(0.025))]

def draw_line_plot():
    # Draw line plot
    fig, ax=plt.subplots(figsize=(20, 10))
    ax.plot(df.index,df['value'],'r',linewidth=2)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Month'] = df_bar.index.month_name()
    #print(df_bar.index.year)
    df_bar['Year']=df_bar.index.year.astype('int64')
    column_names = ["Year","Month", "value"]
    df_bar = df_bar.reindex(columns=column_names)
    df_bar2=df_bar.groupby(['Year','Month'])['value'].mean()
    df_bar2=df_bar2.unstack()
    # Draw bar plot
    fig=df_bar2.plot.bar(legend=True,figsize=(10,5),ylabel='Average Page Views',xlabel='Years').figure
    plt.legend(['January','February','March','April','May','June','July','August','September','October','November','December'])


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box['month_numeric']=df_box['date'].dt.month
    print(df_box)
    df_box=df_box.sort_values('month_numeric')
    print(df_box)

    # Draw box plots (using Seaborn)
    fig, axes=plt.subplots(nrows=1,ncols=2,figsize=(10,5))
    axes[0]=sns.boxplot(data=df_box,x='year',y='value',ax=axes[0])
    axes[1]=sns.boxplot(data=df_box,x='month',y='value')

    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
