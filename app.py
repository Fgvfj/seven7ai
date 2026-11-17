from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "SEVENAI ONLINE - Groq is working!"

@app.route("/", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True) or {}
    msg = data.get("message", "")
    if not msg:
        return jsonify({"reply": "Send me a message Boss!"})

    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You are SEVENAI, a friendly, funny, helpful AI assistant. Keep replies short, in simple English/Hinglish, like talking to a friend."},
                    {"role": "user", "content": msg}
                ],
                "temperature": 0.7,
                "max_tokens": 300
            },
            timeout=30
        )
        j = r.json()
        reply = j["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
