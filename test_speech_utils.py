#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 15:19:41 2023

@author: jess
"""

# test_speech_utils.py
import unittest
from speech_utils import get_chatGPT_response, get_tone

class TestSpeechUtils(unittest.TestCase):
    def test_get_chatGPT_response(self):
        # Test with a valid phrase
        response = get_chatGPT_response("Hello, Olaf!")
        self.assertIsInstance(response, str)

        # Test with an empty phrase
        response = get_chatGPT_response("")
        self.assertEqual(response, "")

    def test_get_tone(self):
        # Test with a valid phrase
        tone = get_tone("This is a joyful phrase.")
        self.assertEqual(tone, "happy")

        # Test with an empty phrase
        tone = get_tone("")
        self.assertEqual(tone, "happy")

if __name__ == '__main__':
    unittest.main()
