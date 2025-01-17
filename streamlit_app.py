import altair as alt
import pandas as pd
import streamlit as st

def mos(row):
    marketcap = parse_formatted_number(row['marketcap'])
    pv = parse_formatted_number(row['pessimisticvalue'])

    if marketcap > pv:
        return 0
    else:
        return round(((pv - marketcap) / pv) * 100, 1)

def parse_formatted_number(formatted):
    multiplier = {'T': 1_000_000_000_000, 'B': 1_000_000_000, 'M': 1_000_000, 'K': 1_000}
    
    # Check if the last character is a known suffix
    if formatted[-1] in multiplier:
        value = float(formatted[:-1])  # Extract the number part
        return int(value * multiplier[formatted[-1]])  # Multiply by the corresponding multiplier
    else:
        # No suffix, return as integer
        return int(formatted)
    
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
balance_sheet = st.slider("balance sheet Rating", 1, 5, (1, 5), help="**Explanation:** The balance sheet rating reflects the qualtiy of its finances (debt, assets, etc.).")
understandability = st.slider("understandability Rating", 1, 5, (1, 5), help="**Explanation:** The understandability rating assesses how easy it is for a regard to understand the business")
moat = st.slider("Moat Rating", 1, 5, (1, 5), help="**Explanation:** The moat rating indicates the strength and sustainability of a company’s competitive advantage.")

df_filtered = df[(df["moat"].between(moat[0], moat[1])) & (df["balance_sheet_health"].between(balance_sheet[0], balance_sheet[1]))\
                 & (df["understandability"].between(understandability[0], understandability[1]))]

# DISPLAY: XYZ Stocks

df_filtered['balance_sheet'] = df_filtered['balance_sheet_health'].apply(lambda x: f"{x}/5")
df_filtered['moat'] = df_filtered['moat'].apply(lambda x: f"{x}/5")
df_filtered['understandability'] = df_filtered['understandability'].apply(lambda x: f"{x}/5")

df_filtered["ticker"] = df_filtered["ticker"].apply(lambda x: f'<a href="https://moatboy.github.io/docs/{x}.html">{x}</a>')

# Display the data as a table using `st.dataframe`.
# st.dataframe(
#     df_filtered,
#     use_container_width=True,
#     column_config={"ticker": st.column_config.TextColumn("ticker")},
# )

st.markdown(f"### {len(df_filtered)} Stocks")
st.markdown(df_filtered.to_html(escape=False, index=False), unsafe_allow_html=True)
