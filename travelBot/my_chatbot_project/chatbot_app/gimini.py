# import google.generativeai as genai
# from django.conf import settings
# import gemini_ai  # Import the Gemini AI library

# # Set your Gemini AI API key
# gemini_ai.api_key = "AIzaSyBguROzz2IjBrAUUZuu0DDnz6pNtRoAapI"

# # Now you can use the Gemini AI library with your API key


# genai.api_key = settings.GEMINI_KEY
# genai.configure(api_key="AIzaSyBguROzz2IjBrAUUZuu0DDnz6pNtRoAapI")
# model = genai.GenerativeModel("gemini-pro")
# response = model.generate_content("virat kohli wife")
# print(response.text)
import gemini_ai  # Import the Gemini AI library

# Set your Gemini AI API key
gemini_ai.api_key = "AIzaSyBguROzz2IjBrAUUZuu0DDnz6pNtRoAapI"

# Now you can use the Gemini AI library with your API key
# Example usage:
response = gemini_ai.generate_content("virat kohli wife")
print(response.text)
