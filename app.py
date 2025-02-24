import streamlit as st
import pandas as pd

# Basic page configuration
st.set_page_config(page_title="Local Food Tracker", page_icon="🌾")

# Title
st.title("Local Food Systems Simple Tracker")

# Sample data initialization (only on first load)
if 'producers' not in st.session_state:
    st.session_state.producers = pd.DataFrame({
        'name': ['Green Acres Farm', 'Sunny Valley'],
        'distance': [15, 25],
        'products': ['Vegetables', 'Dairy']
    })

# Show simple data table
st.subheader("Local Producers")
st.dataframe(st.session_state.producers)

# Simple form for adding new producers
st.subheader("Add New Producer")
with st.form("new_producer"):
    name = st.text_input("Producer Name")
    distance = st.number_input("Distance (miles)", min_value=0, max_value=100)
    products = st.text_input("Products")
    
    if st.form_submit_button("Add Producer"):
        new_producer = pd.DataFrame({
            'name': [name],
            'distance': [distance],
            'products': [products]
        })
        st.session_state.producers = pd.concat([st.session_state.producers, new_producer], ignore_index=True)
        st.success("Producer added successfully!")
