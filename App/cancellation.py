def cancelinfo():
    import streamlit as st
    import matplotlib.pyplot as plt
    from dbfetch import fetchfrommysql
    # Table style
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
    col1,col2 = st.columns((0.5,0.5),gap="small")
    cancel_ride_by_customer = fetchfrommysql(
        "select count(*) cancelled_by_customer from ola_bookings where booking_status='Canceled by Customer';")
    cancel_ride_by_driver=fetchfrommysql("select count(*) cancelled_by_driver from ola_bookings where Canceled_Rides_by_Driver='Personal & Car related issue';")
    cancel_ride_count = fetchfrommysql("select Booking_Status,count(*) total from ola_bookings where Booking_Status<>'Success' group by Booking_Status;")
    incomplete_rides=fetchfrommysql("SELECT Incomplete_Rides_Reason,count(*) total FROM ola_bookings WHERE Incomplete_Rides ='Yes' group by Incomplete_Rides_Reason;")
    with col1:
        can_ride = cancel_ride_by_customer.loc[0,'cancelled_by_customer']
        st.write(f'#### Cancelled Ride by Customer')
        st.write(f'##### {format_indian_number(can_ride)}')
        can_by_driver = cancel_ride_by_driver.loc[0,'cancelled_by_driver']
        st.write(f'#### Cancelled Ride by Driver')
        st.write(f"##### Due to personal and car-related issue")
        st.write(f'##### {format_indian_number(can_by_driver)}')
        incomp_ride = incomplete_rides['total'].sum()
        st.write(f'#### Incomplete Rides')
        st.write(f'##### {format_indian_number(incomp_ride)}')
    with col2:
        fig,ax = plt.subplots(figsize=(5,3))
        ax.bar(cancel_ride_count['Booking_Status'],cancel_ride_count['total'],color='lightgreen',width=0.3)
        ax.set_title("Cancellation Category")
        ax.set_xlabel('Cancellation Type')
        ax.set_ylabel('Count')
        st.pyplot(fig)
    st.markdown("***")
    col1,col2 = st.columns((0.5,0.5),gap="small")
    with col1:
        st.write("### Incomplete Rides Reason")
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(incomplete_rides['Incomplete_Rides_Reason'], cancel_ride_count['total'], color='skyblue', width=0.4)
        ax.set_title("Incomplete Ride Reason")
        ax.set_xlabel('Reason')
        ax.set_ylabel('Count')
        st.pyplot(fig)
    with col2:
        customer_cancel_reason=fetchfrommysql("select distinct canceled_rides_by_customer as Reason  from ola_bookings where Booking_Status<>'Success' and canceled_rides_by_customer<>'NA' ;")
        st.write("### Customers Cancellation Reason")
        customer_cancel_reason['Serial'] = range(1, len(customer_cancel_reason) + 1)
        customer_cancel_reason.set_index('Serial', inplace=True)
        customer_cancel_reason.columns = ['Reason']
        st.table(customer_cancel_reason)
