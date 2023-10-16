#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:23:16 2023

@author: jess
"""

import json
import logging
import re
import requests
from audio_player import play_sound, get_soundbyte
from config_loader import load_config

# Global variables
valid_tones = ["happy", "sad", "angry", "fearful", "disgust"]
CHATGPT_API_KEY = None
VOICE_API_KEY = None
VOICE_ID = None
VOICE_USER = None


def get_chatGPT_response(phrase):
    """
    Retrieves a chatbot response from the OpenAI GPT model.
    
    Args:
        phrase (str): The input phrase to generate a response for.
    
    Returns:
        str: The generated chatbot response.
    """
    global CHATGPT_API_KEY
    
    if not CHATGPT_API_KEY:
        config = load_config("config.json")
        CHATGPT_API_KEY = config.get("CHATGPT_API_KEY")
        
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
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"API Request Failed: {e}")
        return phrase
    
    result = response.json()
    logging.info(f"API Response: {result}")
    return result["choices"][0]["message"]["content"]

def get_tone(phrase):
    """
    Analyzes the tone of a phrase using the GPT model.
    
    Args:
        phrase (str): The phrase to analyze.
    
    Returns:
        str: The detected tone (happy, sad, angry, fearful, disgust, or surprised).
    """
    global CHATGPT_API_KEY
    
    if not CHATGPT_API_KEY:
        config = load_config("config.json")
        CHATGPT_API_KEY = config.get("CHATGPT_API_KEY")
    
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
    """
    Generates speech using a text-to-speech engine.
    
    Args:
        phrase (str): The phrase to convert to speech.
        tone (str): The desired tone of the speech (happy, sad, angry, fearful, disgust).
    """
    global VOICE_API_KEY, VOICE_ID, VOICE_USER
    
    if not VOICE_API_KEY or not VOICE_ID or not VOICE_USER:
        config = load_config("config.json")
        VOICE_API_KEY = config.get("VOICE_API_KEY")
        VOICE_ID = config.get("VOICE_ID")
        VOICE_USER = config.get("VOICE_USER")
    
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
    """
    Plays generated speech from a response.
    
    Args:
        response (requests.Response): The response containing the generated speech data.
    """
    pattern = r"event: completed\s+data: ({.*})"
    
    match = re.search(pattern, response.text)
    
    if match:
        data_json = match.group(1)
    
        data_dict = json.loads(data_json)
        url = data_dict.get("url")
    
        if url:
            print("URL:", url)
            play_sound(url)
        else:
            print("No URL found in the data.")
    else:
        print("No 'event: completed' line found in the response data.")
   