# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import csv, pdb
from collections import defaultdict
from dateutil import parser

def message_row_to_dict(row):
    KEYS = ['message_id','conversation_id','date','sent_received','number','text']
    return dict(zip(KEYS, row))

def group_messages_to_conversations(messages):
    conversations = defaultdict(list)
    for message in messages:
        conversations[message['conversation_id']].append(message)
    return conversations

def iterate_and_prune_conversations(conversations):
    pruned_conversations = []
    for conversation_id,conversation in conversations.iteritems():
        # Filter out short conversations, likely from brands.
        if len(conversation) <= 2:
            continue

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
                # Might want to think about whether we include conversations that have long time gaps between them.

                if len(curr_message['text']) == 0:
                    continue

                last_character = curr_message['text'][len(curr_message['text']) -1]
                if last_character != '.' and last_character != ',':
                    current_text += '.'
                current_text += ' '

        # We went off the end. Add the current message.
        if current_text != '':
            conversation_chat.append(current_text)

        if len(conversation_chat) > 1:
            pruned_conversations.append(conversation_chat)

    return pruned_conversations

def prune_conversations(input_file):
    reader = csv.reader(open(input_file, 'r'))
    input_messages = [message_row_to_dict(row) for row in reader]

    conversations = group_messages_to_conversations(input_messages)

    pruned_conversations = iterate_and_prune_conversations(conversations)

    return pruned_conversations


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Please include an input file name.')

    pruned_conversations = prune_conversations(sys.argv[1])

    for conversation in pruned_conversations:
        print 'NEW CONVERSATION'
        for message in conversation:
            print message

        print ''