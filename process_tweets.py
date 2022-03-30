import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector

import re, string

def get_lang_detector(nlp, name):
    return LanguageDetector()

def spacy_language_detection(text, model):

  pipeline = list(dict(model.pipeline).keys())

  if(not "language_detector" in pipeline):
    Language.factory("language_detector", func=get_lang_detector)
    model.add_pipe("language_detector", last=True)
    
  doc = model(text)

  return doc._.language

def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')    
    return text

def strip_all_entities(text):
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

pre_trained_model = spacy.load("en_core_web_sm")

with open('100000tweet.txt', encoding='utf-8') as tweets:
    i = 0
    with open('proccess_tweets.txt', 'w', encoding='utf-8') as wr:
        for tweet in tweets:
            detection = spacy_language_detection(tweet, pre_trained_model)
            if detection['language'] == 'en' and detection['score'] >= 0.85:
                tweet = strip_all_entities(strip_links(tweet)).rstrip('\n')
                wr.write(f'{tweet}\n')