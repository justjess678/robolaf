#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 21:33:27 2023

@author: jess
"""

import json
import os
import random
import re
import requests
import threading
import time
import vlc

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Constants
CHATGPT_API_KEY = config.get("CHATGPT_API_KEY")
KEYWORD = "hey olaf"
VOICE_API_KEY = config.get("VOICE_API_KEY")
VOICE_ID = config.get("VOICE_ID")
VOICE_USER = config.get("VOICE_USER")


# Global variables
soundbytes = []
idle_sounds = []
idle_player = vlc.MediaPlayer()
response_player = vlc.MediaPlayer()
user_input = []
valid_tones = ["happy", "sad", "angry", "fearful", "disgust"]


# Load user input from a file
with open('user_in', 'r') as file:
    user_input = file.readlines()


def set_soundbytes():
    global soundbytes
    folder_path = "soundbytes/"    
    soundbytes = [os.path.join(root, file) for root, dirs, files in os.walk(folder_path) for file in files if file.endswith(".mp3")]


def get_soundbyte():
    global soundbytes
    return random.choice(soundbytes)

def set_idle_sounds():
    global idle_sounds
    folder_path = "idle_sounds/"
    idle_sounds = [os.path.join(root, file) for root, dirs, files in os.walk(folder_path) for file in files if file.endswith(".mp3")]


def get_idle_sound():
    global idle_sounds
    return random.choice(idle_sounds)

def play_idle():
    while True:
        time.sleep(random.randint(5, 20))
        if response_player.get_state() != vlc.State.Playing:
            sound = get_idle_sound()
            print("playing idle sound: " + sound)
            idle_player.set_mrl(sound)
            idle_player.play()
            time.sleep(random.randint(5, 20))

def stop_idle():
    idle_player.stop()

def get_chatGPT_response(phrase):
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHATGPT_API_KEY}"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", 
                      "content": "as Olaf from Frozen, respond to this statement:" + phrase}],
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        print("API Response:", result)
        return result["choices"][0]["message"]["content"]
    else:
        print("API Request Failed with status code:", response.status_code)
        print("Response Text:", response.text)
        return phrase

def get_tone(phrase):
    if not phrase:
        return "happy"
    
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHATGPT_API_KEY}"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", 
                      "content": "Would you describe the tone of this phrase:\"" + phrase + "\" as: happy, sad, angry, fearful, disgust or surprised? You must pick one. Your answer should only contain the name of the tone."}],
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        content = result["choices"][0]["message"]["content"].lower()
        content_lower = content.lower()
        for tone in valid_tones:
            if tone in content_lower:
                return tone
        return valid_tones[0]
    else:
        print("API Request Failed with status code:", response.status_code)
        print("Response Text:", response.text)
        return "happy"
    
def generate_speech(phrase, tone):
    if not phrase:
        play_sound(get_soundbyte())
        return
    # https://docs.play.ht/reference/api-generate-audio
    
    url = "https://api.play.ht/api/v2/tts"
    
    payload = {
        "text": phrase,
        "voice": VOICE_ID,
        "output_format": "mp3",
        "voice_engine": "PlayHT2.0",
        "emotion": "male_" + tone
    }
    headers = {
        "accept": "text/event-stream",
        "content-type": "application/json",
        "AUTHORIZATION": VOICE_API_KEY,
        "X-USER-ID": VOICE_USER
    }
    print(headers)
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        play_generated_sound(response)
    else:
        print("Voice request failed with status code:", response.status_code, response.text)

    
def play_generated_sound(response):
    # Define a regex pattern to match lines containing "event: completed"
    pattern = r"event: completed\s+data: ({.*})"
    
    # Search for the pattern in the response data
    match = re.search(pattern, response.text)
    
    if match:
        # Extract the JSON content from the match
        data_json = match.group(1)
    
        # Parse the JSON to access the "url" field
        data_dict = json.loads(data_json)
        url = data_dict.get("url")
    
        if url:
            print("URL:", url)
            play_sound(url)
        else:
            print("No URL found in the data.")
    else:
        print("No 'event: completed' line found in the response data.")
    
def play_sound(url): 
    while idle_player.get_state() == vlc.State.Playing:
        time.sleep(0.1)
    response_player.set_mrl(url)
    response_player.play()
    
def listen_for_keyword():
    while True:
        time.sleep(3)
        print("listening for keyword")
        kw = random.choice(user_input)
        if KEYWORD in kw.lower():
            phrase = kw.replace(KEYWORD,"").lower()
            resp = get_chatGPT_response(phrase)
            tone = get_tone(resp)
            generate_speech(resp, tone)
    
if __name__ == "__main__":
    set_soundbytes()
    set_idle_sounds()
    
    idle_thread = threading.Thread(target=play_idle)
    keyword_thread = threading.Thread(target=listen_for_keyword)
    
    idle_thread.daemon = True
    keyword_thread.daemon = True
    
    idle_thread.start()
    keyword_thread.start()
    
    
