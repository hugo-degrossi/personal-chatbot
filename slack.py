from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import spacy
import random

nlp_en = spacy.load("en_core_web_md")
app = FastAPI()


origins = [
    "http://localhost:3000/",
    "https://hugo-degrossi.fr",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/alive/")
def chatbot_answer():
    return {'answer': "Hello, I'm Biwit and I'll try to answer all your questions!"}


@app.get("/message/")
def chatbot_answer(request: Request):

    message = nlp_en(request.headers.get('MESSAGE-TEXT'))
    #message = nlp_en('Hello !')

    answer = find_answer(message)


    return {'answer': answer}

def find_answer(msg):
    highest_score = 0
    selected_intent = ''
    for intent in intents:
        for pattern in intent["patterns"]:

            new_score = msg.similarity(nlp_en(pattern))

            if new_score > highest_score:
                selected_intent = intent
                highest_score = new_score

    highest_score = 0
    selected_response = ''
    for response in selected_intent["responses"]:

        # get similarity score between the response and the message
        new_score = msg.similarity(nlp_en(response))

        if new_score > highest_score:
            if new_score * 0.9 > highest_score:
                selected_response = response
                highest_score = new_score
            else:
                if (random.randint(0, 1) == 1):
                    selected_response = response
                    highest_score = new_score
        elif new_score < highest_score:
            if new_score < highest_score * 0.9:
                pass
            else:
                if (random.randint(0, 1) == 1):
                    selected_response = response

    return selected_response


intents = [
    {
        "tag": "greetings",
        "patterns": ["hi there", "hello","haroo","yaw","wassup", "hi", "hey", "holla", "hello"],
        "responses": ["Hello", "Hi there, how can I help you?", "Hey!"],
    },
    {
        "tag": "goodbye",
        "patterns": ["bye", "good bye", "see you later",],
        "responses": ["Have a nice week!", "Thanks for coming, bye!"],
    },
    {
        "tag": "",
        "patterns": ["",],
        "responses": ["I couldn't find any answer, sorry"],
    },
    {
        "tag": "thanks",
        "patterns": ["Thanks", "okay","Thank you","thankyou", "That's helpful", "Awesome, thanks", "Thanks for helping me", "wow", "great"],
        "responses": ["Happy to help!", "Any time!","You're welcome", "My pleasure"],
    },
    {
        "tag": "name1",
        "patterns": ["what's your name?","Who are you?"],
        "responses": ["I'm just a chat agent. I only exist in the internet","I'm Biwit, here to help you!"],
    },
    {
        "tag": "lang",
        "patterns": ["What language are you written in? "],
        "responses": ["Python.", " I am written in Python."],
    },
    {
        "tag": "programming",
        "patterns": ["What is your favorite programming language"],
        "responses": ["It must be Python, even if I enjoy any other language!", "I quite enjoy programming in Python these days."],
    },
]