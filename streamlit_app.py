import altair as alt
import pandas as pd
import streamlit as st
import yfinance as yf

def mos(row):
    if row['marketcap'] > row['pessimistic value']:
        return 0
    else:
        return ((row['pessimistic value'] - row['marketcap']) / row['pessimistic value']) * 100

def format_large_number(number):
    if number >= 1_000_000_000_000:
        return f"{number / 1_000_000_000_000:.1f}T"  # Trillions
    elif number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f}B"  # Billions
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"  # Millions
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"  # Thousands
    else:
        return str(number)  # No formatting needed

def get_market_cap(ticker):
    stock = yf.Ticker(ticker)
    return format_large_number(stock.info['marketCap']) if 'marketCap' in stock.info else None

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

df_filtered['marketcap'] = df['ticker'].apply(get_market_cap)
df_filtered['margin of safety (in %)'] = df_filtered.apply(mos, axis=1)

# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_filtered,
    use_container_width=True,
    column_config={"ticker": st.column_config.TextColumn("ticker")},
)
