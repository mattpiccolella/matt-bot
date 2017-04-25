# -*- coding: utf-8 -*-

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from data import prune_conversations
import pdb, time

INPUT_DATA_FILE = 'data/result.csv'
CHUNK_SIZE = 20
CONVO_LIMIT = 500

def train_chatbot_from_file(input_data_file):
    chatbot = ChatBot("Matt Bot",
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        database='heroku_vzt7md78',
        database_uri='mongodb://matt:buddymatt123@ds119151.mlab.com:19151/heroku_vzt7md78')
    chatbot.set_trainer(ListTrainer)

    # Generate the conversations from our data.
    messages_trained = 0
    conversations = prune_conversations.prune_conversations(input_data_file)
    for conversation in conversations:
        encoded_conversation = [message.decode('utf-8') for message in conversation]
        chatbot.train(encoded_conversation)
        messages_trained += len(encoded_conversation)
        print 'Trained: ' + str(messages_trained)

    return chatbot

if __name__ == '__main__':
    chatbot = train_chatbot_from_file(INPUT_DATA_FILE)

    pdb.set_trace()

    print 'How are you?'
    print chatbot.get_response('How are you')
    print 'Are you ok?'
    print chatbot.get_response('Are you ok?')
    print 'Are you alive?'
    print chatbot.get_response('Are you alive?')
    print 'What did you do with Matt?'
    print chatbot.get_response('What did you do with Matt?')