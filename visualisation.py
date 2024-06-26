import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

def visualization(df):
    # Visualization 1: Trend Line
    dateReq = df.groupby('cust_ordDate',as_index=False)[[
        'cust_quan_req',
        'ret_quan_avail',
        'whs_quan_avail',
        'spl_quan_avail'
        ]].sum()

    fig1 = make_subplots(rows=2, cols=2,
                        subplot_titles=('cust_quan_req','ret_quan_avail',
                                        'whs_quan_avail','spl_quan_avail'))

    fig1.add_trace(go.Scatter(
        x=dateReq['cust_ordDate'],y=dateReq['cust_quan_req'],
        mode='lines+markers',name='Customer Request'),
        row=1, col=1)
    fig1.add_trace(go.Scatter(
        x=dateReq['cust_ordDate'],y=dateReq['ret_quan_avail'],
        mode='lines+markers',name='Retailer Quantity Availability'),
        row=1, col=2)
    fig1.add_trace(go.Scatter(
        x=dateReq['cust_ordDate'],y=dateReq['whs_quan_avail'],
        mode='lines+markers',name='Warehouse Quantity Availability'),
        row=2, col=1)
    fig1.add_trace(go.Scatter(
        x=dateReq['cust_ordDate'],y=dateReq['spl_quan_avail'],
        mode='lines+markers',name='Supplier Quantity Availability'),
        row=2, col=2)

    fig1.update_layout(
        title='Trend Line',
        xaxis_title='Date',
        yaxis_title='Value'
    )

    # Visualization 2: Product Request Fulfillment Share
    pie = pd.DataFrame({'label':['Retailer Offer','Warehouse Offer','Supplier Offer'],
                    'sum':[df.ret_fulfill.sum(),df.whs_fulfill.sum(),df.spl_fulfill.sum()]})

    fig2 = go.Figure(data=[go.Pie(
        labels=pie['label'],
        values=pie['sum'])])

    fig2.update_layout(
        title='Product Request Fulfillment Share'
    )


    # Visualization 3: Product Share
    barProd = df['prod_name'].value_counts().reset_index()
    barProd.columns = ['prod_name', 'count']

    fig3 = go.Figure(data=[go.Bar(
        labels=barProd['prod_name'],
        values=barProd['count'])])

    fig3.update_layout(
        title='Product Frequency',
        xaxis_title='Product Name',
        yaxis_title='Count',
        template='plotly_white'
    )

    fig3.update_layout(
        title='Product Frequency')

    # Visualization 4: Customer and Supply Fulfillments
    # df['month'] = df['date'].dt.to_period('M')
    ff = df.groupby('month', as_index=False)[['cust_fulfill', 'ret_fulfill', 'whs_fulfill', 'spl_fulfill']].sum()
    ff['Shortage'] = ff['cust_fulfill'] - ff[['ret_fulfill', 'whs_fulfill', 'spl_fulfill']].sum(axis=1)

    fig4 = make_subplots(rows=2, cols=1,
                         subplot_titles=('Customer Fulfill',
                                         'Stacked Fulfillments'))

    fig4.add_trace(
        go.Bar(name='Customer Fulfill', y=ff['cust_fulfill'],
               x=ff['month'].astype(str)), row=1, col=1)

    fig4.add_trace(go.Bar(name='Retail Fulfill', y=ff['ret_fulfill'],
                          x=ff['month'].astype(str)), row=2, col=1)
    fig4.add_trace(go.Bar(name='Warehouse Fulfill', y=ff['whs_fulfill'],
                          x=ff['month'].astype(str), base=ff['ret_fulfill']),
                   row=2, col=1)
    fig4.add_trace(go.Bar(name='Supplier Fulfill', y=ff['spl_fulfill'],
                          x=ff['month'].astype(str),
                          base=ff['ret_fulfill'] + ff['whs_fulfill']),
                   row=2, col=1)
    fig4.add_trace(go.Bar(name='Shortage', y=ff['Shortage'],
                          x=ff['month'].astype(str),
                          base=ff['ret_fulfill'] + ff['whs_fulfill'] + ff['spl_fulfill']),
                   row=2, col=1)

    fig4.update_layout(
        barmode='stack',
        title='Customer and Supply Fulfillments',
        xaxis_title='month',
        yaxis_title='Values'
    )


    # Visualization 5: Price and Quantity Range of Each Component
    custPri = df[['cust_quan_req','cust_price_ord']].copy().rename(columns={'cust_budg_ord':'Price','cust_quan_req':'Quant'})
    custPri['Type'] = 'customer budget'
    retPri = df[['ret_quan_avail','ret_price_ord']].copy().rename(columns={'ret_price_ord':'Price','ret_quan_avail':'Quant'})
    retPri['Type'] = 'retailer price'
    whsPri = df[['whs_quan_avail','whs_price_ord']].copy().rename(columns={'whs_price_ord':'Price','whs_quan_avail':'Quant'})
    whsPri['Type'] = 'warehouse price'
    splPri = df[['spl_quan_avail','spl_price_off']].copy().rename(columns={'spl_price_off':'Price','spl_quan_avail':'Quant'})
    splPri['Type'] = 'supplier price'
    price = pd.concat([custPri,retPri,whsPri,splPri])

    fig5 = go.Figure()

    fig5 = make_subplots(rows=2, cols=1,
                        subplot_titles=('Price Range of Each Components',
                                        'Quantity Range of Each Components'))

    fig5.add_trace(
        go.Box(name='Count Range Each month', x=price['Price'],
            y=price['Type'], orientation='h'), row=1, col=1)
    fig5.add_trace(
        go.Box(name='Price Range Each month', x=price['Quant'],
            y=price['Type'], orientation='h'), row=2, col=1)

    fig5.update_layout(
        title='PRICE AND QUANTITY RANGE OF EACH COMPONENTS',
        xaxis_title='Values',
        yaxis_title='Components',
        width=1000
        )

    # Display the visualizations in Streamlit
    st.title("Visualizations")

    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.plotly_chart(fig5, use_container_width=True)
