import google.generativeai as genai

# 1. Configure API key
genai.configure(api_key="AIzaSyAAgOhuhkiyB2YBX8_gE1J2PI14R07D1bU")

# 2. Create the model
model = genai.GenerativeModel("gemini-1.5-flash")  # ✅ Updated model name

# 3. Generate content
response = model.generate_content("Write a short poem about AI and nature.")

# 4. Print the response
print(response.text)
