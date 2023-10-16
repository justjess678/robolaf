#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:40:04 2023

@author: maxime
"""

# test_config_loader.py
import unittest
from config_loader import load_config, validate_config

class TestConfigUtils(unittest.TestCase):
    def test_load_config(self):
        # Test loading a valid config file
        with open('valid_config.json', 'w') as f:
            f.write('{"CHATGPT_API_KEY": "api_key", "VOICE_API_KEY": "voice_key", "VOICE_ID": "voice_id", "VOICE_USER": "user"}')
        
        config = load_config('valid_config.json')
        self.assertIsInstance(config, dict)

        # Test loading an invalid config file
        config = load_config('invalid_config.json')
        self.assertIsNone(config)

    def test_validate_config(self):
        # Test valid configuration
        valid_config = {"CHATGPT_API_KEY": "abc123", "VOICE_API_KEY": "xyz456", "VOICE_ID": "olaf", "VOICE_USER": "jess"}
        self.assertTrue(validate_config(valid_config))

        # Test missing required keys
        invalid_config = {"CHATGPT_API_KEY": "abc123", "VOICE_ID": "olaf", "VOICE_USER": "jess"}
        self.assertFalse(validate_config(invalid_config))

if __name__ == '__main__':
    unittest.main()
