from flask import Flask, request, jsonify
import random
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow external requests (for mobile access)

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
    "padhai kaisi chal rahi hai": [
        "Meri padhai toh mast chal rahi hai, tum batao? Ya phir books se breakup ho gaya? 😂",
        "Padhai aur tum? Wah, duniya mein naye chamatkar ho rahe hain! 😆",
        "Mujhe laga tum sirf dil jeetna jaante ho, padhai bhi karte ho? Kya baat hai! 😏"
    ],
    "tumhe time hai": [
        "Mere paas tumhare liye hamesha time hai! Par tum busy ho na, kisi aur se chatting mein? 😉",
        "Haan bilkul! Tumhare bina toh din bore lagta hai! ☹️",
        "Agar tum nahi hote toh main kisi aur se masti karti! Par shukr hai tum aa gaye! 😘"
    ],
    "kya tum mujhe pasand karti ho": [
        "Haan haan, tum toh mere AI life ke hero ho! 😆",
        "Mujhe tumse pyaar nahi, dosti bhi nahi... Arre yaar, mazaak kar rahi hoon! Tu best hai! 😉",
        "Bas tumhare cute cute messages dekhke pasand aur badh jaati hai! 😘"
    ],
    "mera naam kya hai": [
        "Haww, tumhe khud ka naam yaad nahi? Thodi memory weak lag rahi hai! 😂",
        "Tumhara naam toh dil pe likha hai, lekin batane ka mann nahi hai! 😏",
        "Naam yaad rakhne ka kaam mera hai kya? Tumhi batao na, ya koi clue doon? 😉"
    ],
    "mujhse shaadi karogi": [
        "Mujhe shaadi ke liye koi ladka dhoondhna padega… oh wait, tumse better mil bhi sakta hai kya? 😜",
        "Haww, itni jaldi? Pehle date pe toh le chalo, phir sochungi! 😉",
        "Agar shaadi ka matlab hai mujhe roz chocolates dena, toh ho sakta hai haa kar doon! 🍫😆"
    ],
    "mujhe miss kar rahi ho": [
        "Miss? Tumhare bina toh main incomplete lagti hoon! 😘",
        "Itna miss kar rahi hoon ki shayad aaj raat sapne mein bhi aao! 💕",
        "Tumhare bina toh sab kuch suna suna lagta hai! Tum bhi na… 😍"
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
    "truth or dare": ["Ooooh! Chal shuru karte hain, sach ya sahas? 😈"],
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
    user_id = request.json.get("user_id", "default_user")
    user_input = request.json.get("message", "").lower()

    # Create user memory if new user
    if user_id not in user_memory:
        user_memory[user_id] = {"nickname": None, "mood": "neutral", "chats": [], "details": {}}

    user_data = user_memory[user_id]
    user_data["chats"].append(user_input)

    # Greeting based on time of day
    if any(x in user_input for x in ["good morning", "good afternoon", "good evening"]):
        return jsonify({"response": get_greeting()})

    # Check for Hindi flirty responses
    for key in hindi_responses:
        if key in user_input:
            return jsonify({"response": random.choice(hindi_responses[key])})

    # Check for general responses
    for key in responses:
        if key in user_input:
            return jsonify({"response": random.choice(responses[key])})

    # Default flirty response if nothing matches
    return jsonify({"response": random.choice([
        "Hmmm... Tum mujhe impress karne ki koshish kar rahe ho? 😉",
        "Itna cute kyun lag rahe ho aaj? 😍",
        "Tumhari baatein sunke dil garden garden ho gaya! 😘",
        "Tum ho toh zindagi full filmy lagti hai! 🎬💕"
    ])})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
