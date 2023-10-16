#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:30:14 2023

@author: jess
"""

import speech_recognition as sr
import string
from speech_utils import get_chatGPT_response, get_tone, generate_speech

# Global variables
KEYWORD = "hey olaf"

def init_recognizer():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=10)
    return r


def listen_for_keyword(recognizer):
    """
    Listens for a keyword and initiates chatbot interactions.
    
    Args:
        recognizer (speech_recognition.Recognizer): The speech recognition engine.
    """
    while True:
        with sr.Microphone() as source:
            print("Listening for keyword...")
            audio = recognizer.listen(source)
            try:
                user_in = recognizer.recognize_google(audio).lower()
                
                # Input validation and sanitation
                user_in = user_in.strip()
                user_in = ''.join(filter(lambda char: char in string.printable, user_in))

                print("Heard: ", user_in)
                if KEYWORD in user_in:
                    print("this is for Olaf!")
                    phrase = user_in.replace(KEYWORD,"").lower()
                    resp = get_chatGPT_response(phrase)
                    tone = get_tone(resp)
                    generate_speech(resp, tone)
            except sr.UnknownValueError:
                pass
