import streamlit as st

# Basic page configuration
st.set_page_config(page_title="Local Food Tracker", page_icon="🌾")

# Title
st.title("Local Food Systems Minimal Tracker")

# Simple data storage using session state
if 'producers' not in st.session_state:
    st.session_state.producers = [
        {"name": "Green Acres Farm", "distance": 15, "products": "Vegetables"},
        {"name": "Sunny Valley", "distance": 25, "products": "Dairy"}
    ]

# Display producers
st.subheader("Local Producers")
for producer in st.session_state.producers:
    st.write(f"**{producer['name']}** - {producer['distance']} miles - {producer['products']}")

# Simple form
st.subheader("Add New Producer")
with st.form("new_producer"):
    name = st.text_input("Producer Name")
    distance = st.number_input("Distance (miles)", min_value=0, max_value=100)
    products = st.text_input("Products")
    
    if st.form_submit_button("Add Producer"):
        st.session_state.producers.append({
            "name": name,
            "distance": distance,
            "products": products
        })
        st.experimental_rerun()
