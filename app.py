import streamlit as st
import pandas as pd
from datetime import datetime

# Simple page configuration
st.set_page_config(
    page_title="Local Food Systems",
    page_icon="🌾"
)

# Initialize data if not already in session state
if 'producers' not in st.session_state:
    st.session_state.producers = pd.DataFrame({
        'name': ['Green Acres Farm', 'Sunny Valley', 'River Farm'],
        'distance': [15, 25, 45],
        'products': ['Vegetables', 'Dairy', 'Meat'],
        'certification': ['Organic', 'Conventional', 'Regenerative']
    })

if 'products' not in st.session_state:
    st.session_state.products = pd.DataFrame({
        'name': ['Tomatoes', 'Lettuce', 'Milk'],
        'price': [3.99, 2.99, 4.50],
        'unit': ['lb', 'head', 'gallon'],
        'season': ['Summer', 'Spring', 'Year-round'],
        'producer': ['Green Acres Farm', 'Green Acres Farm', 'Sunny Valley']
    })

# Simple navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Producers", "Products"])

# Dashboard page
if page == "Dashboard":
    st.title("Local Food Systems Dashboard")
    
    # Simple metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Producers", len(st.session_state.producers))
    with col2:
        st.metric("Total Products", len(st.session_state.products))
    
    # Simple tables
    st.subheader("Local Producers")
    st.dataframe(st.session_state.producers)
    
    st.subheader("Available Products")
    st.dataframe(st.session_state.products)

# Producers page
elif page == "Producers":
    st.title("Producer Directory")
    
    # Add producer form
    st.subheader("Add New Producer")
    with st.form("add_producer"):
        name = st.text_input("Producer Name")
        distance = st.number_input("Distance (miles)", min_value=0)
        products = st.text_input("Products (comma separated)")
        certification = st.selectbox("Certification", ["Organic", "Conventional", "Regenerative"])
        
        if st.form_submit_button("Add Producer"):
            new_producer = pd.DataFrame({
                'name': [name],
                'distance': [distance],
                'products': [products],
                'certification': [certification]
            })
            st.session_state.producers = pd.concat([st.session_state.producers, new_producer], ignore_index=True)
            st.success("Producer added!")
    
    # Show existing producers
    st.subheader("Current Producers")
    st.dataframe(st.session_state.producers)

# Products page
elif page == "Products":
    st.title("Product Directory")
    
    # Add product form
    st.subheader("Add New Product")
    with st.form("add_product"):
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0.0, step=0.01)
        unit = st.selectbox("Unit", ["lb", "oz", "bunch", "head", "dozen", "gallon"])
        season = st.selectbox("Season", ["Spring", "Summer", "Fall", "Winter", "Year-round"])
        
        if len(st.session_state.producers) > 0:
            producer = st.selectbox("Producer", st.session_state.producers['name'].tolist())
        else:
            producer = st.text_input("Producer Name")
        
        if st.form_submit_button("Add Product"):
            new_product = pd.DataFrame({
                'name': [name],
                'price': [price],
                'unit': [unit],
                'season': [season],
                'producer': [producer]
            })
            st.session_state.products = pd.concat([st.session_state.products, new_product], ignore_index=True)
            st.success("Product added!")
    
    # Show existing products
    st.subheader("Current Products")
    st.dataframe(st.session_state.products)

# Simple footer
st.markdown("---")
st.caption(f"Local Food Systems Tracker • Last updated: {datetime.now().strftime('%Y-%m-%d')}")
