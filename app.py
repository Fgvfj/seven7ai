from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return f"SEVENAI ONLINE - Key set: {bool(GROQ_API_KEY)}"

@app.route("/", methods=["POST"])
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True) or {}
    msg = data.get("message", "")
    if not msg:
        return jsonify({"reply": "Send me a message Boss!"})

    if not GROQ_API_KEY:
        return jsonify({"reply": "ERROR: GROQ_API_KEY not set in Render! Go to Render > Environment and add it."})

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
                    {"role": "system", "content": "You are SEVENAI, a friendly, funny, helpful AI assistant. Keep replies short."},
                    {"role": "user", "content": msg}
                ],
                "temperature": 0.7,
                "max_tokens": 300
            },
            timeout=30
        )
        j = r.json()
        print("GROQ RAW:", j)  # will show in Render logs
        if "choices" in j:
            return jsonify({"reply": j["choices"][0]["message"]["content"]})
        else:
            # Show real Groq error in Godot
            return jsonify({"reply": f"GROQ ERROR: {j}"})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
