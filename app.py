from flask import Flask, request, Response
import os
from openai import OpenAI
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()

    # Check if caller already said something
    user_message = request.values.get("SpeechResult")

    if not user_message:
        # First time: ask caller to speak
        gather = Gather(input="speech", action="/voice", timeout=5)
        gather.say("Hello, I am your AI assistant. How can I help you today?")
        resp.append(gather)
        return Response(str(resp), mimetype="text/xml")

    try:
        print("CALLER SAID:", user_message)

        # Send caller’s message to OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a polite receptionist. You can answer questions and help schedule appointments."},
                {"role": "user", "content": user_message}
            ]
        )

        answer = completion.choices[0].message.content
        print("OPENAI RESPONSE:", answer)

        # Speak AI’s response back to caller
        gather = Gather(input="speech", action="/voice", timeout=5)
        gather.say(answer)
        resp.append(gather)

    except Exception as e:
        print("ERROR:", str(e))
        resp.say("Sorry, I had trouble answering that.")

    return Response(str(resp), mimetype="text/xml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
