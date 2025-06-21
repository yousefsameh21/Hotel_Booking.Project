import pandas as pd
import seaborn as sns
import plotly.express as px
import numpy as np
import streamlit as st
# showing  data in streamlit
df=pd.read_csv('hotel_project_cleaned.csv',index_col=0)
page=st.sidebar.radio('Pages',['Home','Introduction','Uni-Variate Analysis', 'Bi-Variate Analysis', 'Multi-Variate Analysis'])
if page=='Home':
    st.markdown("<h1 style='text-align: center; color: Silver; '>Hotel Booking Project</h1>", unsafe_allow_html=True)
    st.image('https://5.imimg.com/data5/LU/XS/MY-33831739/hotel-bookings.jpg')
elif page =='Introduction':
    st.header('Hotel Booking Dataset')
    st.dataframe(df.head(10))
    st.title("Table of Variables")

    column_info = [
    {"Attribute": "hotel", "Description": "Resort or City hotel"},
    {"Attribute": "is_canceled lead_time", "Description": "Booking canceled (1) or not (0)"},
    {"Attribute": "arrival_date_year", "Description": "Year of arrival"},
    {"Attribute": "arrival_date_month", "Description": "Month of arrival (January to December)"},
    {"Attribute": "arrival_date_week_number", "Description": "Week number of the year"},
    {"Attribute": "arrival_date_day_of_month", "Description": "Day of the month"},
    {"Attribute": "stays_in_weekend_nights", "Description": "Weekend nights stayed (Sat/Sun)"},
    {"Attribute": "stays_in_week_nights", "Description": "Week nights stayed (Mon–Fri)"},
    {"Attribute": "adults", "Description": "Number of adults"},
    {"Attribute": "children", "Description": "Number of children"},
    {"Attribute": "babies", "Description": "Number of babies"},
    {"Attribute": "meal", "Description": "Meal type (e.g., BB – Bed & Breakfast)"},
    {"Attribute": "country", "Description": "Country of origin"},
    {"Attribute": "market_segment", "Description": "Market segment (TA = Travel Agents, TO = Tour Operators)"},
    {"Attribute": "distribution_channel", "Description": "Channel used to book (TA, TO, etc.)"},
    {"Attribute": "is_repeated_guest", "Description": "Is the guest repeated (1) or not (0)"},
    {"Attribute": "previous_cancellations", "Description": "Number of previous canceled bookings"},
    {"Attribute": "previous_bookings_not_canceled", "Description": "Number of previous non-canceled bookings"},
    {"Attribute": "reserved_room_type", "Description": "Code of reserved room"},
    {"Attribute": "assigned_room_type", "Description": "Code of assigned room"},
    {"Attribute": "booking_changes", "Description": "Number of booking changes"},
    {"Attribute": "deposit_type", "Description": "Deposit type (No Deposit, Refundable, Non Refund)"},
    {"Attribute": "agent", "Description": "Travel agency ID"},
    {"Attribute": "company", "Description": "Company ID"},
    {"Attribute": "days_in_waiting_list", "Description": "Days booking waited before confirmation"},
    {"Attribute": "customer_type", "Description": "Booking type (Transient, Group, etc.)"},
    {"Attribute": "adr", "Description": "Average Daily Rate"},
    {"Attribute": "required_car_parking_spaces", "Description": "Required parking spaces"},
    {"Attribute": "total_of_special_requests", "Description": "Number of special requests"},
    {"Attribute": "reservation_status", "Description": "Final booking status (Check-Out, No-Show, Canceled)"},
    {"Attribute": "reservation_status_date", "Description": "Date when final status was set"},
]

    df_info = pd.DataFrame(column_info)

    st.dataframe(df_info, use_container_width=True)
elif page =='Uni-Variate Analysis':
    st.write('#### Combare between number of  hotels ')
    df_hot=df['hotel'].value_counts().reset_index()
    st.plotly_chart(px.bar(df_hot,x='hotel',y='count',  title='Number  of hotels '))
    chart_type=st.selectbox('Choose Visualization chart', ['histogram', 'bar']) 
    column=st.selectbox('choose  cloumn',df.columns)
    df_columns=df[column].value_counts().reset_index()
    
    if chart_type=='histogram':
        st.plotly_chart(px.histogram(data_frame=df_columns,x=column,y='count',template = 'plotly_dark'))
    else:
        st.plotly_chart(px.bar(df_columns,x=column,y='count',template = 'plotly_dark'))
