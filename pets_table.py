import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL  # ✅ Import correct Snowflake SQLAlchemy URL

# ✅ Snowflake Connection Setup
SNOWFLAKE_USER = "daveondecks"
SNOWFLAKE_PASSWORD = "thomas100Amario"
SNOWFLAKE_ACCOUNT = "npagkyh-jb20462"
SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"
SNOWFLAKE_DATABASE = "PETSDB"
SNOWFLAKE_SCHEMA = "PUBLIC"

# ✅ Use Snowflake's SQLAlchemy URL for compatibility with Streamlit Cloud
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
    query = "SELECT * FROM ANIMALS ORDER BY ID;"
    df = pd.read_sql(query, engine)
    return df

# ✅ Streamlit UI
df = fetch_data()
st.title("🐾 Animal Records Management")
st.dataframe(df)

# 🆕 Add New Animal
st.subheader("➕ Add New Animal")
name = st.text_input("Animal Name")
species = st.text_input("Species")
age = st.number_input("Age", min_value=0, step=1)
colour = st.text_input("Colour")
description = st.text_area("Description")

if st.button("Add Animal"):
    with engine.connect() as conn:
        conn.execute("""
            INSERT INTO ANIMALS (NAME, SPECIES, AGE, COLOUR, DESCRIPTION)
            VALUES (:name, :species, :age, :colour, :description)
        """, {"name": name, "species": species, "age": age, "colour": colour, "description": description})
        conn.commit()
    st.success("✅ Animal Added Successfully!")
    st.rerun()

# ✏️ Update Existing Animal
st.subheader("✏️ Update Animal")
update_id = st.number_input("Enter ID to Update", min_value=1, step=1)
new_name = st.text_input("New Name")
new_species = st.text_input("New Species")
new_age = st.number_input("New Age", min_value=0, step=1)
new_colour = st.text_input("New Colour")
new_description = st.text_area("New Description")

if st.button("Update Animal"):
    with engine.connect() as conn:
        conn.execute("""
            UPDATE ANIMALS SET 
            NAME = :new_name, SPECIES = :new_species, AGE = :new_age, 
            COLOUR = :new_colour, DESCRIPTION = :new_description
            WHERE ID = :update_id
        """, {"new_name": new_name, "new_species": new_species, "new_age": new_age, "new_colour": new_colour, "new_description": new_description, "update_id": update_id})
        conn.commit()
    st.success(f"✅ Animal ID {update_id} Updated!")
    st.rerun()

# ❌ Delete Animal
st.subheader("❌ Delete Animal")
delete_id = st.number_input("Enter ID to Delete", min_value=1, step=1)
if st.button("Delete Animal"):
    with engine.connect() as conn:
        conn.execute("DELETE FROM ANIMALS WHERE ID = :delete_id", {"delete_id": delete_id})
        conn.commit()
    st.warning(f"⚠️ Animal ID {delete_id} Deleted!")
    st.rerun()