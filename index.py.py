import os
from dotenv import load_dotenv
from groq import Groq
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allows Chrome Console to call this API

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
@app.route("/")
def home():
    return jsonify({"status":"working"});

@app.route("/ask", methods=["POST"])
def ask_groq():
    data = request.get_json()
    
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing 'prompt' in JSON body"}), 400

    user_prompt = data["prompt"]

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for an IoT microcontroller. Keep answers very short, clear, and under 2 sentences.",
                },
                {
                    "role": "user",
                    "content": user_prompt,
                }
            ],
            model="openai/gpt-oss-120b",
        )

        # Note: Make sure to index [0] on choices
        reply = chat_completion.choices[0].message.content
        return jsonify({"response": reply}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
