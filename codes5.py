import streamlit as st
from PIL import Image
import numpy as np
from data import data
from visualisation import visualization

# Page configuration
st.set_page_config(
    page_title="Product and History",
    layout="wide"
)

# Dummy data for products
products = [
    {"name": "Product 1", "price": "$19", "rating": 5, "availability": True, "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
    {"name": "Product 2", "price": "$19", "rating": 5, "availability": False, "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
    {"name": "Product 3", "price": "$19", "rating": 5, "availability": True, "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
    {"name": "Product 4", "price": "$19", "rating": 5, "availability": False, "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
]

# Function to display star ratings
def display_stars(rating):
    return "⭐" * rating

# Product Listing Page
def product_listing():
    st.title("50+ PRODUCT")

    for product in products:
        col1, col2 = st.columns([1, 4])

        with col1:
            st.image(Image.new('RGB', (100, 100), color = 'gray'))  # Placeholder for product image

        with col2:
            st.subheader(product["name"])
            availability_color = "green" if product["availability"] else "red"
            availability_status = "🟢" if product["availability"] else "🔴"
            st.markdown(f"{availability_status} {display_stars(product['rating'])}")
            st.write(product["description"])
            st.write(f"**{product['price']}**")
            st.markdown("[Click more...](#)")

    st.markdown("---")
    st.write("Total products: 50+")

# Function to create a progress line
def mark_light(timeline):
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    columns = [col1, col2, col3, col4]

    for i, stage in enumerate(timeline):
        with columns[i]:
            st.markdown(f"<div style='text-align: center;'>{stage['status']}</div>", unsafe_allow_html=True)
            transaction_color = "green" if stage["transaction"] else "gray"
            product_color = "green" if stage["product"] else "gray"
            delivered_color = "green" if stage["delivered"] else "gray"
            st.markdown(
                f"<div style='text-align: center;'>"
                f"<span style='color: {transaction_color};'>●</span>"
                f"<span style='color: {product_color};'>●</span>"
                f"<span style='color: {delivered_color};'>●</span>"
                f"</div>",
                unsafe_allow_html=True
            )
            st.markdown(f"<div style='text-align: center;'>TPD</div>", unsafe_allow_html=True)

def hist_list(history):
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    columns = [col1, col2, col3, col4]
    for i, stage in enumerate(history):
        with columns[i]:        
            st.markdown(f"""
            <div style="position: relative; margin-bottom: 10px;">
                <div style="color: green; cursor: pointer;">● {stage['date']}</div>
                <div style="padding-left: 20px; color: gray;">{stage['event']}</div>
                <div style="padding-left: 20px; color: gray;">{stage['deliver']}</div>
            </div>
            """, unsafe_allow_html=True)

df = data(110)
gdf = df.copy().sort_values(by=[
        'cust_id',
        'ret_price_off',
        # 'ret_duedate',
        'whs_price_off',
        'spl_price_off',
        ]).groupby([
            'cust_id',
            ],as_index=False).last()
col_list = [col for col in gdf.columns if col != 'date']
tdf = df.copy().drop_duplicates(subset=col_list,keep='first').reset_index(drop=True)

# History Page
def history_page():
    st.title("HISTORY")
    st.dataframe(df)
    
    timeline = []

    for i in range(len(gdf)):
        supplier  = {
            "status"      : gdf['spl_id'][i], 
            "transaction" : True if gdf['whs_paid'][i]==1 else False,
            "product"     : True if gdf['spl_fulfill'][i]==1 else False,
            "delivered"   : True if gdf['spl_dlvr'][i]==1 else False,
        }
        warehouse = {
            "status"      : gdf['whs_id'][i], 
            "transaction" : True if gdf['whs_paid'][i]==1 else False,
            "product"     : True if gdf['whs_fulfill'][i]==1 else False,
            "delivered"   : True if gdf['whs_dlvr'][i]==1 else False,
            }
        retailer  = {
            "status"      : gdf['ret_id'][i], 
            "transaction" : True if gdf['ret_paid'][i]==1 else False,
            "product"     : True if gdf['ret_fulfill'][i]==1 else False,
            "delivered"   : True if gdf['ret_dlvr'][i]==1 else False,
            }
        customer  = {
            "status"      : gdf['cust_id'][i],
            "transaction" : True if gdf['cust_paid'][i]==1 else False,
            "product"     : True if gdf['cust_fulfill'][i]==1 else False,
            "delivered"   : True if gdf['cust_dlvr'][i]==1 else False,
            }
        timeline.append([supplier,warehouse,retailer,customer])
            
        with st.expander(f"History {gdf['cust_req_id'][i]} ({gdf['cust_duedate'][i]})"):# ({gdf['cust_req_id'][i]})"):
            mark_light(timeline[i])

            st.markdown("<hr style='border: 1px solid gray;' />", unsafe_allow_html=True)
        
            hist_det = []
        
            for j in range(len(tdf[tdf['cust_id']==tdf['cust_id'][i]])):
                supplier  = {
                    "status"  : gdf['spl_id'][j], 
                    "date"    : tdf['date'][j] if tdf['whs_paid'][j]==1 else tdf['date'][j] if tdf['spl_dlvr'][j]==1 else tdf['date'][j], 
                    "event"   : "Paid" if tdf['whs_paid'][j]==1 else '-',
                    "deliver" : "Delivered" if tdf['spl_dlvr'][j]==1 else  '-'
                }
                warehouse  = {
                    "status" : gdf['whs_id'][j], 
                    "date"   : tdf['date'][j] if tdf['whs_paid'][j]==1 else tdf['date'][j] if tdf['spl_dlvr'][j]==1 else tdf['date'][j], 
                    "event"   : "Paid" if tdf['whs_paid'][j]==1 else '-',
                    "deliver" : "Delivered" if tdf['whs_dlvr'][j]==1 else  '-'
                }
                retailer  = {
                    "status" : gdf['ret_id'][j], 
                    "date"   : tdf['date'][j] if tdf['ret_paid'][j]==1 else tdf['date'][j] if tdf['ret_dlvr'][j]==1 else tdf['date'][j], 
                    "event"   : "Paid" if tdf['ret_paid'][j]==1 else '-',
                    "deliver" : "Delivered" if tdf['ret_dlvr'][j]==1 else  '-'
                }
                customer  = {
                    "status" : gdf['cust_id'][j], 
                    "date"   : tdf['date'][j] if tdf['cust_paid'][j]==1 else tdf['date'][j] if tdf['cust_dlvr'][j]==1 else tdf['date'][j], 
                    "event"   : "Paid" if tdf['cust_paid'][j]==1 else '-',
                    "deliver" : "Delivered" if tdf['cust_dlvr'][j]==1 else  '-'
                }
                hist_det.append([supplier,warehouse,retailer,customer])

                hist_list(hist_det[j])

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Product Listing", 
    "History", 
    "Visualisation"])

# Display the selected page
if page == "Product Listing":
    product_listing()
elif page == 'History':
    history_page()
else:
    visualization(gdf)
