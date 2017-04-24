# -*- coding: utf-8 -*-
import csv, sys, pdb
from collections import defaultdict

def message_row_to_dict(row):
    KEYS = ['message_id','conversation_id','date','sent_received','number','text']
    return dict(zip(KEYS, row))

def group_messages_to_conversations(messages):
    conversations = defaultdict(list)
    for message in messages:
        conversations[message['conversation_id']].append(message)
    return conversations

def prune_conversations(conversations):
    for conversation_id,conversation in conversations.iteritems():
        # Filter out short conversations, likely from brands.
        if len(conversation) <= 2:
            continue

        print 'NEW CONVERSATION'

        current_text = ''
        has_started = False
        conversation_chat = []
        for curr_message, next_message in zip(conversation[:-1], conversation[1:]):
            # Want to make sure messages I've sent are read as the replies for Chatterbot.
            # Don't start reading until I have received a message.
            if not has_started and curr_message['sent_received'] == 'Sent':
                continue
            elif curr_message['sent_received'] == 'Received':
                has_started = True

            current_text += curr_message['text']
            if curr_message['sent_received'] != next_message['sent_received']:
                # Add this to a list
                conversation_chat.append(current_text)
                current_text = ''
            else:
                pdb.set_trace()
                if len(curr_message['text']) == 0:
                    continue

                last_character = curr_message['text'][len(curr_message['text']) -1]
                if last_character != '.' and last_character != ',':
                    current_text += '.'
                current_text += ' '

        # We went off the end. Add the current message.
        if current_text != '':
            conversation_chat.append(current_text)

        print conversation_chat

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Please include input and output file names.')

    reader = csv.reader(open(sys.argv[1], 'r'))
    input_messages = [message_row_to_dict(row) for row in reader]

    conversations = group_messages_to_conversations(input_messages)

    prune_conversations(conversations)