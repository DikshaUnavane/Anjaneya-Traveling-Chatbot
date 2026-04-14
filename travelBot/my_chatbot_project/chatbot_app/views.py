# chatbot_app/views.py

from django.shortcuts import render , HttpResponse
from django.http import JsonResponse
import google.generativeai as genai
    
def index(request):

        return render(request, 'chatbot_app\index.html')



def chatbot(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
           
    # Configure the API key
    genai.configure(api_key="AIzaSyBguROzz2IjBrAUUZuu0DDnz6pNtRoAapI")

    # Create a GenerativeModel instance
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_input)
    bot_response = response.text
    return JsonResponse({'bot_response': bot_response})
    
