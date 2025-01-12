import altair as alt
import pandas as pd
import streamlit as st
import yfinance as yf

def mos(row):
    marketcap = parse_formatted_number(row['marketcap'])
    pv = parse_formatted_number(row['pessimisticvalue'])

    if marketcap > pv:
        return "0%"
    else:
        return str(round(((pv - marketcap) / pv) * 100, 1)) + "%"

def parse_formatted_number(formatted):
    multiplier = {'T': 1_000_000_000_000, 'B': 1_000_000_000, 'M': 1_000_000, 'K': 1_000}
    
    # Check if the last character is a known suffix
    if formatted[-1] in multiplier:
        value = float(formatted[:-1])  # Extract the number part
        return int(value * multiplier[formatted[-1]])  # Multiply by the corresponding multiplier
    else:
        # No suffix, return as integer
        return int(formatted)
    

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
#@st.cache_data
def load_data():
    df = pd.read_csv("data/moatboy.csv")
    return df

df = load_data()

# Show a slider widget with the years using `st.slider`.
management = st.slider("Management Rating", 1, 5, (1, 5), help="**Explanation:** The management rating reflects the leadership quality and decision-making abilities of the company’s management.")

catalyst = st.slider("Catalyst Rating", 1, 5, (1, 5), help="**Explanation:** The catalyst rating assesses the likelihood of an upcoming event that can trigger stock price growth.")

moat = st.slider("Moat Rating", 1, 5, (1, 5), help="**Explanation:** The moat rating indicates the strength and sustainability of a company’s competitive advantage.")

df_filtered = df[(df["moat"].between(moat[0], moat[1])) & (df["management"].between(management[0], management[1]))\
                 & (df["catalyst"].between(catalyst[0], catalyst[1]))]

# DISPLAY: XYZ Stocks

df_filtered['management'] = df_filtered['management'].apply(lambda x: f"{x}/5")
df_filtered['moat'] = df_filtered['moat'].apply(lambda x: f"{x}/5")
df_filtered['catalyst'] = df_filtered['catalyst'].apply(lambda x: f"{x}/5")
df_filtered['marketcap'] = df_filtered['ticker'].apply(get_market_cap)
df_filtered['margin of safety'] = df_filtered.apply(mos, axis=1)

# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_filtered,
    use_container_width=True,
    column_config={"ticker": st.column_config.TextColumn("ticker")},
)