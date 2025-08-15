from flask import Flask, request, jsonify
from flasgger import Swagger
import requests
import os

app = Flask(__name__)
swagger = Swagger(app)  # Enable Swagger UI at /apidocs by default

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAAgOhuhkiyB2YBX8_gE1J2PI14R07D1bU")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

@app.route('/llm/query', methods=['POST'])
def llm_query():
    """
    Call Gemini API and return generated text.
    ---
    tags:
      - LLM
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
              example: "Hello Gemini!"
    responses:
      200:
        description: The LLM response
        schema:
          type: object
          properties:
            response:
              type: string
              example: "Hello from Gemini!"
      400:
        description: Missing 'text' in request body
    """
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    payload = {
        "contents": [{"parts": [{"text": data['text']}]}]
    }
    headers = {"Content-Type": "application/json"}
    r = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", headers=headers, json=payload)

    if r.status_code != 200:
        return jsonify({"error": "Gemini API error", "details": r.text}), r.status_code

    gemini_data = r.json()
    output_text = gemini_data['candidates'][0]['content']['parts'][0]['text']

    return jsonify({"response": output_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
