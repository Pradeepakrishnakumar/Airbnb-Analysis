import pandas as pd
import plotly.express as px
import folium
import streamlit as st

# Read the CSV file into a DataFrame
file_path = r'C:\Users\Prem\OneDrive\Desktop\Guvi\capstone\air_bnb_data.csv'
df = pd.read_csv(file_path)

def app():
    st.subheader(":red[Explore Accommodation by Country]")

    # Get the unique list of countries from the DataFrame
    df_Country = df['nation'].drop_duplicates().reset_index(drop=True)
    selected_country = st.selectbox("Select Country", options=df_Country.tolist())
    

    if selected_country:
        on = st.checkbox('Switch to view')

        if on:
            # Filter the DataFrame based on the selected country
            df_filtered = df[df['nation'] == selected_country]

            if not df_filtered.empty:
                # Create a map centered around the average coordinates
                map_center = [df_filtered['latitude'].mean(), df_filtered['longitude'].mean()]
                airbnb_map = folium.Map(location=map_center, zoom_start=12)

                # Add listings to the map
                for idx, row in df_filtered.iterrows():
                    folium.Marker(
                        location=[row['latitude'], row['longitude']],
                        popup=f"Price: {row['prices']}\nRating: {row['rating']}",
                        icon=folium.Icon(color='blue' if row['prices'] < 100 else 'red')
                    ).add_to(airbnb_map)

            
                # Ensure columns are in float type for Plotly
                df_filtered[['longitude', 'latitude', 'prices']] = df_filtered[['longitude', 'latitude', 'prices']].astype('float')

                # Create Plotly scatter mapbox
                fig = px.scatter_mapbox(df_filtered, lat="latitude", lon="longitude", color="prices",
                                        zoom=10, hover_name='names',
                                        color_continuous_scale=px.colors.colorbrewer.Blues_r)
                fig.update_layout(mapbox_style="open-street-map")
                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                
                # Display the Plotly map in Streamlit
                st.plotly_chart(fig, use_container_width=True)



