import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
url = 'https://docs.google.com/spreadsheets/d/1WFfAL1ixsncQ46V0yLfE8pLovzSvjVg3hJhmJHTaUEw/export?format=csv'
df = pd.read_csv(url)

# convert date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Define grouping columns
group_cols = ['Game', 'Competition', 'Date', 'Writer']

# Define player columns to plot
players = [
    'Gregor Kobel', 'Alexander Meyer', 'Soumaila Coulibaly', 'Mats Hummels',
    'Nico Schlotterbeck', 'Niklas Sule', 'Julian Ryerson', 'Tom Rothe',
    'Felix Passlack', 'Thomas Meunier', 'Rapha Guerreiro', 'Marius Wolf',
    'Salih Ozcan', 'Emre Can', 'Mahmoud Dahoud', 'Jude Bellingham',
    'Julian Brandt', 'Gio Reyna', 'Marco Reus', 'Thorgan Hazard',
    'Jamie Bynoe-Gittens', 'Justin Njinmah', 'Karim Adeyemi',
    'Donyell Malen', 'Youssoufa Moukoko', 'Sebastien Haller',
    'Anthony Modeste'
    ]

# create a function to plot ratings distribution
def display_distribution(column_name1, column_name2):

    # define columns to be melted
    melt_cols = [column_name1, column_name2]

    # convert df to long format
    df_long = pd.melt(
        df,
        id_vars=df.columns.drop(melt_cols),
        value_vars=melt_cols,
        var_name='player',
        value_name='rating'
        )

    # Round the ratings to the nearest integer
    df_long['rating'] = df_long['rating'].round()

    # Create a histogram of the ratings using Plotly Express
    fig = px.histogram(
        df_long, x='rating', color='player',
        barmode='group',
        nbins=20, range_x=[0, 10],
        labels={'rating': 'Rating'},
        opacity=0.8, width=800, height=400
        )

    # remove border of each bar
    fig.update_traces(marker_line_width=0, marker_line_color='rgba(0,0,0,0)')

    # set gap between the bars
    fig.update_layout(bargap=0.1, legend_title=None, yaxis_title=None)
    st.plotly_chart(fig)

# create a function to plot ratings over time
def display_trend(column_name1, column_name2):

    # define columns to be melted
    melt_cols = [column_name1, column_name2]

    # convert df to long format
    df_long = pd.melt(
        df,
        id_vars=df.columns.drop(melt_cols),
        value_vars=melt_cols,
        var_name='player',
        value_name='rating'
        )

    # scatter plot with lowess curves
    fig = px.scatter(
        df_long, x='Date', y='rating', color='player',
        trendline='lowess', trendline_options=dict(frac=0.6),
        labels={'rating': 'Rating'},
        width=800, height=400
        )
    fig.update_layout(legend_title=None)
    st.plotly_chart(fig)

# Create a sidebar with a dropdown menu to select the column to plot
selected_player1 = st.sidebar.selectbox(
    label='## Select First Player to Compare',
    options=players
    )

selected_player2 = st.sidebar.selectbox(
    label='## Select Second Player to Compare',
    options=players
    )

# Define the names of the tabs
tab1, tab2 = st.tabs(['Distribution', 'Trend'])

with tab1:
    st.write(f'## {selected_player1} vs {selected_player2}')

    st.write("### 📊 Ratings' Distribution")
    display_distribution(selected_player1, selected_player2)

    mean1 = df[selected_player1].mean()
    median1 = df[selected_player1].median()
    std_dev1 = df[selected_player1].std()
    mad1 = (df[selected_player1] - df[selected_player1].mean()).abs().mean()

    st.write('### 🧮  Summary Statistics')
    st.write(f'#### {selected_player1}')
    st.write(f'Mean: {mean1:.2f}')
    st.write(f'Median: {median1:.2f}')
    st.write(f'Standard Deviation: {std_dev1:.2f}')
    st.write(f'Mean Absolute Deviation: {mad1:.2f}')

    mean2 = df[selected_player2].mean()
    median2 = df[selected_player2].median()
    std_dev2 = df[selected_player2].std()
    mad2 = (df[selected_player2] - df[selected_player2].mean()).abs().mean()

    st.write(f'#### {selected_player2}')
    st.write(f'Mean: {mean2:.2f}')
    st.write(f'Median: {median2:.2f}')
    st.write(f'Standard Deviation: {std_dev2:.2f}')
    st.write(f'Mean Absolute Deviation: {mad2:.2f}')

with tab2:
    st.write(f'## {selected_player1} vs {selected_player2}')

    st.write('### 📈 Performance Over Time')
    display_trend(selected_player1, selected_player2)

