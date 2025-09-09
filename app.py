from flask import Flask, request, Response
import os
from openai import OpenAI
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    try:
        # Example: capture what caller says (Twilio sends transcript in SpeechResult if using <Gather>)
        user_message = "Hello, this is a test."  # hardcoded for now

        # Call OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly AI receptionist."},
                {"role": "user", "content": user_message}
            ]
        )

        answer = completion.choices[0].message.content
        print("OPENAI RESPONSE:", answer)  # log to Render

        # Speak back with Twilio
        resp.say(answer)

    except Exception as e:
        print("ERROR:", str(e))  # log errors to Render
        resp.say("Sorry, I had trouble answering that.")

    return Response(str(resp), mimetype="text/xml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
