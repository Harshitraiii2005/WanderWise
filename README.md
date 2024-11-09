WanderWise is a web application designed to help users explore the best tourist attractions across India. By providing real-time weather data, tourist attraction details, and location-based services, it aims to make travel planning easier and more convenient for tourists.

This application is built using Streamlit, Python, and various APIs, and is deployed for public use to help travelers make informed decisions when visiting different states and cities in India.

Features
Tourist Attraction Information: Access detailed information about popular tourist attractions across various states in India. This includes details like ticket prices, ratings, timings, nearest metro/bus stations, and special features.

Weather Information: Get real-time weather updates for any selected location using an integrated weather API.

Map Integration: The app integrates interactive maps using Folium to display the exact location of tourist attractions, helping users easily navigate to their destinations.

Seasonality & Event Schedules: Know the best times to visit specific attractions, based on seasonal trends and scheduled events.

Visitor Footfall Data: Understand the popularity of various attractions with visitor footfall data.



Tech Stack
Python: The core programming language used to build the app.
Streamlit: A Python-based framework to create beautiful and interactive web apps with minimal effort.
Folium: For map visualizations, allowing for interactive, location-based features.
Pandas: For data handling and processing.
Requests: To fetch data from external APIs like weather data.
Git: For version control and collaboration.
Installation
To run this project locally, follow these steps:

Clone the repository:

bash
Copy code
git clone https://github.com/Harshitraiii2005/WanderWise.git
Navigate to the project directory:

bash
Copy code
cd WanderWise
Create a virtual environment (optional but recommended):

bash
Copy code
python -m venv venv
Activate the virtual environment:

For Windows:
bash
Copy code
.\venv\Scripts\activate
For MacOS/Linux:
bash
Copy code
source venv/bin/activate
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Run the application:

bash
Copy code
streamlit run app.py
APIs Used
Weather API: Provides real-time weather data for the selected location. (Make sure to replace the API keys in the code).
Contributing
We welcome contributions! Feel free to fork the repository and submit a pull request. If you have any suggestions or issues, open an issue in the GitHub repository.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
Streamlit: For building the interactive web app.
Folium: For interactive mapping solutions.
Weather APIs: For providing accurate weather information.
Pandas: For data manipulation and analysis.
GitHub: For hosting the repository.
