import google.generativeai as genai
genai.configure(api_key="AIzaSyBguROzz2IjBrAUUZuu0DDnz6pNtRoAapI")
model = genai.GenerativeModel("gemini-pro")
response = model.generate_content("virat kohli wife")
print(response.text)
