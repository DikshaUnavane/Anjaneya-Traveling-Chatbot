import streamlit as st
import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import urllib.parse
import IPython.display as display
import webbrowser
import google.generativeai as genai
from datetime import datetime
import random
import folium
from geopy.geocoders import Nominatim


# Download NLTK resources
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")
import nltk
nltk.download('stopwords')

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



# Chatbot logic
def get_chat_response(user_message):
    import random
    user_message = user_message.lower()
    greetings = ("hello", "hi", "hii", "heyy" , "hey buddy" ,  "hiii bot", "bot","greeting", "sup", "what's up", "hey" , "hello", "hi", "hey", "good morning", "good afternoon", "good evening", "what's up?", "howdy", "greetings", "how's it going?", "hey there", "yo!")
    greet_res = ["hello", "hi", "sup", "what's up", "hey", "how can I help you?" , "hello", "hi", "hey", "what's up?", "howdy", "greetings", "how's it going?", "hey there", "yo!"]

    def greet(sentence):
        if any(word.lower() in sentence for word in greetings):
            return random.choice(greet_res)
    greeting_response = greet(user_message)
    if greeting_response:
        return greeting_response
        

    def is_location_present(location):
    # Check if the location is present in the dataset
        return location.lower() in data["City"].str.lower().unique() 
    location_response = is_location_present(user_message)
    if location_response:
        return location_response
        
        
    from datetime import datetime
    import random
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

    
    if any(word in user_message.lower() for word in ["book", "booking", "reservation", "reserve"]):
            if any(item in user_message.lower() for item in ["hotel", "room", "resort"]):
                location = input("Enter the location: ")

                while True:
                    check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
                    is_valid_check_in, error_msg_check_in = validate_date(check_in_date)
                    if is_valid_check_in:
                        break
                    else:
                        st.write("Error:", error_msg_check_in)

                while True:
                    check_out_date = input("Enter check-out date (YYYY-MM-DD): ")
                    is_valid_check_out, error_msg_check_out = validate_date(check_out_date)
                    if is_valid_check_out:
                        break
                    else:
                        st.write("Error:", error_msg_check_out)

                if is_valid_check_in and is_valid_check_out:
                    booking_url = book_hotel(location, check_in_date, check_out_date)

                    webbrowser.open(booking_url)

                    # shortened_url = shorten_url(booking_url)
                    st.write("BOT: You can book a hotel using the following link:", booking_url)

            elif any(item in user_message.lower() for item in ["flight", "plane"]):
                    origin = input("Enter origin: ")
                    destination = input("Enter destination: ")
                    while True:
                        departure_date = input("Enter check-in date (YYYY-MM-DD): ")
                        is_valid, error_msg = validate_date(departure_date)
                        if is_valid:
                            break
                        else:
                            st.write("Error:", error_msg)

                    while True:
                        return_date = input("Enter check-out date (YYYY-MM-DD): ")
                        is_valid_check_out, error_msg_check_out = validate_date(return_date)
                        if is_valid_check_out:
                            break
                        else:
                            st.write("Error:", error_msg_check_out)
                    booking_url = book_flight(origin, destination, departure_date, return_date)
                    # shortened_url = shorten_url(booking_url)
                    st.write("BOT: You can book a flight using the following link:", booking_url)

            elif "train" in user_message.lower():
                    source = input("Enter source: ")
                    destination = input("Enter destination: ")
                    while True:
                        date = input("Enter check-in date (YYYY-MM-DD): ")
                        is_valid, error_msg = validate_date(date)
                        if is_valid:
                            break
                        else:
                            st.write("Error:", error_msg)

                    booking_url = book_train(source, destination, date)
                    # shortened_url = shorten_url(booking_url)
                    st.write("BOT: You can book a flight using the following link:", booking_url)


                    booking_url = book_train(source, destination, date)
                    # shortened_url = shorten_url(booking_url)
                    st.write("BOT: You can book a train using the following link:", booking_url)

            elif "bus" in user_message.lower():
                    source = input("Enter source: ")
                    destination = input("Enter destination: ")
                    while True:
                        date = input("Enter check-in date (YYYY-MM-DD): ")
                        is_valid, error_msg = validate_date(date)
                        if is_valid:
                            break
                        else:
                            st.write("Error:", error_msg)
                    booking_url = book_bus(source, destination, date)
                    # shortened_url = shorten_url(booking_url)
                    st.write("BOT: You can book a bus using the following link:", booking_url)

        
    genai.configure(api_key="AIzaSyBguROzz2IjBrAUUZuu0DDnz6pNtRoAapI")
    model = genai.GenerativeModel("gemini-pro")
    def generate_response(question):
        # Generate content based on the user's question
        response = model.generate_content(question)
        return response.text   
    
    if any(word.lower() in user_message for word in nltk.word_tokenize(user_message)):
            # Generate a response using the generative model
            response = generate_response(user_message)
            st.write("BOT:", response)      
    else:
        st.write("I am not getting your questions")    
    gen_res = generate_response(user_message)
    if gen_res:
        return gen_res
    

# Streamlit app
def main():
    st.title("Travel Assistant")
    user_message = st.text_input("You:", "")
    if st.button("Send"):
        st.write("YOU: " , user_message)
        bot_response = get_chat_response(user_message)
        st.text_area("BOT: " , value=bot_response, height=200)



if __name__ == "__main__":
    main()
