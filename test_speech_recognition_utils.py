#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 15:22:06 2023

@author: maxime
"""

# test_speech_recognition_utils.py
import unittest
from speech_recognition_utils import init_recognizer, sr

class TestMain(unittest.TestCase):
    def test_init_recognizer(self):
        recognizer = init_recognizer()
        self.assertIsInstance(recognizer, sr.Recognizer)

if __name__ == '__main__':
    unittest.main()
