import streamlit as st
import pandas as pd

# Read the CSV file into a DataFrame
file_path = r'C:\Users\Prem\OneDrive\Desktop\Guvi\capstone\air_bnb_data.csv'
df = pd.read_csv(file_path)

def app():
    st.title(' Airbnb Explorer')

    # Split the page into columns for better layout
    
    st.write(' ')
    st.subheader(' Welcome to the Airbnb Explorer!')
    st.markdown(' Start your journey with us.')

        # Select country and street
    df_countries = df['nation'].drop_duplicates().reset_index(drop=True)
    selected_country = st.selectbox("Search destinations", options=df_countries.tolist())

    if selected_country:
        df_streets = df[df['nation'] == selected_country]['street'].drop_duplicates().reset_index(drop=True)
        selected_street = st.selectbox("Select Street", options=df_streets.tolist())

        if selected_street:
            df_hotels = df[(df['nation'] == selected_country) & (df['street'] == selected_street)]['names'].drop_duplicates().reset_index(drop=True)
            selected_hotel = st.selectbox('Select Hotel', options=df_hotels.tolist())

            if selected_hotel:
                st.write("Selected Accommodation:", f"<span style='color:#F8CD47'>{selected_hotel}</span>", unsafe_allow_html=True)

                if st.button('Click for Details'):
                        # Filter the DataFrame based on the selected hotel
                    df_filtered = df[df['names'] == selected_hotel]

                        # Display detailed information
                    if not df_filtered.empty:
                        details = df_filtered.iloc[0]  # Assuming only one row per hotel is selected
                        st.subheader(f"Details for {selected_hotel}")
                        st.markdown(f"**Website Url:** {details['url']}")
                        st.markdown(f"**Country:** {details['nation']}")
                        st.markdown(f"**Description:** {details['descriptions']}")
                        st.markdown(f"**Price in $:** {details['prices']}")
                        st.markdown(f"**Total Reviews:** {details['reviews']}")
                        st.markdown(f"**Overall Score:** {details['reviews']} | **Rating:** {details['rating']}")
                        
                        # Additional details as needed
                        st.subheader('Room Details')
                        st.markdown(f"**Property Type:** {details['property_types']}")
                        st.markdown(f"**Room Type:** {details['room_types']}")
                        
                        st.subheader('Host Details')
                        st.markdown(f"**Host Name:** {details['name']}")
                        st.markdown(f"**Host Location:** {details['location']}")
                        

