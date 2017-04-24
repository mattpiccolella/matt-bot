# -*- coding: utf-8 -*-

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

SAMPLE_CONVERSATION = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]

def train_chatbot(conversation):
    chatbot = ChatBot("Matt Bot")
    chatbot.set_trainer(ListTrainer)
    chatbot.train(conversation)

    return chatbot

if __name__ == '__main__':
    chatbot = train_chatbot(SAMPLE_CONVERSATION)

    input_string = raw_input('>')
    while input_string != -1:
        input_string = raw_input('>')

        print chatbot.get_response(input_string)