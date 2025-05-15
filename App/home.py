def homeinfo():
    import streamlit as st
    import matplotlib.pyplot as plt
    from dbfetch import fetchfrommysql
    # Get the total Booking values
    booking_df = fetchfrommysql("select booking_status,count(*)  overall_booking from ola_bookings group by booking_status;")
    #Table style
    st.markdown("""
    <style>
    [data-testid="stTable"] {
        width: 400px;
        height: 200px;
        overflow-y: auto;
        background-color: #71f0b7;
        border-radius: 8px;  
        border:1px;
        font-size: 19px;
        color: black;
        font-color:black;
    }
    [data-testid="stTable"] thead th {
        font-size: 20px;
        text-align: left !important; 
        font-weight: bold;
        border:1px !important;
        border-color:black;
        color:black;
    }
    </style>
    """, unsafe_allow_html=True)
    # Format number
    def format_indian_number(number):
        num_str = str(int(number))[::-1]
        formatted_str = ""
        for i in range(len(num_str)):
            if i != 0 and (i == 3 or (i > 3 and (i - 1) % 2 == 0)):
                formatted_str += ','
            formatted_str += num_str[i]
        return formatted_str[::-1]

    #Split the columns
    success_booking = booking_df[booking_df['Booking_Status']=='Success']
    overall_booking = booking_df['overall_booking'].sum()
    col1, col2 = st.columns((0.4, 0.6), gap="large")
    with col1:
        st.write(f'#### All Bookings')
        st.write(f'##### {format_indian_number(overall_booking)}')
        st.markdown("***")
        st.write(f'#### Successful Bookings ')
        st.write(f'##### {format_indian_number(success_booking['overall_booking'])}')
    with col2:
        # Create the pie chart using Seaborn and Matplotlib
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.pie(booking_df['overall_booking'], labels=booking_df['Booking_Status'],
               autopct='%1.1f%%', startangle=120)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        # Set title
        ax.set_title('Category wise booking status')

        # Display the chart in Streamlit
        st.pyplot(fig)

    st.markdown("***")
    avg_ride=fetchfrommysql("SELECT Vehicle_Type as type,`Vehicle Images` as img, AVG(Ride_Distance)  as avg_distance FROM ola_bookings GROUP BY Vehicle_Type,`Vehicle Images`;")
    top5_customer_rids =fetchfrommysql("SELECT Customer_ID, COUNT(Booking_ID) as total_rides FROM ola_bookings GROUP BY Customer_ID ORDER BY total_rides DESC LIMIT 5;")
    colm1,colm2 = st.columns((0.5,0.5),gap="medium")
    with colm1:
        st.write("### Average Ride Distance")
        header_cols = st.columns([1 ,1])
        header_cols[0].write("**Type**")
        header_cols[1].write("**Average Distance**")
        for _, row in avg_ride.iterrows():
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(
                f"""
                <div style='border: 1px solid #ccc; padding: 10px; border-radius: 8px; margin-bottom: 10px;'>
                    <img src="{row['img']}" width="50" style="margin-right: 10px;" />
                    <span style='font-weight: bold;'>{row['type']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            with col2:
                st.markdown(
                    f"""
                    <span style='font-weight: bold; color:green'>{row['avg_distance']}</span>
                    """,unsafe_allow_html=True)
    with colm2:
        st.write("### Top 5 Customers")
        st.write("#### Booked highest number of ride")
        top5_customer_rids['Serial'] = range(1, len(top5_customer_rids) + 1)
        top5_customer_rids.set_index('Serial', inplace=True)
        top5_customer_rids.columns = ['Customer ID', 'Total Rides']
        st.table(top5_customer_rids)
