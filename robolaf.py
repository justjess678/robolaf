#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 21:33:27 2023

@author: jess
"""

import logging
import threading

from audio_player import set_soundbytes, play_idle, set_idle_sounds
from speech_recognition_utils import init_recognizer, listen_for_keyword

logging.basicConfig(filename='olaf.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    
def main():
    logging.info("Olaf program started.")
    
    print("Initialising microphone input...")
    r = init_recognizer()
    
    print("Accessing soundbytes...")
    set_soundbytes()
    set_idle_sounds()

    print("Launching threads...")
    idle_thread = threading.Thread(target=play_idle)
    keyword_thread = threading.Thread(target=listen_for_keyword, args=(r,))

    idle_thread.daemon = True
    keyword_thread.daemon = True

    idle_thread.start()
    keyword_thread.start()

if __name__ == "__main__":
    main()