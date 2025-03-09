import streamlit as st
import pandas as pd
import io
from PIL import Image
from sqlalchemy import create_engine, text
from snowflake.sqlalchemy import URL

# ✅ Page Config
st.set_page_config(page_title="Animal Records", page_icon="🐾", layout="wide")

st.title("🐾 Animal Records with Images")

# ✅ Sidebar Navigation
st.sidebar.title("Navigation")
st.sidebar.page_link("pets_table.py", label="🐾 Animal Management")
st.sidebar.page_link("pages/analytics.py", label="📊 Analytics")
st.sidebar.page_link("pages/trends.py", label="📈 Animal Trends")
st.sidebar.page_link("pages/export.py", label="📂 Export Data")
st.sidebar.page_link("pages/dashboard.py", label="📊 Records Dashboard")
st.sidebar.page_link("pages/data_entry.py", label="📝 Add Animal Record")

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

# ✅ Fetch data including images
query = "SELECT NAME, SPECIES, AGE, COLOUR, DESCRIPTION, IMAGE FROM ANIMALS"
df = pd.read_sql(query, engine)

df.columns = df.columns.str.upper()  # Ensure column names match Snowflake's uppercase format

# ✅ Display records with images
for index, row in df.iterrows():
    st.subheader(f"{row['NAME']} ({row['SPECIES']})")
    st.write(f"Age: {row['AGE']} | Colour: {row['COLOUR']}")
    st.write(row["DESCRIPTION"])

    # ✅ Show image if available
    if row["IMAGE"]:
        image_bytes = io.BytesIO(row["IMAGE"])
        image = Image.open(image_bytes)
        st.image(image, caption=row["NAME"], use_container_width=True)

st.success("✅ Data loaded successfully!")
