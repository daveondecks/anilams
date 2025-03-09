import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from snowflake.sqlalchemy import URL

# ✅ Page Config
st.set_page_config(page_title="Animal Records Dashboard", page_icon="📊", layout="wide")

st.title("📊 Animal Records Dashboard")

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
    query = "SELECT ID, SPECIES, AGE, COLOUR, DESCRIPTION FROM ANIMALS;"
    df = pd.read_sql(query, engine)
    df.columns = df.columns.str.upper()
    return df

# ✅ Load Data
df = fetch_data()

if df.empty:
    st.error("❌ No data found in the ANIMALS table!")
else:
    # 📊 Key Metrics
    st.subheader("📈 Key Metrics")
    total_animals = df.shape[0]
    most_common_species = df["SPECIES"].value_counts().idxmax()
    avg_age = round(df["AGE"].mean(), 1)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Animals", total_animals)
    col2.metric("Most Common Species", most_common_species)
    col3.metric("Average Age", avg_age)

    # 📊 Species Distribution
    st.subheader("🔢 Species Distribution")
    species_counts = df["SPECIES"].value_counts().reset_index()
    species_counts.columns = ["SPECIES", "COUNT"]
    fig1 = px.bar(species_counts, x="SPECIES", y="COUNT", title="Species Count")
    st.plotly_chart(fig1)

    # 📊 Age Distribution
    st.subheader("📊 Age Distribution")
    fig2 = px.histogram(df, x="AGE", nbins=10, title="Age Distribution of Animals")
    st.plotly_chart(fig2)

    # 📊 Recently Added Records
    st.subheader("📋 Recently Added Animals")
    recent_animals = df.sort_values(by="ID", ascending=False).head(5)
    st.dataframe(recent_animals)
