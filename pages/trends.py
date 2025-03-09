import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from snowflake.sqlalchemy import URL

# ✅ Page Config
st.set_page_config(page_title="Animal Trends", page_icon="📈", layout="wide")

st.title("📈 Animal Trends & Insights")

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

# 🔍 Check if DataFrame is empty
if df.empty:
    st.error("❌ No data found in the ANIMALS table!")
else:
    # 📊 Most Common Species
    st.subheader("🔢 Most Common Species")
    species_counts = df["SPECIES"].value_counts().reset_index()
    species_counts.columns = ["SPECIES", "COUNT"]
    fig1 = px.bar(species_counts, x="SPECIES", y="COUNT", title="Most Common Species")
    st.plotly_chart(fig1)

    # 📊 Age Group Distribution
    st.subheader("📊 Age Distribution")
    fig2 = px.histogram(df, x="AGE", nbins=10, title="Age Distribution of Animals")
    st.plotly_chart(fig2)
