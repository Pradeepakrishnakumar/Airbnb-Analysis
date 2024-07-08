import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
file_path = r'C:\Users\Prem\OneDrive\Desktop\Guvi\capstone\air_bnb_data.csv'
df = pd.read_csv(file_path)

def app():
    st.header('Airbnb Data Visualization')

    # Selection option
    option = st.radio('Select your option', ('Price Analysis', 'Availability Analysis', 'Review Analysis', 'Query Analysis'),horizontal=True)

    # Price Analysis
    if option == 'Price Analysis':
        st.title("Price Analysis by Location")

        # Sidebar filters
        st.sidebar.header("Filter Options")
        neighbourhoods = st.sidebar.multiselect('Select Neighbourhood', df['nation'].unique())
        price_range = st.sidebar.slider('Select Price Range', min_value=int(df['prices'].min()), max_value=int(df['prices'].max()), value=(50, 300))

        # Filter data based on selections
        filtered_df = df[df['nation'].isin(neighbourhoods) & (df['prices'] >= price_range[0]) & (df['prices'] <= price_range[1])]

        # Display filtered data
        st.subheader("Filtered Data")
        st.write(filtered_df.head())

        # Get top 10 locations by number of listings
        top_locations = filtered_df['location'].value_counts().head(10).index
        filtered_top_locations_df = filtered_df[filtered_df['location'].isin(top_locations)]

        # Price Analysis by Top Locations
        st.subheader("Price Analysis by Top 10 Locations")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='location', y='prices', data=filtered_top_locations_df)
        plt.xticks(rotation=45)
        plt.title('Price Variation by Top 10 Locations')
        st.pyplot(plt)

    # Availability Analysis
    elif option == 'Availability Analysis':
        st.title("Availability Analysis by Season")

        # Sidebar filters
        st.sidebar.header("Filter Options")
        selected_country = st.sidebar.selectbox('Select Country', df['country_code'].unique())

        # Filter data based on selected country
        filtered_df = df[df['country_code'] == selected_country]

        # Display filtered data
        st.subheader("Filtered Data")
        st.write(filtered_df.head())

        # Aggregating availability by month
        availability_means = filtered_df[['availability30', 'availability60', 'availability90', 'availability365']].mean()

        # Plotting the availability data
        plt.figure(figsize=(12, 8))
        plt.bar(['Availability in Next 30 Days', 'Availability in Next 60 Days', 'Availability in Next 90 Days', 'Availability in Next 365 Days'], availability_means)
        plt.title(f'Average Availability in {selected_country}')
        plt.xlabel('Availability Period')
        plt.ylabel('Average Availability')
        st.pyplot(plt)

    if option == 'Review Analysis':
        st.title("Review Analysis")

        # Sidebar filters
        st.sidebar.header("Filter Options")
        selected_country = st.sidebar.selectbox('Select Country', df['country_code'].unique())

        # Filter data based on selected country
        filtered_df = df[df['country_code'] == selected_country]

        # Display filtered data
        st.subheader("Filtered Data")
        st.write(filtered_df.head())

        # Distribution of Ratings
        st.subheader("Distribution of Ratings")
        plt.figure(figsize=(10, 6))
        sns.histplot(filtered_df['rating'], bins=5, kde=True)
        plt.title('Distribution of Ratings')
        plt.xlabel('Rating')
        plt.ylabel('Count')
        st.pyplot(plt)

        # Average Cleanliness, Communication, and Value Ratings
        st.subheader("Average Ratings for Cleanliness, Communication, and Value")
        avg_ratings = filtered_df[['cleanliness', 'communication', 'value']].mean()
        plt.figure(figsize=(10, 6))
        sns.barplot(x=avg_ratings.index, y=avg_ratings.values)
        plt.title('Average Ratings for Cleanliness, Communication, and Value')
        plt.xlabel('Aspect')
        plt.ylabel('Average Rating')
        st.pyplot(plt)

    if option =="Query Analysis":
        

        query=st.selectbox(":violet[Select Your Query]",("Select the Query","Top 10 Hotels With Maximum Price",
                                                        "Top 10 Hotels with Minimum Price","Number of Hotels by Country",
                                                        "Average Price of Rooms by Country","Average Price of Room Types",
                                                        "Count of Room Types by Country","Hotels Count by Rating",
                                                        "Property type Distribution by country"))
       
        if query=="Select the Query":
            st.write("Your are getting the View about airbnb Analysis ")

        elif query=="Top 10 Hotels With Maximum Price":

            # Filter top 10 hotels with maximum price
            top_10_hotels = df.nlargest(10, 'prices')

            # Display filtered dataframe
            st.subheader('Top 10 Hotels')
            st.dataframe(top_10_hotels)

            # Plot the data
            fig, ax = plt.subplots()
            ax.barh(top_10_hotels['names'], top_10_hotels['prices'], color='skyblue')
            ax.set_xlabel('Price')
            ax.set_title('Top 10 Hotels with Maximum Price')
            plt.gca().invert_yaxis()  # To display the highest price hotel on top

            # Display the plot in Streamlit
            st.pyplot(fig)
            st.subheader('Insights')
            st.write('''Istanbul, Turkey:Hotel Name: "Center of Istanbul Sisli"
                     Location: Sisli District Minimum Price: 48,842 Turkish Lira 
                     Insight: This hotel is the most expensive in the dataset, reflecting its prime location in Istanbul's vibrant Sisli district, known for its shopping and cultural attractions.''')
        
        elif query=="Top 10 Hotels with Minimum Price":

            # Filter top 10 hotels with minimum price
            top_10_min_price = df.nsmallest(10, 'prices')

            
            # Display filtered dataframe
            st.header("Top 10 Hotels with Minimum Price")
            st.dataframe(top_10_min_price[['names', 'nation', 'prices']])


            

            # Plot top 10 hotels with minimum price
            st.header("Top 10 Hotels with Minimum Price - Plot")
            fig, ax = plt.subplots()
            sns.barplot(x='prices', y='names', data=top_10_min_price, ax=ax)
            ax.set_title("Top 10 Hotels with Minimum Price")
            ax.set_xlabel("Price")
            ax.set_ylabel("Hotel Name")
            st.pyplot(fig)
            st.subheader('Insights')
            st.write('''A hotel from Portugal Economy INN give the lowest price 50 currency we get insights This hotel offers the lowest price among the top 10, 
                making it an attractive option for budget travelers. Its central location adds to its appeal, providing easy access to the city’s main attractions.''')
        
        elif query=="Number of Hotels by Country":

            
            # Aggregate data by country
            country_counts = df['country_code'].value_counts().reset_index()
            country_counts.columns = ['country_code', 'number_of_hotels']

            # Display aggregated dataframe
            st.header("Number of Hotels by Country")
            st.dataframe(country_counts)

            # Plot number of hotels by country
            st.header("Number of Hotels by Country - Plot")
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.barplot(x='number_of_hotels', y='country_code', data=country_counts, ax=ax)
            ax.set_title("Number of Hotels by Country")
            ax.set_xlabel("Number of Hotels")
            ax.set_ylabel("Country")
            st.pyplot(fig)
            st.subheader('Insights:')
            st.write(''' Top Countries
                        The countries with the highest number of hotels indicate a robust hospitality infrastructure. These nations are well-equipped to accommodate large numbers of tourists, which is crucial for both domestic and international tourism.''')

                        
            st.subheader(" Tourism Hotspots:")
            st.write("-Countries leading in hotel counts are likely significant tourist destinations or major business hubs. This high hotel density suggests a strong demand for accommodations driven by tourism, business travel, and events.")

            st.subheader(" Strategic Planning for Businesses")
            st.write(" Market Entry: Companies looking to enter the hospitality market can identify potential regions for expansion based on hotel density. Countries with higher hotel counts might offer more opportunities but also face more competition.")
            st.subheader(" Customer Insights")
            st.write("For businesses focusing on customer acquisition and retention, knowing the countries with high hotel density helps in tailoring services to meet the specific needs of tourists from these regions. This could include language services, local cuisine options, and culturally relevant hospitality practices.")            

        elif query=="Average Price of Rooms by Country": 
            # Aggregate data by country to calculate the average price
            average_price_by_country = df.groupby('country_code')['prices'].mean().reset_index()
            average_price_by_country.columns = ['country_code', 'average_price']

            
            # Display aggregated dataframe
            st.header("Average Price of Rooms by Country")
            st.dataframe(average_price_by_country)

            # Plot average price of rooms by country
            st.header("Average Price of Rooms by Country - Plot")
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.barplot(x='average_price', y='country_code', data=average_price_by_country, ax=ax)
            ax.set_title("Average Price of Rooms by Country")
            ax.set_xlabel("Average Price")
            ax.set_ylabel("Country")
            st.pyplot(fig)
            st.subheader(' Insights: Affordability Analysis')
        
            st.write("Countries with the lowest average room prices represent more affordable travel destinations. This can attract budget-conscious travelers and boost tourism in these regions.")
            st.subheader("Market Positioning")
            st.write(" Businesses can use this data to position their offerings. Countries with lower average prices might need to focus on volume and attracting a larger number of guests, while countries with higher prices can target luxury and premium segments.")
            st.subheader(" Competitive Landscape")
            st.write("Understanding the average room prices helps in assessing the competitive landscape. Hotels in countries with higher average prices might offer more premium services and amenities, setting a benchmark for other hotels.")

        elif query=="Average Price of Room Types":
            
