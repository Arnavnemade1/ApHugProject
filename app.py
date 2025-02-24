import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Local Food Systems Tracker",
    page_icon="🌾",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .local-tag {
        color: #2E7D32;
        background-color: #C8E6C9;
        padding: 5px 10px;
        border-radius: 15px;
    }
    .regional-tag {
        color: #1976D2;
        background-color: #BBDEFB;
        padding: 5px 10px;
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with sample data
if 'producers' not in st.session_state:
    st.session_state.producers = pd.DataFrame({
        'name': ['Green Acres', 'Sunny Valley', 'River Farm', 'Highland Ranch'],
        'distance': [15, 25, 45, 30],
        'products': ['Vegetables', 'Dairy', 'Meat', 'Fruits'],
        'certification': ['Organic', 'Conventional', 'Regenerative', 'Organic'],
        'lat': [40.7128, 40.7589, 40.6892, 40.7281],
        'lon': [-74.0060, -73.9851, -74.0445, -73.9467]
    })

if 'products' not in st.session_state:
    st.session_state.products = pd.DataFrame({
        'name': ['Tomatoes', 'Lettuce', 'Milk', 'Eggs', 'Apples'],
        'price_per_unit': [3.99, 2.99, 4.50, 5.99, 2.99],
        'unit': ['lb', 'head', 'gallon', 'dozen', 'lb'],
        'season': ['Summer', 'Spring/Fall', 'Year-round', 'Year-round', 'Fall'],
        'producer': ['Green Acres', 'Sunny Valley', 'River Farm', 'River Farm', 'Highland Ranch']
    })

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["Dashboard", "Producers", "Products", "Market Analysis"]
)

# Dashboard
if page == "Dashboard":
    st.title("Local Food Systems Dashboard")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Local Producers",
            value=len(st.session_state.producers),
            delta="2 new this month"
        )
    
    with col2:
        avg_distance = st.session_state.producers['distance'].mean()
        st.metric(
            label="Average Food Miles",
            value=f"{avg_distance:.1f} miles",
            delta="-5.2 miles",
            delta_color="inverse"
        )
    
    with col3:
        local_count = len(st.session_state.producers[st.session_state.producers['distance'] <= 30])
        st.metric(
            label="Local Producers (<30 miles)",
            value=local_count,
            delta="1 new this month"
        )
    
    # Map of producers
    st.subheader("Producer Network")
    fig = px.scatter_mapbox(
        st.session_state.producers,
        lat='lat',
        lon='lon',
        hover_name='name',
        hover_data=['products', 'certification'],
        zoom=10,
        title="Local Producer Network"
    )
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig)
    
    # Seasonal products
    st.subheader("Currently In Season")
    current_month = datetime.now().strftime("%B")
    seasonal_products = st.session_state.products[
        st.session_state.products['season'].str.contains('Year-round') |
        st.session_state.products['season'].str.contains(current_month)
    ]
    st.dataframe(seasonal_products)

