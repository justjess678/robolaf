#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:25:00 2023

@author: jess
"""

import os
import random
import time
import vlc

# Global variables
soundbytes = []
idle_sounds = []
idle_player = vlc.MediaPlayer()
response_player = vlc.MediaPlayer()

def set_soundbytes():
    """
    Sets the list of available sound files by traversing a directory.
    """
    global soundbytes
    folder_path = "soundbytes/"    
    soundbytes = [os.path.join(root, file) for root, dirs, files in os.walk(folder_path) for file in files if file.endswith(".mp3")]


def get_soundbyte():
    """
    Gets a random sound file from the list.
    
    Returns:
        str: Path to a random sound file.
    """
    global soundbytes
    return random.choice(soundbytes)


def set_idle_sounds():
    """
    Sets the list of available idle sound files by traversing a directory.
    """
    global idle_sounds
    folder_path = "idle_sounds/"
    idle_sounds = [os.path.join(root, file) for root, dirs, files in os.walk(folder_path) for file in files if file.endswith(".mp3")]


def get_idle_sound():
    """
    Gets a random idle sound file from the list.
    
    Returns:
        str: Path to a random idle sound file.
    """
    global idle_sounds
    return random.choice(idle_sounds)


def play_idle():
    """
    Plays idle sounds at random intervals.
    """
    while True:
        time.sleep(random.randint(5, 20))
        if response_player.get_state() != vlc.State.Playing:
            sound = get_idle_sound()
            print("playing idle sound: " + sound)
            idle_player.set_mrl(sound)
            idle_player.play()
            time.sleep(random.randint(5, 20))


def stop_idle():
    """
    Stops the idle sound player.
    """
    idle_player.stop()


def play_sound(url): 
    """
    Plays a sound from a given URL.
    
    Args:
        url (str): The URL of the sound to be played.
    """
    while idle_player.get_state() == vlc.State.Playing:
        time.sleep(0.1)
    response_player.set_mrl(url)
    response_player.play()