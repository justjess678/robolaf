# Olaf the Snowman Voice Assistant

## Introduction

Olaf the Snowman Voice Assistant is a Python project that brings the lovable character Olaf from Disney's Frozen to life. It utilizes various APIs and libraries to listen for a keyword, generate voice responses in Olaf's style, and play appropriate sound effects.

## Features

- **Keyword Activation:** The assistant is activated by saying "hey Olaf," making it responsive to voice commands.

- **Interactive Responses:** Olaf responds to user statements and questions with text-to-speech functionality, delivering lines in Olaf's voice.

- **Emotion Recognition:** The assistant can determine the tone of the response to emotions like happiness, sadness, anger, fear, and more.

- **Random Idle Sounds:** To keep Olaf "busy" and entertaining, the project plays random idle sounds in the background when not interacting with the user.

## Prerequisites

Before running the Olaf Voice Assistant, you'll need to have the following:

- Python 3 installed
- VLC media player
- Dependencies installed (you can install them using `pip install -r requirements.txt`)
- A [chatGPT](https://chat.openai.com) account
- A [play.ht](https://play.ht) account and a generated voice

## Configuration

To get started, create a `config.json` file in the project directory and add your API keys and configuration:

```json
{
    "CHATGPT_API_KEY": "YOUR_CHATGPT_API_KEY",
    "VOICE_ID": "YOUR_PLAY.HT_VOICE_ID",
    "VOICE_API_KEY": "YOUR_PLAY.HT_API_KEY",
    "VOICE_USER": "YOUR_PLAY.HT_USER"
}
```
Replace the placeholders with your actual API keys and configuration.

## Usage
Run the Python script main.py to start the Olaf Voice Assistant.
The assistant will listen for the keyword "hey Olaf." When it hears the keyword, it will activate and respond to your commands and statements in Olaf's voice. For testing purposes, it currently reads commands from a text file.


## Additional Sounds
You can add your sound files to the soundbytes and idle_sounds directories to customize Olaf's responses and idle sounds further. These sounds are played at random intervals.
