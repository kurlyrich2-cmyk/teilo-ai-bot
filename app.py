from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)

# ✅ Load your OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/voice", methods=["POST"])
def voice():
    # If caller just connected, prompt them to say something
    if "SpeechResult" not in request.form:
        twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather input="speech" action="/voice" method="POST" timeout="5">
        <Say voice="alice">Hello, thanks for calling. How can I help you today?</Say>
    </Gather>
    <Say>I didn’t catch that. Goodbye!</Say>
</Response>"""
        return Response(twiml, mimetype="text/xml")

    # ✅ Get caller's speech
    user_input = request.form["SpeechResult"]

    # ✅ Send to OpenAI
    try:
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",  # lightweight GPT model
            messages=[
                {"role": "system", "content": "You are a polite AI receptionist for a small business."},
                {"role": "user", "content": user_input}
            ]
        )
        ai_reply = completion.choices[0].message.content.strip()
    except Exception as e:
        ai_reply = "Sorry, I had trouble answering that."

    # ✅ Respond back with AI's reply
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">{ai_reply}</Say>
    <Gather input="speech" action="/voice" method="POST" timeout="5">
        <Say>Anything else I can help you with?</Say>
    </Gather>
</Response>"""

    return Response(twiml, mimetype="text/xml")

# ✅ Health check route
@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

# ✅ Error handler
@app.errorhandler(500)
def server_error(e):
    return Response(
        '<?xml version="1.0" encoding="UTF-8"?><Response><Say>Sorry, something went wrong.</Say></Response>',
        mimetype="text/xml"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
