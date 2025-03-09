import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from snowflake.sqlalchemy import URL

# ✅ Page Config
st.set_page_config(page_title="Export Animal Records", page_icon="📂", layout="wide")

st.title("📂 Export & Download Animal Records")

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
    query = "SELECT * FROM ANIMALS;"
    df = pd.read_sql(query, engine)
    df.columns = df.columns.str.upper()
    return df

# ✅ Load Data
df = fetch_data()

if df.empty:
    st.error("❌ No data found in the ANIMALS table!")
else:
    st.subheader("📋 Preview of Animal Records")
    st.dataframe(df)

    # 📂 Export Options
    st.subheader("💾 Download Options")
    export_format = st.radio("Choose Export Format:", ("CSV", "Excel"))

    if export_format == "CSV":
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(label="📥 Download CSV", data=csv_data, file_name="animal_records.csv", mime="text/csv")
    else:
        excel_data = df.to_excel(index=False, engine="openpyxl")
        st.download_button(label="📥 Download Excel", data=excel_data, file_name="animal_records.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
