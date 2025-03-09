import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from snowflake.sqlalchemy import URL

# ✅ Page Config
st.set_page_config(page_title="Add New Animal Record", page_icon="📝", layout="wide")

st.title("📝 Add New Animal Record")

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

# ✅ Function to reset fields
def reset_fields():
    for key in ["name", "species", "age", "colour", "description"]:
        if key in st.session_state:  
            st.session_state[key] = ""

# ✅ Input Form
with st.form("animal_form"):
    name = st.text_input("Animal Name", max_chars=50, key="name")
    species = st.text_input("Species", max_chars=50, key="species")
    age = st.number_input("Age", min_value=0, step=1, key="age")
    colour = st.text_input("Colour", max_chars=30, key="colour")
    description = st.text_area("Description", key="description")
    submit_button = st.form_submit_button("Add Animal")

    if submit_button:
        if name and species and colour:
            with engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO ANIMALS (NAME, SPECIES, AGE, COLOUR, DESCRIPTION)
                    VALUES (:name, :species, :age, :colour, :description)
                """), {
                    "name": name, "species": species, "age": age, "colour": colour, "description": description
                })
                conn.commit()
            st.success("✅ Animal Added Successfully!")
            reset_fields()
        else:
            st.error("❌ Please fill in all required fields.")
