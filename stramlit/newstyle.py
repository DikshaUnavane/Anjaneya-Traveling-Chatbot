import streamlit as st
import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
import IPython.display as display
import requests
import urllib.parse
import webbrowser
import streamlit as st
import datetime
import random
import streamlit as st
import urllib.parse
from PIL import Image
import os

from PIL import Image
import streamlit as st

# Open the image
img = Image.open('logo3.png')

# Display the image with Streamlit
#st.image(img, use_column_width=True)
# col1, col2 = st.columns([1, 4])

# # Place the image in the first column
# with col1:
#     st.image(img, width=100)

# # Place other elements in the second column
# with col2:
#     st.write("Text or other elements here")

import streamlit as st

# Divide the layout into two columns
col1, col2 = st.columns([1, 4])
row1, row2 = st.columns([1, 1])
# Place the image in the first column
with col1:
    st.image(img, width=100)

# Place other elements in the second column
with row1:
    with col2:
        st.title("Anjaneya Chatbot")



st.markdown(
    """
    <style>
    img {
        max-width: 200px; /* Set max width to 100px */
        max-height: 200px; /* Set max height to 100px */
        border-radius: 50%; /* Example border radius */
        
    }
    </style>
    """,
    unsafe_allow_html=True
)

# st.image(
#     img,
#     width=100,
#     height=100,
#     border= round,
# )

# st.markdown(
#     """
#     <style>
#     img {
#         border-radius: 10px; /* Example border radius */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
st.markdown(
    """
    <style>
    body {
        background-color: ##ffc107 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* Set input field background to transparent */
    user_input {
        background-color: transparent;
    }
    /* Set input field border color to transparent */
     user_input {
        border-color: transparent;
    }
    /* Set input field text color */
    user_input {
        color: black; /* Change text color if needed */
    }
    </style>
    """,
    unsafe_allow_html=True
)
user_input = st.text_input("You:", "")


