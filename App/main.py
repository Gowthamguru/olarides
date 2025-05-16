#Import the important libraries
import streamlit as st
from streamlit_option_menu import option_menu
import home
import cancellation
import ratings
import payment
from dbfetch import fetchfrommysql

# Set the Page configuration
st.set_page_config(
    page_title="Ola Ride insights",
    layout="wide",
    initial_sidebar_state="expanded")
st.markdown("""
    <style>
    .stApp {
     background-color: #defaf0;
    }
    </style>
    """,unsafe_allow_html=True)

# Sidebar menu

# Inject custom CSS for sidebar width
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        width: 270px !important;      /* sidebar width */
    }
    [data-testid="stSidebar"] > div:first-child {
        width: 270px !important;      /* actual content area width */
    }
    </style>
""", unsafe_allow_html=True)


# Sidebar menu
with st.sidebar:
    st.sidebar.image("./Images/Ola_Cabs_logo.svg")
    selected = option_menu(None, ["Home", 'Ratings','Cancellation','Payments'],
                           icons=['taxi-front-fill', 'star-half','x-octagon-fill','credit-card-2-front-fill'], menu_icon="cast", default_index=0,
    styles = {
        "container": {"padding": "2!important", "background-color": "#defaf0"},
        "icon": {"color": "black", "font-size": "16px"},
        "nav-link": {"color": "black", "font-size": "16px", "text-align": "left", "margin": "0px",
                     "--hover-color": "#83f7d8"},
        "nav-link-selected": {"background-color": "#83f7d8"}, }
    )

#Define the sidebar menu select event
if selected =="Home":
    home.homeinfo()
if selected == "Cancellation":
    cancellation.cancelinfo()
if selected == "Ratings":
    ratings.ratinginfo()
if selected =="Payments":
    payment.paymentinfo()