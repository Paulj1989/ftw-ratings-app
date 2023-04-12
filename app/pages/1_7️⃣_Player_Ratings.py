import streamlit as st
import pandas as pd
import altair as alt

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

    # round ratings to nearest integer
    df[column_name] = df[column_name].round()

    # create histogram
    fig = (
        alt
        .Chart(df)
        .mark_bar(
            color='#217CA3',
            cornerRadiusTopLeft=3,
            cornerRadiusTopRight=3,
            binSpacing=0.5,
            strokeWidth=0
        )
        .encode(
            alt.X(column_name, bin=alt.Bin(maxbins=10), title='Rating'),
            alt.Y('count()', title=None),
            tooltip=[
                'count()',
                alt.X(column_name, bin=alt.Bin(step=1), title='Rating')
                ]
            )
        .properties(width=850, height=500)
    )

    # configure figure
    fig = (
        fig
        .configure_mark(opacity=0.8)
        .configure_view(stroke='transparent')
        .configure_axis(grid=False)
        .configure_scale(bandPaddingInner=0.1)
    )

    # display plot
    st.altair_chart(fig, use_container_width=True)


# create a function to plot ratings over time
def display_trend(column_name):

    # scatter plot with lowess curves
    fig = (
        alt
        .Chart(df)
        .mark_point(
            color='#217CA3',
            opacity=0.8
            )
        .encode(
            alt.X('Date:T', title=None),
            alt.Y(column_name, title='Rating'),
            tooltip=['Date:T', column_name]
            )
    )

    loess = fig.transform_loess('Date', column_name, bandwidth=0.6).mark_line(color='#217CA3')

    fig = (fig + loess).properties(width=850, height=500)

    # display the chart
    st.altair_chart(fig, use_container_width=True)


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
