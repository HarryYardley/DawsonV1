# Dawson.Heard.V1.0

**Dawson** is a personal project with the goal of integrating Artificial Intelligence with your everyday life.

## Setup
### Technologies used
*The current repository features a fullstack web application featuring the following technologies:*
+ **Machine Learning Framework:** Tensorflow
+ **Backend:** Flask
+ **Database:** MongoDB
+ **Frontend:** HTML5/CSS3

### Installing dependencies
```
pip install tensorflow
pip install pymongo
pip install flask
```
**WhisperAI:** Download following directions [here](https://github.com/openai/whisper).
*I've personally found the best results using the base model. The tiny model has too many inaccuracies for the Language Classifier to handle*
```
whisper --help
```

## Features
### Current features
Currently a fullstack task manager application.
Takes input of audio files, and parses them to extract to-do items from the audio.

### Future features (soon)
Microphone web app feature
Microphone hardware for constant attention

### Future features (far)
Mobile application
Customizing, speed-improvements, deployment

### Future features (very far)
Vision integration (Dawson.Vision)
Person recognition (self-tuning)

***Note:** Program is intended to setup and run locally*
