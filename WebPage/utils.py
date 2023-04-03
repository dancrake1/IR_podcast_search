import pandas as pd
import numpy as np
import string
import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

#pre_processing query
preprocessing_switches = {'convert_to_lowercase': True,
                            'separate_out_punctuation': True,
                            'remove_punctuation': True,
                            'convert_number_words_to_digits': True,
                            'convert_numbers': True,
                            'remove_stopwords': True,
                            'apply_lemmatization': True,
                            'stem_tokens': False}
def text2int(textnum, numwords={}):
    if not numwords:
        units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):  numwords[word] = (1, idx)
        for idx, word in enumerate(tens):       numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)

    ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}
    ordinal_endings = [('ieth', 'y'), ('th', '')]

    textnum = textnum.replace('-', ' ')

    current = result = 0
    curstring = ""
    onnumber = False
    for word in textnum.split():
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
            onnumber = True
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)

            if word not in numwords:
                if onnumber:
                    curstring += repr(result + current) + " "
                curstring += word + " "
                result = current = 0
                onnumber = False
            else:
                scale, increment = numwords[word]

                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True

    if onnumber:
        curstring += repr(result + current)

    return curstring


# pre-processing
def pre_process(text):
    punctuation_marks = string.punctuation.replace("'", "")

    # converts to lower case
    if preprocessing_switches['convert_to_lowercase']:
        text = text.lower()

    # separate punctuation from words - preserving apostrophe
    if preprocessing_switches['separate_out_punctuation']:
        for c in punctuation_marks:
            text = text.replace(c, ' ' + c + ' ')

    # converting numbers to digits
    if preprocessing_switches["convert_number_words_to_digits"]:
        text = text2int(text)

        # removing numbers
    if preprocessing_switches["convert_numbers"]:
        text = re.sub('\d+', 'NUMBER', text)
        text = text.replace('NUMBER ', '')

    # Tokenize the text
    tokens = text.split()

    # Remove stopwords
    if preprocessing_switches['separate_out_punctuation']:
        stop_words = set(stopwords.words("english"))
        tokens = [token for token in tokens if token not in stop_words]

    # Remove punctuation
    if preprocessing_switches['remove_punctuation']:
        tokens = [token for token in tokens if token not in punctuation_marks]

    # Lemmatize the tokens
    if preprocessing_switches['apply_lemmatization']:
        tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Stem the tokens
    if preprocessing_switches['stem_tokens']:
        tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join(tokens)