st.markdown(
    """
    <style>
    /* Style the button */
    .stButton>button {
        background-color: #4CAF50; /* Green */
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 8px;
    }
    /* Change the button color on hover */
    .stButton>button:hover {
        background-color: #45a049; /* Darker green */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Download NLTK resources
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")


# Configure GenAI
genai.configure(api_key="AIzaSyBguROzz2IjBrAUUZuu0DDnz6pNtRoAapI")
model = genai.GenerativeModel("gemini-pro")

# Load data
file_path = "Places.csv"
data = pd.read_csv(file_path)
data.drop(data.columns[5], axis=1, inplace=True)

# Preprocess text data
data["Place_desc"] = data["Place_desc"].str.lower()

# Define stopwords and lemmatizer
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# Lemmatize words and remove stopwords
for index, row in data.iterrows():
    filter_sen = []
    sen = str(row["Place_desc"])
    sen = re.sub(r'[^\w\s]', '', sen)
    words = nltk.word_tokenize(sen)
    words = [w for w in words if not w in stop_words]
    for word in words:
        filter_sen.append(lemmatizer.lemmatize(word))
    data.at[index, "Place_desc"] = ' '.join(filter_sen)

# Concatenate columns
data["all_data"] = data["City"].fillna("") + data["Place"] + "-> Overall Rating of this place is " + data["Ratings"].fillna("").astype(str) + ". " + data["Distance"].fillna("").astype(str) + ". " + data["Place_desc"].fillna("") + ". Special Fact About that place " + data["Place"].fillna("")

# Tokenize sentences
sent_tokens = data["all_data"].tolist()

# Calculate TF-IDF vectors
tfidf_vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf_vectorizer.fit_transform(sent_tokens)

# Function to get similar sentences
def get_similar_sentences(user_message, top_n=5):
    user_tfidf = tfidf_vectorizer.transform([user_message])
    similarity_scores = cosine_similarity(user_tfidf, tfidf_matrix)
    top_indices = similarity_scores.argsort()[0][-top_n:]
    similar_sentences = [sent_tokens[i] for i in top_indices]
    return similar_sentences

greet_in = ("hello", "hi", "hii", "heyy" , "hey buddy" ,  "hiii bot", "bot","greeting", "sup", "what's up", "hey" , "Hello", "Hi", "Hey", "Good morning", "Good afternoon", "Good evening", "What's up?", "Howdy", "Greetings", "How's it going?", "Hey there", "Yo!")
greet_res = ["hello", "hi", "sup", "what's up", "hey", "how can I help you?" , "Hello", "Hi", "Hey", "What's up?", "Howdy", "Greetings", "How's it going?", "Hey there", "Yo!"]
def greet(sentence):
    if any(word.lower() in greet_in for word in nltk.word_tokenize(sentence)):
        return random.choice(greet_res)


def book_hotel(location, check_in_date , check_out_date):
    return "https://www.makemytrip.com/hotels/hotel-listing/?checkin=03062024&city=CTGOI&checkout=03072024&roomStayQualifier=2e0e&locusId=CTGOI&country=IN&locusType=city&searchText=Goa&regionNearByExp=3&rsc=1e2e0e".format(location, check_in_date, check_out_date)

def book_flight(origin, destination, departure_date, return_date=None):
    return "https://www.makemytrip.com/flight/search?itinerary=DEL-BLR-06/03/2024&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&ccde=IN&lang=eng".format(origin, destination, departure_date, return_date)

def book_train(source, destination, date):
    return "https://www.makemytrip.com/railways/listing?classCode=&className=All%20Classes&date=20240306&destCity=Kanpur&destStn=CNB&srcCity=New%20Delhi&srcStn=NDLS".format(source, destination, date)

def book_bus(source, destination, date):
    return "https://www.makemytrip.com/bus/search/Delhi/Kanpur/06-03-2024?from_code=MMTCC1199&to_code=MMTCC2140".format(source, destination, date)

def validate_date(date_str):
    try:
        # Parse the date string into a datetime object
        date = datetime.strptime(date_str, '%Y-%m-%d')
        # Get the current date
        current_date = datetime.now()

        # Check if the date is in the past
        if date < current_date:
            return False, "Date cannot be in the past."
        else:
            return True, None  # Date is valid
    except ValueError:
        return False, "Invalid date format. Please enter date in YYYY-MM-DD format."
def is_location_present(location):
# Check if the location is present in the dataset
    return location.lower() in data["City"].str.lower().unique()   
def get_weather_info(city):
    api_key = '1a9b16b294eb930505377676ad8cd169'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        return weather_description, temperature, humidity  # Returning as a tuple
    except requests.RequestException as e:
        st.write(f"Failed to fetch weather data for {city}: {e}")
        return None, None, None  # Returning default values in case of failure
def recommend_places_for_season(season):
    if season.lower() == "summer":
        return ["Leh-Ladakh", "Shimla", "Manali", "Darjeeling", "Goa"]
    elif season.lower() == "monsoon" or season.lower() == "rain" or season.lower() == "rainy":
        return ["Munnar", "Coorg", "Udaipur", "Alleppey", "Mahabaleshwar"]
    elif season.lower() == "autumn":
        return ["Jaipur", "Rishikesh", "Kerala Backwaters", "Hampi", "Jaisalmer"]
    elif season.lower() == "winter":
        return ["Auli", "Gulmarg", "Kufri", "Mcleodganj", "Ooty"]
    else:
        return ["Varanasi", "Pondicherry", "Pune", "Agra", "Mumbai"]

random_places = ["Delhi", "Mumbai", "Goa", "Jaipur", "Kerala", "Agra", "Shimla", "Darjeeling", "Pondicherry", "Varanasi",
"Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad", "Lucknow", "Surat", "Kanpur", "Nagpur",
"Indore", "Thane", "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara", "Ghaziabad", "Ludhiana", "Agra",
"Nashik", "Ranchi", "Faridabad", "Meerut", "Rajkot", "Kalyan-Dombivli", "Vasai-Virar", "Varanasi", "Srinagar", "Aurangabad",
"Dhanbad", "Amritsar", "Navi Mumbai", "Allahabad", "Howrah", "Gwalior", "Jabalpur", "Coimbatore", "Vijayawada"]
# random.shuffle(random_places)  # Shuffle the list of places
# return random_places
def get_random_places():
    return random.sample(random_places, 10)

import streamlit as st
import pandas as pd
import urllib.parse
from IPython import display


# Assuming `data` is your DataFrame containing places data

# def generate_map_url(location, api_key):
#     base_url = "https://www.google.com/maps/embed/v1/place"
#     params = {
#         "key": api_key,
#         "q": location
#     }
#     encoded_params = urllib.parse.urlencode(params)
#     return f"{base_url}?{encoded_params}"

# def handle_map_request(location, api_key):
#     map_url = generate_map_url(location, api_key)
#     if map_url:
#         st.write("BOT: Here is the map for", location)
#         st.write("Below is the map:")
#         st.markdown(f'<iframe width="600" height="450" frameborder="0" style="border:0" src="{map_url}"></iframe>', unsafe_allow_html=True)
#     else:
#         st.write("BOT: Failed to generate map URL. Please try again later.")

# def display_places(city):
#     places_data = data
#     relevant_places = places_data[places_data['City'] == city]['Place']
#     if not relevant_places.empty:
#         st.write("Relevant places in", city, "are:")
#         for place in relevant_places:
#             st.write("-", place)
#         st.write("")
#         handle_map_request(city, '1a9b16b294eb930505377676ad8cd169')  # Assuming you want to display map for the city
#     else:
#         st.write("No places found for the city", city)

# Assuming you collect user input for city
# def generate_map_url(location, api_key):
#     base_url = "https://www.google.com/maps/embed/v1/place"
#     params = {
#         "key": api_key,
#         "q": location
#     }
#     encoded_params = urllib.parse.urlencode(params)
#     return f"{base_url}?{encoded_params}"

# def display_map(location, api_key):
#     map_url = generate_map_url(location, api_key)
#     if map_url:
#         st.write("Here is the map for", location)
#         st.markdown(f'<iframe width="600" height="450" frameborder="0" style="border:0" src="{map_url}"></iframe>', unsafe_allow_html=True)
#     else:
#         st.write("Failed to generate map URL. Please try again later.")
# Assuming you have your Google Maps API key

# Call the function with your API key

def generate_map_url(location, api_key):
    base_url = "https://www.google.com/maps/embed/v1/place"
    params = {
        "q": location,
        "key": api_key
    }
    encoded_params = urllib.parse.urlencode(params)
    return f"{base_url}?{encoded_params}"

    
      
genai.configure(api_key="AIzaSyBguROzz2IjBrAUUZuu0DDnz6pNtRoAapI")
model = genai.GenerativeModel("gemini-pro")
def gemini_response(question):
    # Generate content based on the user's question
    response = model.generate_content(question)
    return response.text   
    
    
# Function to generate response using GenAI
def generate_response(user_res):
    api_key = 'AIzaSyDxh9mzu93K1Uxggh4ov5KOhvetlXX95DY'
    flag = True
    if flag:
        greeting_response = greet(user_res)
        if greeting_response:
                st.write("BOT:", greeting_response)

        elif "thanks" in user_res or  "thank you" in user_res:
            flag = False
            st.write("BOT: You're welcome! Feel Free to ask!!!")
        elif  "bye" in user_res:
            flag = False
            st.write("BOT: Goodbye! Have a great day!")
        # if "map" in user_res.lower():
        #     api_key = "AIzaSyDxh9mzu93K1Uxggh4ov5KOhvetlXX95DY"
        #     location = st.text_input("Please enter a location:")
        #     if location:
        #         map_url = generate_map_url(location, api_key)
        #         st.write("Here is the map for", location)
        #         st.markdown(f'<iframe width="600" height="450" frameborder="0" style="border:0" src="{map_url}"></iframe>', unsafe_allow_html=True)
  
        elif any(word in user_res for word in ["suggestion", "suggestions", "random", "recommendation", "recommend" , "Recommendation", "Proposal", "Advice", "Tip", "Counsel", "Guidance", "Hint", "Idea", "Suggestion", "st.text_input" , "suggest"]):
            recommended_places = get_random_places()
            if recommended_places:
                st.write("BOT: Recommended places to visit:")
                for place in recommended_places:
                    st.write("-", place)
            else:
                st.write("BOT: No recommendations available at the moment.")
        elif any(word in user_res for word in ["suggestion", "suggestions", "random", "recommendation", "recommend" , "Recommendation", "Proposal", "Advice", "Tip", "Counsel", "Guidance", "Hint", "Idea", "Suggestion", "st.text_input" , "suggest"]):
            recommended_places = get_random_places()
            if recommended_places:
                st.write("BOT: Recommended places to visit:")
                for place in recommended_places:
                    st.write("-", place)
            else:
                st.write("BOT: No recommendations available at the moment.")
        # elif "place" in user_res and any(city in user_res for city in data['City'].values):
        #     # Extract city name from user st.text_input
        #     words = nltk.word_tokenize(user_res)
        #     cities = [word for word in words if word in data['City'].values]
        #     for city in cities:
        #         display_places(city)
        elif any(word in user_res.lower() for word in ["book", "booking", "reservation", "reserve"]):
            if any(item in user_res.lower() for item in ["hotel", "room", "resort"]):
                # location = st.text_input("Enter the location: ", "")
                # if location:
                #     check_in_date = st.date_input("Enter check-in date: ", datetime.datetime.now())
                #     check_out_date = st.date_input("Enter check-out date: ", datetime.datetime.now() + datetime.timedelta(days=1))

                #     is_valid_check_in, error_msg_check_in = validate_date(check_in_date.strftime('%Y-%m-%d'))
                #     is_valid_check_out, error_msg_check_out = validate_date(check_out_date.strftime('%Y-%m-%d'))

                #     if is_valid_check_in and is_valid_check_out:
                #         booking_url = book_hotel(location, check_in_date.strftime('%Y-%m-%d'), check_out_date.strftime('%Y-%m-%d'))
                #         if booking_url:
                #             st.write("BOT: You can book a hotel using the following link:", booking_url)
                #         else:
                #             st.write("BOT: Failed to generate booking URL. Please try again later.")
                #     else:
                #         st.write("BOT: Invalid date format or date range. Please enter valid dates.")
                booking_url = "https://www.makemytrip.com/hotels/hotel-listing/?checkin=03062024&city=CTGOI&checkout=03072024&roomStayQualifier=2e0e&locusId=CTGOI&country=IN&locusType=city&searchText=Goa&regionNearByExp=3&rsc=1e2e0e"
                webbrowser.open(booking_url)
            elif "train" in user_res.lower():
                    # source = st.text_input("Enter source: ")
                    # destination = st.text_input("Enter destination: ")
                    # while True:
                    #     date = st.text_input("Enter check-in date (YYYY-MM-DD): ")
                    #     is_valid, error_msg = validate_date(date)
                    #     if is_valid:
                    #         break
                    #     else:
                    #         st.write("Error:", error_msg)

                    # booking_url = book_train(source, destination, date)
                    # shortened_url = shorten_url(booking_url)
                    booking_url = "https://www.makemytrip.com/railways/listing?classCode=&className=All%20Classes&date=20240306&destCity=Kanpur&destStn=CNB&srcCity=New%20Delhi&srcStn=NDLS"

                    webbrowser.open(booking_url)    

                    # booking_url = book_train(source, destination, date)
                    # # shortened_url = shorten_url(booking_url)
                    # st.write("BOT: You can book a train using the following link:", booking_url)

            elif "bus" in user_res.lower():
                    # source = st.text_input("Enter source: ")
                    # destination = st.text_input("Enter destination: ")
                    # while True:
                    #     date = st.text_input("Enter check-in date (YYYY-MM-DD): ")
                    #     is_valid, error_msg = validate_date(date)
                    #     if is_valid:
                    #         break
                    #     else:
                    #         st.write("Error:", error_msg)
                    # booking_url = book_bus(source, destination, date)
                    # # shortened_url = shorten_url(booking_url)
                    booking_url ="https://www.makemytrip.com/bus/search/Delhi/Kanpur/06-03-2024?from_code=MMTCC1199&to_code=MMTCC2140"

                    webbrowser.open(booking_url)
                    
            elif "flight" in user_res.lower() or "plane" in user_res.lower():
                    # source = st.text_input("Enter source: ")
                    # destination = st.text_input("Enter destination: ")
                    # while True:
                    #     date = st.text_input("Enter check-in date (YYYY-MM-DD): ")
                    #     is_valid, error_msg = validate_date(date)
                    #     if is_valid:
                    #         break
                    #     else:
                    #         st.write("Error:", error_msg)
                    # booking_url = book_bus(source, destination, date)
                    # # shortened_url = shorten_url(booking_url)
                    booking_url ="https://www.makemytrip.com/flight/search?itinerary=DEL-BLR-06/03/2024&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&ccde=IN&lang=eng"
                    webbrowser.open(booking_url)
        elif any(word in user_res.lower() for word in ["weather", "climate", "atmosphere", "meteorological", "elements", "forecast", "conditions", "temperature", "data", "meteorology"]):
            words = nltk.word_tokenize(user_res)
            for word in words:
                if is_location_present(word):
                    location = word
                    break
            if location:
                weather_description, temperature, humidity = get_weather_info(location)
                if weather_description:
                    st.write(f"BOT: Current weather in {location}:")
                    st.write(f"Weather: {weather_description}")
                    st.write(f"Temperature: {temperature}°C")
                    st.write(f"Humidity: {humidity}%")
                else:
                    st.write("BOT: Failed to fetch weather data.")
            else:
                st.write("BOT: I'm sorry, I couldn't identify the location for which you want weather information.")
        elif is_location_present(user_res):
            words = nltk.word_tokenize(user_res)
            location = None
            for word in words:
                if is_location_present(word):
                    location = word
                    break
            if location:
                weather_description, temperature, humidity = get_weather_info(location)
                if weather_description:
                    st.write(f"BOT: Current weather in {location}:")
                    st.write(f"Weather: {weather_description}")
                    st.write(f"Temperature: {temperature}°C")
                    st.write(f"Humidity: {humidity}%")
                else:
                    st.write("BOT: Failed to fetch weather data.")
                response_sentences = get_similar_sentences(user_res)
                if response_sentences:
                    for sentence in response_sentences:
                            st.write("- " + sentence)
                else:
                    pass
        elif any(word.lower() in user_res for word in nltk.word_tokenize(user_res)):
            # Generate a response using the generative model
            response = gemini_response(user_res)
            st.write("BOT:", response)
                
        else:
            st.write("I am not getting your questions")  




    
        
# Streamlit app
def main():
    # st.title("Anjaneya Chatbot")
    # user_input = st.text_input("You:", "")
    def start(user_input):
        if st.button("start"):
            st.write("YOU: " , user_input)
            response = generate_response(user_input)
            user_input = ""
            st.write("BOT:", response) 
    start(user_input)

    def generate_map_url(location, api_key):
        base_url = "https://www.google.com/maps/embed/v1/place"
        params = {
            "q": location,
            "key": api_key
        }
        encoded_params = urllib.parse.urlencode(params)
        return f"{base_url}?{encoded_params}"

    def process_message(user_input, api_key):
        if "map" in user_input.lower():
            location = st.text_input("Please enter a location:")
            if location:
                map_url = generate_map_url(location, api_key)
                st.write("Here is the map for", location)
                st.markdown(f'<iframe width="600" height="450" frameborder="0" style="border:0" src="{map_url}"></iframe>', unsafe_allow_html=True)

    api_key = "AIzaSyDxh9mzu93K1Uxggh4ov5KOhvetlXX95DY"
    if user_input:
        process_message(user_input, api_key)


        


if __name__ == "__main__":
    main()

