def ratinginfo():
    import streamlit as st
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

    #Split the columns
    col1,col2 = st.columns((0.5,0.5),gap="large")
    with col1:
        minandmaxrating= fetchfrommysql(f"select vehicle_type type,`Vehicle Images` as img,min(Driver_ratings) min_driver_rating,max(Driver_Ratings) max_driver_rating, min(customer_rating) min_customer_rating,max(customer_rating) max_customer_rating from ola_bookings Group by vehicle_type,`Vehicle Images`;")
        st.markdown("#### Min and Max Customer & Driver Ratings")
        html = """
            <style>
        .styled-table {
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 16px;
        min-width: 400px;
        width: 100%;
        }
        .styled-table th, .styled-table td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: center;
         }
        .styled-table th {
        background-color: #71f0b7;
        font-weight: bold;
        }
        .styled-table img {
        width: 60px;
        height: auto;
        }
        </style>
        <table class="styled-table">
            <tr>
                <th style='width:120px'>Type</th>
                <th>Min Customer Rating</th>
                <th>Max Customer Rating</th>
                <th>Min Driver Rating</th>
                <th>Max Driver Rating</th>
            </tr>
        """
        for _,row in minandmaxrating.iterrows():
            html += f"""
        <tr>
            <td><img src="{row.loc['img']}" width="70"/>
            </br>
            <span style='font-weight: bold;text-align:center'>{row.loc['type']}</span>
            </td>
            <td><span style='font-weight: bold; color:green'>{row['min_customer_rating']}</span></td>
            <td><span style='font-weight: bold; color:green'>{row['max_customer_rating']}</span></td>
            <td><span style='font-weight: bold; color:green'>{row['min_driver_rating']}</span></td>
            <td><span style='font-weight: bold; color:green'>{row['max_driver_rating']}</span></td>                                                    
        </tr>
            """
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)
    with col2:
        avgrating= fetchfrommysql(f"SELECT Vehicle_Type as type,`Vehicle Images` as img, round(AVG(Customer_Rating),2) Customer_Rating,round(AVG(Driver_Ratings),2) as Driver_Rating FROM ola_bookings GROUP BY Vehicle_Type,`Vehicle Images`;")
        st.markdown("#### Average Customer & Driver Ratings")
        html = """
            <style>
        .styled-table {
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 16px;
        min-width: 400px;
        width: 100%;
        }
        .styled-table th, .styled-table td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: center;
         }
        .styled-table th {
        background-color: #71f0b7;
        font-weight: bold;
        }
        .styled-table img {
        width: 60px;
        height: auto;
        }
        </style>
        <table class="styled-table">
            <tr>
                <th style='width:120px'>Type</th>
                <th>Customer Rating</th>
                <th>Driver Rating</th>
            </tr>
        """
        for _,row in avgrating.iterrows():
            html += f"""
        <tr>
            <td><img src="{row.loc['img']}" width="70"/>
            </br>
            <span style='font-weight: bold;text-align:center'>{row.loc['type']}</span>
            </td>
            <td><span style='font-weight: bold; color:green'>{row.loc['Customer_Rating']}</span></td>
            <td><span style='font-weight: bold; color:green'>{row.loc['Driver_Rating']}</span></td>                                                    
        </tr>
            """
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)