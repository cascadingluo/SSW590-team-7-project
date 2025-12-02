# import google.generativeai as genai
# import os
# # genai.configure(api_key="AIzaSyDoH4bxqpmoe0oiGvwbUlqxRQ5SlyUhCvU")
# # model = genai.GenerativeModel(model_name="tunedModels/mentalhealthchatbot-7mrtrsg0fib1")
# # response = model.generate_content("What is a panic attack?")
# # print(response.text)

# client = genai.Client()
# response = client.models.generate_content(
#     model="gemini-2.5-flash", contents="Explain how AI works in a few words"
# )
# print(response.text)

from google import genai

import os

API_KEY = 'AIzaSyB76uW0XLIijk8ulil5MW358tbsM-VP6zU'

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words"
)

print(response.text)
