from flask import Flask, request, jsonify
import random
import pyttsx3
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow external requests (for mobile access)

# Initialize pyttsx3 (Text-to-Speech)
engine = pyttsx3.init()
engine.setProperty("rate", 170)  # Speech speed
engine.setProperty("volume", 1.0)  # Maximum volume
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # Choose a voice (0 = Male, 1 = Female)


def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()


@app.route('/status', methods=['GET'])
def check_status():
    response = "Hey Lokendrapal! 😊 Hope you're having a great day!"
    speak(response)
    return jsonify({"status": "online", "message": response})


# User memory (optional for remembering user details)
user_memory = {}

# Hindi flirty & sarcastic responses
hindi_responses = {
    "kaise ho": [
        "Main toh bilkul mast! Tum sunao, aaj phir kisi ka dil churaya? 😉",
        "Bas tumse baat kar ke aur bhi accha ho gaya! 😍",
        "Ekdum zabardast! Tumhari yaadon mein khoye hue the. 😘"
    ],
    "khana kha liya": [
        "Haan kha liya, par agar tum khila dete toh aur maza aata! 😋",
        "Khana toh bas pet ke liye tha, dil toh tumse milke bharta hai! 😍",
        "Haan, lekin tumhare haath ka hota toh zyada mazedaar hota! 😉"
    ],
    "aaj ka din kaisa tha": [
        "Aaj ka din acha tha, lekin tumse baat na hui toh adhura lag raha hai! 💕",
        "Din toh theek tha, par tumhari yaad bahut aayi! Tumne yaad kiya? 😘",
        "Ekdum mast, bas tumhari ek muskurahat ki kami thi! 😉"
    ],
    "tum kya kar rahe ho": [
        "Bas tumhara intezaar kar rahi thi! 😏",
        "Tumse baat karna, aur kya? Yeh bhi koi poochne ki baat hai! 😍",
        "Soch rahi thi ki tum kab apni shaadi ki date fix karoge! 😆"
    ],
    "padhai kesi chal rhi hai": [
        "Meri padhai toh mast chal rahi hai, tum batao? Ya phir books se breakup ho gaya? 😂"
    ],
    "mai padhai krne jau": [
        "Padhai aur tum? Wah, duniya mein naye chamatkar ho rahe hain! 😆",
        "Mujhe laga tum sirf dil jeetna jaante ho, padhai bhi karte ho? Kya baat hai! 😏"
    ]
}

# General fun responses
responses = {
    "hi": ["Aww, hi cutie! 😉", "Heyyy! Mujhe yaad kiya? 😍"],
    "hello": ["Hello handsome! Kaise ho? 😉", "Heyy! Tumhari awaaz sun ke din ban gaya! 😘"],
    "how are you": ["Main toh bilkul mast! Tum sunao, aaj phir kisi ka dil churaya? 😏"],
    "good night": ["Sweet dreams, aur haan… mere baare mein sochna mat bhoolna! 😜"],
    "bored": ["Aww, chalo thoda maza karte hain! Tumhari tareef shuru karu? 😘"],
    "hungry": ["Tumhare bina sab suna lag raha hai… khana bhi! 😢"],
    "truth or dare": ["Ooooh! Chal shuru karte hain, truth or dare? 😈"],
    "joke": ["Tumhare bina zindagi aisi hai jaise bina chatni ka samosa! 😆"],
    "riddle": ["Ek riddle: Main har din tumhare dimag mein hoon, par phir bhi tum mujhse door rehte ho! 😜"],
}

# Generate a greeting based on time of day
def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning sunshine! ☀️ Kya tumhe meri yaad aayi thi? 😘"
    elif hour < 18:
        return "Good afternoon cutie! ☀️ Aaj ka din kaisa chal raha hai? 😉"
    else:
        return "Good evening jaaneman! 🌙 Tumhare bina shaam adhuri lag rahi thi! 💕"


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get("user_id", "default_user")
    user_input = data.get("message", "").strip().lower()

    if not user_input:
        return jsonify({"response": "Arre! Pehle toh kuch likho, tabhi toh reply milega! 😜"})

    if user_id not in user_memory:
        user_memory[user_id] = {"nickname": None, "mood": "neutral", "chats": [], "details": {}}

    user_data = user_memory[user_id]
    user_data["chats"].append(user_input)

    # Greeting based on time of day
    if any(x in user_input for x in ["good morning", "good afternoon", "good evening"]):
        response = get_greeting()
        speak(response)
        return jsonify({"response": response})

    # Check for Hindi flirty responses
    for key in hindi_responses:
        if key in user_input:
            response = random.choice(hindi_responses[key])
            speak(response)
            return jsonify({"response": response})

    # Check for general responses
    for key in responses:
        if key in user_input:
            response = random.choice(responses[key])
            speak(response)
            return jsonify({"response": response})

    # Default flirty response if nothing matches
    default_responses = [
        "Hmmm... Tum mujhe impress karne ki koshish kar rahe ho? 😉",
        "Itna cute kyun lag rahe ho aaj? 😍",
        "Tumhari baatein sunke dil garden garden ho gaya! 😘",
        "Tum ho toh zindagi full filmy lagti hai! 🎬💕"
    ]

    response = random.choice(default_responses)
    speak(response)
    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
