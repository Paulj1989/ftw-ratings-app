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

    # plot ratings distribution
    fig = (
        alt
        .Chart(df_long)
        .mark_bar(
            cornerRadiusTopLeft=3,
            cornerRadiusTopRight=3,
            opacity=0.5,
            binSpacing=0.5
            )
        .encode(
            x=alt.X('rating:Q', title='Rating', bin=alt.Bin(maxbins=10)),
            y=alt.Y('count()', title=None, stack=None),
            color=alt.Color(
                'player:N', title=None,
                scale=alt.Scale(
                    domain=[column_name1, column_name2],
                    range=['#217CA3', '#C4274C']
                    ))
        )
        .properties(width=850, height=500)
        .configure_legend(orient='top')
        # remove border of each bar
        .configure_mark(strokeWidth=0)
        .configure_axis(grid=False)
    )

    st.altair_chart(fig, use_container_width=True)


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

    # Round the ratings to the nearest integer
    df_long['rating'] = df_long['rating'].round()

    # scatter plot with loess curves
    fig = (
        alt
        .Chart(df_long)
        .mark_circle()
        .encode(
            x=alt.X('Date:T', title=None, axis=alt.Axis(format='%B')),
            y=alt.Y('rating:Q', title='Rating'),
            color=alt.Color(
                'player:N', title=None,
                scale=alt.Scale(
                    domain=[column_name1, column_name2],
                    range=['#217CA3', '#C4274C']
                    ))
        )
        .properties(width=750, height=500)
    )

    loess = (
        fig
        .transform_loess(
            'Date', 'rating', groupby=['player'], bandwidth=0.6
            )
        .mark_line()
    )

    fig = (fig + loess).configure_legend(orient='top', title=None)

    st.altair_chart(fig, use_container_width=True)


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

    st.write('### 🧮  Summary Statistics')

    col1, col2 = st.columns((1, 1))

    with col1:
        mean1 = df[selected_player1].mean()
        median1 = df[selected_player1].median()
        std_dev1 = df[selected_player1].std()
        mad1 = (df[selected_player1] - df[selected_player1].mean()).abs().mean()

        st.write(f'#### {selected_player1}')
        st.write(f'Mean: {mean1:.2f}')
        st.write(f'Median: {median1:.2f}')
        st.write(f'Standard Deviation: {std_dev1:.2f}')
        st.write(f'Mean Absolute Deviation: {mad1:.2f}')

    with col2:

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
