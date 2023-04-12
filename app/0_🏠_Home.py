import streamlit as st

st.set_page_config(
    page_title="FTW Ratings Tracker",
    page_icon="⚽",
)

st.write("# ⚽ Fear The Wall Ratings Tracker ⚽")

st.markdown(
    """
    The Fear The Wall (FTW) Ratings Tracker is a web app that allows you to
    explore the player ratings given to each player, by the FTW writers,
    after every Borussia Dortmund match.

    The app contains a page for individual player ratings, as well as a
    page for exploring overall team performance, and a page for comparing
    players against each other (so that you can make a case that the guy
    you don't like is actually terrible and belongs in the bin).

    ### 👈 Select a page from the sidebar to get started!

    ### Want to Get Involved?
    - Check out [Fear The Wall](https://fearthewall.com)
    - Join the [FTW Discord Server](https://discord.gg/aZ2aCsYBmW)
    - Bother Sean on [Twitter](https://twitter.com/fearthewall)

    ### Further Information
    - FTW Ratings App [GitHub](https://github.com/paulj1989/ftw-ratings-app)
    - [Streamlit](https://streamlit.io)
    - [Vega-Altair](https://altair-viz.github.io/index.html)
    """
)
