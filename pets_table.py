import streamlit as st
import pandas as pd
import io
from PIL import Image
from sqlalchemy import create_engine, text
from snowflake.sqlalchemy import URL

# ✅ FIRST: Set Page Config
st.set_page_config(page_title="Animal Records", page_icon="🐾", layout="wide")

# ✅ THEN: Define Background Function
def add_background():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://raw.githubusercontent.com/daveondecks/anilams/main/assets/pets_bg.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-blend-mode: overlay;
            background-color: rgba(255, 255, 255, 0.85); /* Semi-transparent overlay */
        }}
        .stApp * {{
            color: #3D3D3D; /* Darker text for better contrast */
            font-weight: bold;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_background()  # ✅ Call Background Function AFTER setting page config

st.title("🐾 Animal Records with Image Thumbnails")

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

# ✅ Fetch Data Including Images
query = "SELECT NAME, SPECIES, AGE, COLOUR, DESCRIPTION, IMAGE FROM ANIMALS"
df = pd.read_sql(query, engine)

df.columns = df.columns.str.upper()  # Ensure column names match Snowflake's uppercase format

# ✅ Display Records with Image Thumbnails
for index, row in df.iterrows():
    col1, col2 = st.columns([1, 3])  # Create layout with two columns
    with col1:
        if row["IMAGE"]:
            image_bytes = io.BytesIO(row["IMAGE"])
            image = Image.open(image_bytes)
            image.thumbnail((100, 100))  # Create a small thumbnail
            if st.button(f"📷 View {row['NAME']}", key=f"btn_{index}"):
                st.image(image_bytes, caption=row["NAME"], use_container_width=True)
            else:
                st.image(image, caption=row["NAME"])
    with col2:
        st.subheader(f"{row['NAME']} ({row['SPECIES']})")
        st.write(f"Age: {row['AGE']} | Colour: {row['COLOUR']}")
        st.write(row["DESCRIPTION"])
    st.markdown("<hr style='border: 0.5px solid #ccc;'>", unsafe_allow_html=True)  # Thin horizontal line

st.success("✅ Data loaded successfully!")
