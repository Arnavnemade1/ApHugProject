# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# File paths
PRODUCERS_FILE = 'data/producers.csv'
PRODUCTS_FILE = 'data/products.csv'

# Function to load or initialize data
def load_data(file_path, default_data):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        df = pd.DataFrame(default_data)
        df.to_csv(file_path, index=False)
        return df

# Load data
producers = load_data(PRODUCERS_FILE, {
    'name': ['Green Acres Farm', 'Sunny Valley', 'River Farm'],
    'distance': [15, 25, 45],
    'products': ['Vegetables', 'Dairy', 'Meat'],
    'certification': ['Organic', 'Conventional', 'Regenerative']
})

products = load_data(PRODUCTS_FILE, {
    'name': ['Tomatoes', 'Lettuce', 'Milk'],
    'price': [3.99, 2.99, 4.50],
    'unit': ['lb', 'head', 'gallon'],
    'season': ['Summer', 'Spring', 'Year-round'],
    'producer': ['Green Acres Farm', 'Green Acres Farm', 'Sunny Valley']
})

# Save data back to CSV
def save_data(df, file_path):
    df.to_csv(file_path, index=False)

# Page configuration
st.set_page_config(
    page_title="Local Food Systems",
    page_icon="🌾"
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Producers", "Products"])

# Dashboard
if page == "Dashboard":
    st.title("Local Food Systems Dashboard")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Producers", len(producers))
    with col2:
        st.metric("Total Products", len(products))

    st.subheader("Producers by Certification")
    st.bar_chart(producers['certification'].value_counts())

    st.subheader("Available Products by Season")
    st.bar_chart(products['season'].value_counts())

# Producers Page
elif page == "Producers":
    st.title("Producer Directory")
    st.subheader("Add New Producer")
    with st.form("add_producer"):
        name = st.text_input("Producer Name")
        distance = st.number_input("Distance (miles)", min_value=0)
        products_list = st.text_input("Products (comma separated)")
        certification = st.selectbox("Certification", ["Organic", "Conventional", "Regenerative"])
        if st.form_submit_button("Add Producer"):
            new_producer = pd.DataFrame({
                'name': [name],
                'distance': [distance],
                'products': [products_list],
                'certification': [certification]
            })
            producers = pd.concat([producers, new_producer], ignore_index=True)
            save_data(producers, PRODUCERS_FILE)
            st.success("Producer added!")
    st.subheader("Current Producers")
    st.dataframe(producers)

# Products Page
elif page == "Products":
    st.title("Product Directory")
    st.subheader("Add New Product")
    with st.form("add_product"):
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0.0, step=0.01)
        unit = st.selectbox("Unit", ["lb", "oz", "bunch", "head", "dozen", "gallon"])
        season = st.selectbox("Season", ["Spring", "Summer", "Fall", "Winter", "Year-round"])
        producer = st.selectbox("Producer", producers['name'].tolist())
        if st.form_submit_button("Add Product"):
            new_product = pd.DataFrame({
                'name': [name],
                'price': [price],
                'unit': [unit],
                'season': [season],
                'producer': [producer]
            })
            products = pd.concat([products, new_product], ignore_index=True)
            save_data(products, PRODUCTS_FILE)
            st.success("Product added!")
    st.subheader("Current Products")
    st.dataframe(products)

# Footer
st.markdown("---")
st.caption(f"Local Food Systems Tracker • Last updated: {datetime.now().strftime('%Y-%m-%d')}")

# requirements.txt
# List of dependencies
# ----------------------
# streamlit for the web app
# pandas for data manipulation

streamlit
pandas

# README.md
# Local Food Systems Tracker

## Overview
This Streamlit app helps track local food producers and their products. It allows adding new producers, tracking products, and visualizing certifications and seasonal offerings.

## How to Run
1. Clone this repository:
```bash
git clone https://github.com/your-username/local-food-systems-tracker.git
cd local-food-systems-tracker
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

## Data Storage
Data for producers and products is stored in CSV files under the `data/` directory.

## Features
- Add new producers and products
- Visualize data with bar charts
- View tables of all producers and products

## License
This project is licensed under the MIT License.