# Aggregate data by room type to calculate the average price
            average_price_by_roomtype = df.groupby('room_types')['prices'].mean().reset_index()
            average_price_by_roomtype.columns = ['room_types', 'average_price']

            # Display aggregated dataframe
            st.header("Average Price of Room Types")
            st.dataframe(average_price_by_roomtype)

            # Plot average price of room types
            st.header("Average Price of Room Types - Plot")
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.barplot(x='average_price', y='room_types', data=average_price_by_roomtype, ax=ax)
            ax.set_title("Average Price of Room Types")
            ax.set_xlabel("Average Price")
            ax.set_ylabel("Room Type")
            st.pyplot(fig)
            st.subheader("Insights: Affordability Analysis")
            st.write("- Countries with the lowest average room prices are attractive destinations for budget-conscious travelers. These countries can leverage their affordability to boost tourism, attracting a larger volume of tourists who seek value for money.")
            st.subheader("Promotion and Marketing")
            st.write("Tourism boards and travel agencies can promote destinations with lower average prices to budget travelers and backpackers, potentially increasing tourist footfall and spending in these regions. Highlighting the affordability and unique experiences available in these destinations can attract a broader audience.")

        elif query=="Count of Room Types by Country":    

            # Aggregate data to count room types by country
            roomtype_count_by_country = df.groupby(['country_code', 'room_types']).size().reset_index(name='room_type_count')

           
            # Display aggregated dataframe
            st.header("Count of Room Types by Country")
            st.dataframe(roomtype_count_by_country)

            # Plot count of room types by country
            st.header("Count of Room Types by Country - Plot")
            fig, ax = plt.subplots(figsize=(12, 10))
            sns.barplot(x='room_type_count', y='country_code', hue='room_types', data=roomtype_count_by_country, ax=ax)
            ax.set_title("Count of Room Types by Country")
            ax.set_xlabel("Count")
            ax.set_ylabel("Country")
            ax.legend(title='Room Types', loc='best')
            st.pyplot(fig)
            st.subheader(" Insights: Room Type Distribution")
            st.write("Understanding the distribution of room types across different countries can help in identifying market trends and preferences. Countries with a higher count of specific room types might indicate a demand for those types, guiding hotels in their room offerings.")
            st.subheader(" Strategic Planning for Hotels")
            st.write("Hotels can use this information to align their room offerings with market demand. For instance, if a country shows a high count of budget rooms, hotels might focus on offering more affordable options. Conversely, a high count of luxury rooms indicates a market for premium services.")
        
        elif query=="Property type Distribution by country":
            from ast import literal_eval 


            def safe_eval(x):
                try:
                    return literal_eval(x)
                except (ValueError, SyntaxError):
                    return x  # If literal_eval fails, return the original value

            df['property_types'] = df['property_types'].apply(safe_eval)

            # Aggregate data to count property types by country
            property_types_df = df.explode('property_types')
            property_types_by_country = property_types_df.groupby(['country_code', 'property_types']).size().reset_index(name='property_type_count')

            # Streamlit App
            st.title("Airbnb Analysis")

            # Display aggregated dataframe
            st.header("Property Type Distribution by Country")
            st.dataframe(property_types_by_country)

            # Plot property type distribution by country
            st.header("Property Type Distribution by Country - Plot")
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.barplot(x='property_type_count', y='country_code', hue='property_types', data=property_types_by_country, ax=ax)
            ax.set_title("Property Type Distribution by Country")
            ax.set_xlabel("Count")
            ax.set_ylabel("Country")
            st.pyplot(fig)

              
           
            
            st.subheader('Insights')
            st.write('''The most common property types across these countries are Apartments, reflecting the popularity 
                            of urban living spaces and providing comfortable accommodation options for travelers.''')
                    
            st.write('''Other prevalent property types include Houses, Townhouses, and Condominiums, offering diverse choices 
                            for different preferences and travel styles.''')
                    
            st.write(''' Additionally, unique accommodations such as Lofts, Serviced Apartments, and Boutique Hotels cater to travelers 
                            seeking distinctive and memorable lodging experiences.''')
                    
            st.write('''Overall, the availability of a wide range of property types highlights the diversity and richness of accommodation 
                                options in these countries, accommodating various traveler needs and preferences.''')
                    
        elif query=="Hotels Count by Rating":   
            # Aggregate data to count hotels by rating
            hotels_by_rating = df['rating'].value_counts().reset_index()
            hotels_by_rating.columns = ['rating', 'hotel_count']
            hotels_by_rating = hotels_by_rating.sort_values(by='rating')

            
            # Display aggregated dataframe
            st.header("Hotels Count by Rating")
            st.dataframe(hotels_by_rating)

            # Plot count of hotels by rating
            st.header("Hotels Count by Rating - Plot")
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.barplot(x='rating', y='hotel_count', data=hotels_by_rating, ax=ax)
            ax.set_title("Count of Hotels by Rating")
            ax.set_xlabel("Rating")
            ax.set_ylabel("Hotel Count")
            st.pyplot(fig) 
            st.subheader('Insights')
            st.write(''' Distribution of Ratings: The majority of Airbnb listings have ratings ranging from 90 to 100, with the highest concentration around the 100 rating mark.''')
                    
            st.write('''Highly Rated Listings: A significant number of listings receive ratings of 95 and above, indicating a high level of satisfaction among guests.''')
                    
            st.write('''Variety of Ratings: While most listings have high ratings, there is also diversity in ratings across the platform, with some listings receiving ratings below 80.''')
                    
            st.write(''' Room for Improvement: Despite the overall positive trend, there are opportunities for improvement in some listings, 
                            as reflected in the lower ratings received by a small percentage of accommodations.''')
                    






