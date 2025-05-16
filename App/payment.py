def paymentinfo():
    import streamlit as st
    import matplotlib.pyplot as plt
    import seaborn as sns
    from babel.numbers import format_currency
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
    # Format amount
    def format_amount(amount):
        if amount >= 1e7:
            amount_in_crore = amount / 1e7
            formatted_amount = format_currency(amount_in_crore, 'INR', locale='en_IN')
            return f"{formatted_amount} Cr"
        elif amount >= 1e5:
            amount_in_lakhs = amount / 1e5
            formatted_amount = format_currency(amount_in_lakhs, 'INR', locale='en_IN')
            return f"{formatted_amount} L"
        elif amount >= 1e3:
            amount_in_thousand = amount / 1e3
            formatted_amount = format_currency(amount_in_thousand, 'INR', locale='en_IN')
            return f"{formatted_amount} K"
        else:
            formatted_amount = format_currency(amount, 'INR', locale='en_IN')
            return format_indian_number(formatted_amount)

    # Split the columns
    col1, col2 = st.columns((0.5, 0.5), gap="large")
    with col1:
        booking = fetchfrommysql(
            f"select sum(Booking_value) total from ola_bookings where booking_status='Success';")
        bookingtotal = booking.loc[0,'total']
        st.write(f'#### Total Booking value of Success Bookings')
        st.write(f'##### {format_amount(bookingtotal)}')
        st.markdown("***")
        top5bookingvalue=fetchfrommysql("SELECT Customer_ID, Booking_value as total_amount FROM ola_bookings  ORDER BY Booking_value DESC LIMIT 5;")
        st.write("### Top 5 Booking Value")
        top5bookingvalue['Serial'] = range(1, len(top5bookingvalue) + 1)
        top5bookingvalue.set_index('Serial', inplace=True)
        top5bookingvalue['total_amount'] = top5bookingvalue['total_amount'].apply(format_amount)
        top5bookingvalue.columns = ['Customer ID','Booking Value']
        st.table(top5bookingvalue)
    with col2:
        paymentmethodval = fetchfrommysql(
            "SELECT payment_method, sum(Booking_value) as total_amount FROM ola_bookings  group by payment_method;")
        st.write("### Payment Method wise Booking Value")
        paymentmethodval['Serial'] = range(1, len(top5bookingvalue) + 1)
        paymentmethodval.set_index('Serial', inplace=True)
        paymentmethodval['total_amount'] =paymentmethodval['total_amount'].apply(format_amount)
        paymentmethodval.columns = ['Payment Method', 'total_amount']
        st.table(paymentmethodval)

    st.markdown("***")
    rideavg = fetchfrommysql("select  Ride_Distance,avg(Booking_value) value from ola_bookings where booking_status='Success' group by ride_distance order by ride_distance;")

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 4))

    # Create a Seaborn line plot
    sns.lineplot(data=rideavg, x='Ride_Distance', y='value', marker='o', ax=ax)

    # Set chart labels
    ax.set_title("Average Booking value based on Distance")
    ax.set_ylabel("Amount")
    ax.set_xlabel("Distance")

    # Display in Streamlit
    st.pyplot(fig)