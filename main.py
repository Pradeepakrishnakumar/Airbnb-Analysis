import streamlit as st
from streamlit_option_menu import option_menu
# Multi page initialization
import home,explore,geo,visual

st.set_page_config(page_title='Airbnb Analysis using Streamlit and Plotly')
# Initialize a class
class Multiapp:
    def __init__(self):
        self.apps = []
    def add_app(self,title,function):
        self.apps.append({
            "title":title,
            "function":function
        })

    def run():
# Inputs for Side bar option 
        with st.sidebar:
            app = option_menu(
            menu_title='Airbnb',
            options=["Home", "Exploration", "Geovisualization", "Data_analyzation"],
            menu_icon='building',  # A general icon for Airbnb menu
            icons=['house-door', 'search', 'map', 'bar-chart'],
            default_index=0  # Start with the "Home" tab selected
    )
            
    # Function call for use other pages
        if app=='Home':
            home.app()
        elif app=='Exploration':
           explore.app()
        elif app=='Geovisualization':
            geo.app()
        elif app=='Data_analyzation':
            visual.app()

    run()