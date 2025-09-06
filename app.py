from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    # TwiML response (Twilio XML)
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say voice="alice">Hello, thanks for calling! This is your AI receptionist test.</Say>
    </Response>"""
    return Response(twiml, mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