elif page =='Bi-Variate Analysis':
    st.write('### Showing Reservation Status in Different Hotels')
    df_Reservation_Statu=df.groupby(['hotel','is_canceled'])['is_canceled'].count().sort_values(ascending=False).reset_index(name='count')
    df_Reservation_Statu['is_canceled'] = df_Reservation_Statu['is_canceled'].map({0: 'Not Canceled', 1: 'Canceled'})
    st.plotly_chart(px.bar(df_Reservation_Statu,x='hotel',y='count',color='is_canceled',title=' hotel vs is_canceled',text='count',barmode='group'))
    st.write('### What is the percentage of booking for each year?')
    df_notcansel=df[df['is_canceled']==0]
    df_by=df_notcansel.groupby('hotel')['year'].value_counts().sort_values(ascending=False).reset_index(name='count')
    df_by['percentage (%)'] = round(100 * df_by['count'] / df_by.groupby('hotel')['count'].transform('sum'),2)
    st.plotly_chart(px.bar(df_by,x='year',y='percentage (%)',color='hotel',barmode='group',text='percentage (%)',title='arrival_date_year by Hotel\n',template = 'plotly_dark'))
    st.write('### From which country most guests come?')
    df_notcansel=df[df['is_canceled']==0]
    df_country=df_notcansel['country'].value_counts().reset_index(name='count').head(10)
    df_country['percentage (%)']=round(100* df_country['count']  / df_country['count'].sum(),2)
    st.plotly_chart(px.bar(df_country,x='country',y='percentage (%)',title='guests from each country',text='percentage (%)',template = 'plotly_dark').update_traces(texttemplate='%{text:.2f}%', textposition='outside'))
    categorical_columns=st.selectbox('choose  cloumn',['hotel', 'meal', 'country', 'market_segment', 'distribution_channel', 'reserved_room_type', 'assigned_room_type', 'customer_type', 'reservation_status'])
    df_column=df.groupby([categorical_columns, 'is_canceled']).size().reset_index(name='count')
    df_column['is_canceled'] = df_column['is_canceled'].map({0: 'Not Canceled', 1: 'Canceled'})
    st.plotly_chart(px.bar(df_column,x=categorical_columns,y='count',color='is_canceled',text='count',barmode='group',title=f'Booking Cancellation by {categorical_columns}',template='plotly_dark'))
else :
    st.write('##### Which are the most busy month?')
    redf_resort = df[(df['hotel']=='Resort Hotel') & (df['is_canceled']==0)]
    data_city = df[(df['hotel']=='City Hotel') & (df['is_canceled']==0)]
    rush_resort=redf_resort['month'].value_counts().reset_index()
    rush_city=data_city['month'].value_counts().reset_index()
    final_rush=rush_resort.merge(rush_city,on='month')
    final_rush.columns=['month','no_of_guests_in_resort','no_of_guests_city']
    final_rush = final_rush.sort_values('month')
    st.plotly_chart(px.line(final_rush,x='month',y=['no_of_guests_in_resort', 'no_of_guests_city'],title='Number of Guests Over Months',labels={'month': 'Month', 'value': 'Number of Guests', 'variable': 'Guest Type'}))
    st.write('### Cancellation Rate by Market Segment and Hotel')
    df_crbmsh=df.groupby(['market_segment','hotel'])['is_canceled'].agg(
    total_bookings='count',
    canceled_bookings='sum').reset_index()
    df_crbmsh['cancellation_rate (%)'] = round(100 * df_crbmsh['canceled_bookings'] / df_crbmsh['total_bookings'], 2)
    st.plotly_chart(px.bar( df_crbmsh,x='market_segment',y='cancellation_rate (%)',color='hotel',barmode='group', text='cancellation_rate (%)', title='Cancellation Rate by Market Segment and Hotel', template='plotly_dark'))
    st.write('### Heatmap for Cancellation Rate by Market Segment and Hotel')
    st.plotly_chart(px.density_heatmap(df_crbmsh,x='hotel',y='market_segment',z='cancellation_rate (%)'))
    
