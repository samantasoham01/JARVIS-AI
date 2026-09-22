from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

# ==============================
# GROQ CLIENT
# ==============================

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


# ==============================
# CONVERSATION MEMORY
# ==============================

conversation_history = [
    {
        "role": "system",
        "content": (
            "You are JARVIS, a helpful personal AI assistant. "
            "Be intelligent, concise and polite. "
            "Address the user as Sir when appropriate. "
            "Remember the conversation and use previous messages "
            "to understand follow-up questions."
        )
    }
]


# ==============================
# NORMAL AI CHAT
# ==============================

@app.route("/ask", methods=["POST"])
def ask_jarvis():

    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({
            "error": "No message received"
        }), 400

    try:

        # Add user message to memory
        conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Keep recent conversation
        messages = (
            [conversation_history[0]]
            + conversation_history[-20:]
        )

        # Ask Groq
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            max_completion_tokens=1024,
            include_reasoning=False
        )

        answer = response.choices[0].message.content

        # Save JARVIS response
        conversation_history.append({
            "role": "assistant",
            "content": answer
        })

        return jsonify({
            "reply": answer
        })

    except Exception as e:

        # Remove failed user message
        if (
            conversation_history
            and conversation_history[-1]["role"] == "user"
        ):
            conversation_history.pop()

        return jsonify({
            "error": str(e)
        }), 500


# ==============================
# WEB SEARCH
# ==============================

@app.route("/search", methods=["POST"])
def web_search():

    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({
            "error": "No search message received"
        }), 400

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are JARVIS, a web-enabled AI assistant. "
                        "Use the browser search tool to find current "
                        "and accurate information from the internet. "
                        "Answer clearly and concisely. "
                        "If the user asks about current events, weather, "
                        "news, sports, prices, recent information, or "
                        "anything that may have changed, search the web "
                        "before answering."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_completion_tokens=1024,
            tool_choice="required",
            tools=[
                {
                    "type": "browser_search"
                }
            ]
        )

        answer = response.choices[0].message.content

        return jsonify({
            "reply": answer
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==============================
# CLEAR MEMORY
# ==============================

@app.route("/clear", methods=["POST"])
def clear_memory():

    global conversation_history

    conversation_history = [
        {
            "role": "system",
            "content": (
                "You are JARVIS, a helpful personal AI assistant. "
                "Be intelligent, concise and polite. "
                "Address the user as Sir when appropriate. "
                "Remember the conversation and use previous messages "
                "to understand follow-up questions."
            )
        }
    ]

    return jsonify({
        "message": "JARVIS memory cleared"
    })


# ==============================
# SERVER START
# ==============================

if __name__ == "__main__":

    print("======================================")
    print("        JARVIS BACKEND STARTING")
    print("======================================")
    print("Server: http://192.168.29.35:5000")
    print("Web Search: ENABLED")
    print("AI Model: openai/gpt-oss-20b")
    print("======================================")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )