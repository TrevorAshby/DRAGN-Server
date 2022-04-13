from chatbots.Chatbot import Chatbot
from transformers import pipeline
import os
import spacy
from spacy.language import Language
from chatbots.fill_temp import fill_templates

# Adam's Spacy pipeline
@Language.component("templater_component")
def templater_component(doc):
    for token in doc:
      #### Adds an attribute called 'is_template' ####
      get_is_template = lambda token: True if token.ent_type_ in ['<PERSON1>', '<LOC1>', '<ORG1>'] else False      
      token.set_extension("is_template", getter=get_is_template, force=True)

      #### Adds an attribute called 'template_text' ####
      get_template_text = lambda token: token.ent_type_ if token.ent_type_ in ['<PERSON1>', '<LOC1>', '<ORG1>'] else token.text
      def set_template_text(token, value): 
        token._.template_text = value  
      token.set_extension("template_text", getter=get_template_text, setter=set_template_text, force=True)
        
    return doc

def insert_newlines(text):
    ## Adds newline every 25 characters
    for i in range(0, len(text), 95):
        text = text[:i] + "\n" + text[i:]

    return text

def doc_to_string(doc):
    doc_long = " ".join([token._.template_text for token in doc])
    return insert_newlines(doc_long)

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("templater_component", name="templater", last=True)



class Kevin(Chatbot):
    def __init__(self):
        #print(os.listdir())
        #! self.generator = pipeline('text-generation', model='./chatbots/gpt2-untemplated-quests', tokenizer='gpt2',config="chatbots\gpt2-untemplated-quests\config.json")
        self.response = None

    def send_message(self):
        print('\nSending message...')

        # Extract the player's message from the json
        plr_full_msg = self.response['text'].split(":")[1]

        # Generate response and parse everything up to the last period to prevent incomplete sentence
        # TODO: Is there a better way to do this?
        #! npc_quest = self.generate(plr_full_msg).rpartition('.')
        #! npc_quest = npc_quest[0] + npc_quest[1]

        # Use spacy pipeline to template quest
        #! doc = nlp(npc_quest)

        # Convert to String
        #! quest_template = doc_to_string(doc)
        #! print("before processing: ", quest_template)

        # Add the 5->Plr message to the front of the string 
        # TODO: Eliminate the need for this
        hard_coded_temp = "Armageddon approaches. Only you can stop it, with the help of <PERSON1>. You must meet them at <LOC1>." #!
        quest_template = "5->Plr: " + hard_coded_temp #!
        #! quest_template = "5->Plr: " + quest_template

        # Replace newlines with spaces to avoid awkward formatting from GPT2
        quest_template = quest_template.replace('\n', ' ')

        print("\nTemplated Quest: ", quest_template)

        filled_in_quest = fill_templates.fill_in(quest_template)
        
        return {"text": filled_in_quest}
        # return {"text": quest_template}

    def recv_message(self, message):
        self.response = message
        return super().recv_message(message)

    def generate(self, input):
        print("Generating message from pipeline...")
        return self.generator(input)[0]['generated_text']

