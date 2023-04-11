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
def display_distribution(column_name):
    # Round the ratings to the nearest integer
    rounded_ratings = df[column_name].round()
    # Create a histogram of the ratings using Plotly Express
    fig = px.histogram(
        rounded_ratings, x=column_name, nbins=20, range_x=[0, 10],
        labels={column_name: 'Rating'},
        opacity=0.8, width=800, height=400
        )
    # remove border of each bar
    fig.update_traces(marker_line_width=0, marker_line_color='rgba(0,0,0,0)')
    # set gap between the bars
    fig.update_layout(bargap=0.1, yaxis_title=None)
    st.plotly_chart(fig)

# create a function to plot ratings over time
def display_trend(column_name):
    # scatter plot with lowess curves
    fig = px.scatter(
        df, x='Date', y=column_name, trendline='lowess',
        trendline_options=dict(frac=0.6),
        labels={column_name: 'Rating'},
        width=800, height=400
        )

    fig.update_layout(xaxis_title=None)
    st.plotly_chart(fig)

# Create a sidebar with a dropdown menu to select the column to plot
selected_player = st.sidebar.selectbox(
    label='## Select a player to display',
    options=players
    )

# Define the names of the tabs
tab1, tab2 = st.tabs(['Distribution', 'Trend'])

with tab1:
    st.write(f'## {selected_player}')

    st.write("### 📊 Ratings' Distribution")
    display_distribution(selected_player)

    mean = df[selected_player].mean()
    median = df[selected_player].median()
    std_dev = df[selected_player].std()
    mad = (df[selected_player] - df[selected_player].mean()).abs().mean()

    st.write('### 🧮 Summary Statistics')
    st.write(f'Mean: {mean:.2f}')
    st.write(f'Median: {median:.2f}')
    st.write(f'Standard Deviation: {std_dev:.2f}')
    st.write(f'Mean Absolute Deviation: {mad:.2f}')

with tab2:
    st.write(f'## {selected_player}')

    st.write('### 📈 Performance Over Time')
    display_trend(selected_player)

