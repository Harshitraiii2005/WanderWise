import streamlit as st
import pandas as pd
import pickle
import requests
import folium
from streamlit_folium import st_folium
from PIL import Image

# Define API keys
SERP_API_KEY = "f1b6771dbf538c0e5600244226a36f79b7f73fb3ca59e017e2d94de8c1b87460"
UNSPLASH_API_KEY = "S5zKvtYOMACmjZjad0NhAeZ4rux-rCTsRBYqmq7gAV4"
PIXABAY_API_KEY = "46949974-4f2935be7915a7eefe4a13846"
WEATHER_API_KEY = "a9451312692f41cda5d134952240611"

# Load the DataFrame from the pickle file
try:
    with open("new_df (4).pkl", "rb") as file:
        new_df = pickle.load(file)
except FileNotFoundError:
    st.error("The data file 'new_df.pkl' was not found. Please ensure the file is in the correct location.")
    st.stop()

# Cache for storing images to reduce API calls
image_cache = {}



# Function to fetch an image using multiple APIs with fallback
def fetch_image(query):
    if query in image_cache:
        return image_cache[query]

    api_sources = [
        {
            "name": "Pixabay",
            "url": f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}&image_type=photo",
            "extract_func": lambda data: data['hits'][0]['webformatURL'] if 'hits' in data and data['hits'] else None
        },
        {
            "name": "Unsplash",
            "url": f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_API_KEY}",
            "extract_func": lambda data: data['results'][0]['urls']['small'] if 'results' in data and data['results'] else None
        },
        {
            "name": "SERP",
            "url": f"https://serpapi.com/search.json?q={query}&tbm=isch&api_key={SERP_API_KEY}",
            "extract_func": lambda data: data['images_results'][0]['thumbnail'] if 'images_results' in data else None,
            "rate_limit_wait": 120
        },
    ]

    for api in api_sources:
        try:
            response = requests.get(api["url"])
            if response.status_code == 200:
                data = response.json()
                image_url = api["extract_func"](data)
                if image_url:
                    image_cache[query] = image_url
                    return image_url
            elif response.status_code == 429 and api["name"] == "SERP":
                st.warning(f"{api['name']} API rate limit exceeded. No reattempt until after other sources.")
                time.sleep(api.get("rate_limit_wait", 60))
                break
        except Exception as e:
            st.error(f"Error with {api['name']} API: {e}")
            continue

    return None

# Function to fetch weather data
def fetch_weather(location):
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        if 'current' in weather_data:
            temp_c = weather_data['current']['temp_c']
            condition = weather_data['current']['condition']['text']
            icon = weather_data['current']['condition']['icon']
            humidity = weather_data['current']['humidity']
            wind_kph = weather_data['current']['wind_kph']
            return temp_c, condition, icon, humidity, wind_kph
    return None

# Main App Interface
st.title("🌎 Wander Wise")
st.markdown("""
    ### Discover Your Next Destination
    **Explore** the best tourist attractions across India with real-time weather updates, beautiful images, and travel tips!
    """)

# Display an intro image at the top
intro_image = Image.open("C:\\Users\\admin\\Pictures\\dc0475ea337cd67a214ddcf0e174a9bb.jpg")
st.image(intro_image, use_column_width=True)

# Dropdown for selecting the state
state_name = st.selectbox("Select a State:", sorted(new_df['State'].dropna().unique()))

# Function to retrieve attractions
def get_attractions(state_name):
    attractions = new_df[new_df['State'].str.lower() == state_name.lower()]
    return attractions

# Display the map if a state name is selected
if state_name:
    attractions_df = get_attractions(state_name)

    if attractions_df.empty:
        st.warning(f"No attractions found for the state: {state_name}. Please check the name and try again.")
    else:
        st.subheader(f"✨ Tourist Attractions in {state_name.title()} ✨")

        # Create and display a map centered on India
        initial_location = [20.5937, 78.9629]
        map_attractions = folium.Map(location=initial_location, zoom_start=6)

        # Add markers for each attraction
        for _, row in attractions_df.iterrows():
            info_parts = {part.split(": ")[0].strip(): part.split(": ")[1].strip() for part in row['Info'].split(", ") if ": " in part}
            attraction_name = info_parts.get("Tourist Attraction", "N/A")
            latitude = row.get("Latitude")
            longitude = row.get("Longitude")

            if latitude and longitude:
                folium.Marker(
                    location=[latitude, longitude],
                    popup=attraction_name,
                    tooltip=attraction_name
                ).add_to(map_attractions)

        # Display the map
        st_folium(map_attractions, width=700, height=500)

        # "Show More" button with attractions below map
        if st.button("Show The Attractions....😍"):
            for _, row in attractions_df.iterrows():
                info_parts = {part.split(": ")[0].strip(): part.split(": ")[1].strip() for part in row['Info'].split(", ") if ": " in part}
                attraction_name = info_parts.get("Tourist Attraction", "N/A")

                # Attraction info card
                st.markdown(f"""
                    <div class="card">
                        <h3 class="attraction-title">{attraction_name}</h3>
                        <p class="info-section">Ticket Price (INR): {info_parts.get('Ticket Price (INR)', 'Data not available')}</p>
                        <p class="info-section">Rating: {info_parts.get('Rating', 'Data not available')}</p>
                        <p class="info-section">Timing: {info_parts.get('Timing', 'Data not available')}</p>
                        <p class="info-section">Special Features: {info_parts.get('Special Features', 'Data not available')}</p>
                        <p class="info-section">Visitor Footfall: {info_parts.get('Visitor Footfall Data', 'Data not available')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Fetch and display the photo
                photo_url = fetch_image(attraction_name)
                if photo_url:
                    st.image(photo_url, caption=attraction_name)
                else:
                    st.write("📷 Image not available")

                # Fetch and display the weather data
                location = info_parts.get('City', state_name)
                weather = fetch_weather(location)
                if weather:
                    temp_c, condition, icon, humidity, wind_kph = weather
                    st.markdown("#### Current Weather")
                    st.image(f"http:{icon}", width=50)
                    st.write(f"**Temperature:** {temp_c}°C")
                    st.write(f"**Condition:** {condition}")
                    st.write(f"**Humidity:** {humidity}%")
                    st.write(f"**Wind Speed:** {wind_kph} kph")
                else:
                    st.write("🌤️ Weather data not available for this location.")

                st.markdown("---")  # Add a horizontal line between attractions
