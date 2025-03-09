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
    df.columns = df.columns.str.upper()
    return df

# ✅ Load Data
df = fetch_data()

if df.empty:
    st.error("❌ No data found in the ANIMALS table!")
else:
    # ✅ Sidebar Filters
    species_list = df["SPECIES"].unique().tolist()
    selected_species = st.sidebar.multiselect("Filter by Species", species_list, default=species_list)
    min_age, max_age = st.sidebar.slider("Filter by Age Range", int(df["AGE"].min()), int(df["AGE"].max()), (int(df["AGE"].min()), int(df["AGE"].max())))
    colour_list = df["COLOUR"].unique().tolist()
    selected_colours = st.sidebar.multiselect("Filter by Colour", colour_list, default=colour_list)

    # ✅ Apply Filters
    filtered_df = df[
        (df["SPECIES"].isin(selected_species)) &
        (df["AGE"] >= min_age) &
        (df["AGE"] <= max_age) &
        (df["COLOUR"].isin(selected_colours))
    ]

    # 📊 Age Distribution Chart
    st.subheader("📈 Age Distribution")
    fig1 = px.histogram(filtered_df, x="AGE", nbins=10, title="Age Distribution of Animals", color="SPECIES", barmode="overlay")
    st.plotly_chart(fig1)

    # 📊 Colour Distribution
    st.subheader("🎨 Colour Distribution")
    fig2 = px.pie(filtered_df, names="COLOUR", title="Colour Distribution of Animals")
    st.plotly_chart(fig2)

    # 📊 Species Breakdown
    st.subheader("📊 Species Breakdown")
    species_counts = filtered_df["SPECIES"].value_counts().reset_index()
    species_counts.columns = ["SPECIES", "COUNT"]
    fig3 = px.bar(species_counts, x="SPECIES", y="COUNT", title="Species Count by Category")
    st.plotly_chart(fig3)

    # 📊 Age vs Colour Scatter Plot
    st.subheader("🔍 Age vs Colour Distribution")
    fig4 = px.scatter(filtered_df, x="AGE", y="COLOUR", color="SPECIES", title="Age vs Colour Analysis")
    st.plotly_chart(fig4)