# Producers page
elif page == "Producers":
    st.title("Producer Directory")
    
    # Add new producer
    with st.expander("Add New Producer"):
        with st.form("new_producer"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Producer Name")
                distance = st.number_input("Distance (miles)", min_value=0)
                products = st.multiselect(
                    "Products",
                    ["Vegetables", "Fruits", "Dairy", "Meat", "Eggs"]
                )
            
            with col2:
                certification = st.selectbox(
                    "Certification",
                    ["Organic", "Conventional", "Regenerative"]
                )
                lat = st.number_input("Latitude", value=40.7128)
                lon = st.number_input("Longitude", value=-74.0060)
            
            submitted = st.form_submit_button("Add Producer")
            if submitted:
                new_producer = pd.DataFrame({
                    'name': [name],
                    'distance': [distance],
                    'products': [', '.join(products)],
                    'certification': [certification],
                    'lat': [lat],
                    'lon': [lon]
                })
                st.session_state.producers = pd.concat([st.session_state.producers, new_producer], ignore_index=True)
                st.success("Producer added successfully!")
    
    # Producer list
    st.subheader("Producer List")
    st.dataframe(st.session_state.producers)
    
    # Producer analytics
    st.subheader("Producer Analytics")
    col1, col2 = st.columns(2)
    
    with col1:
        # Distance distribution
        fig = px.histogram(
            st.session_state.producers,
            x='distance',
            title="Distribution of Food Miles",
            labels={'distance': 'Miles from City Center'}
        )
        st.plotly_chart(fig)
    
    with col2:
        # Certification breakdown
        cert_counts = st.session_state.producers['certification'].value_counts()
        fig = px.pie(
            values=cert_counts.values,
            names=cert_counts.index,
            title="Producer Certifications"
        )
        st.plotly_chart(fig)

# Products page
elif page == "Products":
    st.title("Product Directory")
    
    # Add new product
    with st.expander("Add New Product"):
        with st.form("new_product"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Product Name")
                price = st.number_input("Price per Unit", min_value=0.0, step=0.01)
                unit = st.selectbox("Unit", ["lb", "oz", "bunch", "head", "dozen", "gallon"])
            
            with col2:
                season = st.multiselect(
                    "Season Available",
                    ["Spring", "Summer", "Fall", "Winter", "Year-round"]
                )
                producer = st.selectbox("Producer", st.session_state.producers['name'].tolist())
            
            submitted = st.form_submit_button("Add Product")
            if submitted:
                new_product = pd.DataFrame({
                    'name': [name],
                    'price_per_unit': [price],
                    'unit': [unit],
                    'season': [', '.join(season)],
                    'producer': [producer]
                })
                st.session_state.products = pd.concat([st.session_state.products, new_product], ignore_index=True)
                st.success("Product added successfully!")
    
    # Product list
    st.subheader("Product List")
    st.dataframe(st.session_state.products)
    
    # Seasonal calendar
    st.subheader("Seasonal Availability")
    seasons = ["Spring", "Summer", "Fall", "Winter"]
    for season in seasons:
        st.write(f"**{season}**")
        seasonal = st.session_state.products[
            st.session_state.products['season'].str.contains(season) |
            st.session_state.products['season'].str.contains('Year-round')
        ]
        st.dataframe(seasonal[['name', 'producer', 'price_per_unit', 'unit']])

# Market Analysis
else:
    st.title("Market Analysis")
    
    # Price trends
    st.subheader("Price Trends")
    
    # Generate sample price history
    dates = pd.date_range(start='2024-01-01', end='2024-02-23', freq='W')
    products = st.session_state.products['name'].unique()
    
    price_history = []
    for product in products:
        base_price = st.session_state.products[
            st.session_state.products['name'] == product
        ]['price_per_unit'].iloc[0]
        
        for date in dates:
            # Add some random variation to prices
            price = base_price * (1 + np.random.normal(0, 0.1))
            price_history.append({
                'date': date,
                'product': product,
                'price': price
            })
    
    price_df = pd.DataFrame(price_history)
    
    # Price trend chart
    selected_product = st.selectbox("Select Product", products)
    product_prices = price_df[price_df['product'] == selected_product]
    
    fig = px.line(
        product_prices,
        x='date',
        y='price',
        title=f"{selected_product} Price Trends"
    )
    st.plotly_chart(fig)
    
    # Market insights
    st.subheader("Market Insights")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Price Comparison**")
        current_prices = st.session_state.products.copy()
        current_prices['price_category'] = pd.qcut(
            current_prices['price_per_unit'],
            q=3,
            labels=['Low', 'Medium', 'High']
        )
        st.dataframe(current_prices[['name', 'price_per_unit', 'unit', 'price_category']])
    
    with col2:
        st.write("**Seasonal Analysis**")
        season_counts = pd.Series(
            [season for seasons in st.session_state.products['season']
             for season in seasons.split('/')]
        ).value_counts()
        
        fig = px.bar(
            x=season_counts.index,
            y=season_counts.values,
            title="Products Available by Season"
        )
        st.plotly_chart(fig)

# Footer
st.markdown("---")
st.markdown(
    "Built with ❤️ to support local food systems. "
    "Data last updated: " + datetime.now().strftime("%Y-%m-%d")
)
