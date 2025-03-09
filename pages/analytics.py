import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from snowflake.sqlalchemy import URL

# ✅ Page Config
st.set_page_config(page_title="Animal Analytics", page_icon="📊", layout="wide")

st.title("📊 Animal Analytics Dashboard")

# ✅ Snowflake Connection
SNOWFLAKE_USER = "daveondecks"
SNOWFLAKE_PASSWORD = "thomas100Amario"
SNOWFLAKE_ACCOUNT = "npagkyh-jb20462"
SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"
SNOWFLAKE_DATABASE = "PETSDB"
SNOWFLAKE_SCHEMA = "PUBLIC"

engine = create_engine(
    URL(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )
)

def fetch_data():
    query = "SELECT SPECIES, AGE, COLOUR FROM ANIMALS;"
    df = pd.read_sql(query, engine)

    # ✅ Force column names to uppercase to match Snowflake
    df.columns = df.columns.str.upper()

    return df

# ✅ Load Data
df = fetch_data()

# 🔍 Debugging: Check if DataFrame is empty
if df.empty:
    st.error("❌ No data found in the ANIMALS table!")
else:
    # ✅ Sidebar Filters
    species_list = df["SPECIES"].unique().tolist()
    selected_species = st.sidebar.multiselect("Filter by Species", species_list, default=species_list)

    filtered_df = df[df["SPECIES"].isin(selected_species)]

    # 📊 Age Distribution Chart
    st.subheader("📈 Age Distribution")
    fig = px.histogram(filtered_df, x="AGE", nbins=10, title="Age Distribution of Animals")
    st.plotly_chart(fig)

    # 📊 Colour Distribution
    st.subheader("🎨 Colour Distribution")
    fig2 = px.pie(filtered_df, names="COLOUR", title="Colour Distribution of Animals")
    st.plotly_chart(fig2)
