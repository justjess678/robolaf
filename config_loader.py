#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:18:16 2023

@author: jess
"""

import json
import logging

def load_config(filename):
    try:
        with open(filename, 'r') as config_file:
            config = json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading config: {e}")
        return None
    
    if config is None:
        return None # Exit if config file is missing or invalid
    
    if not validate_config(config):
        logging.error("Configuration validation failed. Please check the configuration file.")
        return None # Exit if configuration is invalid

    return config


def validate_config(config):
    required_keys = ["CHATGPT_API_KEY", "VOICE_API_KEY", "VOICE_ID", "VOICE_USER"]
    for key in required_keys:
        if key not in config:
            logging.error(f"Missing required configuration key: {key}\n")
            return False
    return True
