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
            binSpacing=0.5
        )
        .encode(
            alt.X(column_name, bin=alt.Bin(step=1), title='Rating'),
            alt.Y('count()', title=None),
            tooltip=[
                'count()',
                alt.X(column_name, bin=alt.Bin(step=1), title='Rating')
                ]
            )
        .properties(width=800, height=400)
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
            color= '#217CA3',
            opacity=0.8
            )
        .encode(
            alt.X('Date:T', title=None),
            alt.Y(column_name, title='Rating'),
            tooltip=['Date:T', column_name]
            )
    )

    loess = fig.transform_loess('Date', column_name, bandwidth=0.4).mark_line(color='#217CA3')

    fig = (fig + loess).properties(width=850, height=500)

    # display the chart
    st.altair_chart(fig, use_container_width=True)


# Define the names of the tabs
tab1, tab2 = st.tabs(['Distribution', 'Trend'])

with tab1:
    st.write('## BVB Team Performance')

    st.write("### 📊 Ratings' Distribution")
    display_distribution('Overall')

    mean = df['Overall'].mean()
    median = df['Overall'].median()
    std_dev = df['Overall'].std()
    mad = (df['Overall'] - df['Overall'].mean()).abs().mean()

    st.write('### 🧮 Summary Statistics')
    st.write(f'Mean: {mean:.2f}')
    st.write(f'Median: {median:.2f}')
    st.write(f'Standard Deviation: {std_dev:.2f}')
    st.write(f'Mean Absolute Deviation: {mad:.2f}')

with tab2:
    st.write('## BVB Team Performance')

    st.write('### 📈 Ratings Over Time')
    display_trend('Overall')
