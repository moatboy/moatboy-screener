import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="MoatBoy Screener", page_icon="📈")
st.title("📈 MoatBoy Screener")
st.write(
    """
    A way to filter the data contained in https://moatboy.github.io/.
    """
)


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_csv("data/moatboy.csv")
    return df


df = load_data()

# Show a slider widget with the years using `st.slider`.
management = st.slider("Management", 1, 5, (1, 5))
catalyst = st.slider("Catalyst", 1, 5, (1, 5))
moat = st.slider("Moat", 1, 5, (1, 5))

# Filter the dataframe based on the widget input and reshape it.
df_filtered = df[(df["moat"].between(moat[0], moat[1])) & (df["management"].between(management[0], management[1]))\
                 & (df["catalyst"].between(catalyst[0], catalyst[1]))]

# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_filtered,
    use_container_width=True,
    column_config={"ticker": st.column_config.TextColumn("ticker")},
)
