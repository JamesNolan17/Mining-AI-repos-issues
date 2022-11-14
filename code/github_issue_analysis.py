import requests
import pandas as pd
import re
import string
import nltk
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import spacy
db_file = "issueDB_OPEN.csv"
df_issue = pd.read_csv(db_file)
nlp = spacy.load('en_core_web_sm')
tokenizer = AutoTokenizer.from_pretrained("eleldar/language-detection")
model = AutoModelForSequenceClassification.from_pretrained("eleldar/language-detection")
lang_table = {
    "0": "ja",
    "1": "nl",
    "2": "ar",
    "3": "pl",
    "4": "de",
    "5": "it",
    "6": "pt",
    "7": "tr",
    "8": "es",
    "9": "hi",
    "10": "el",
    "11": "ur",
    "12": "bg",
    "13": "en",
    "14": "fr",
    "15": "zh",
    "16": "ru",
    "17": "th",
    "18": "sw",
    "19": "vi"
}

def clean_string(text, stem="None"):
    final_string = ""
    # Make lower
    try:
        text = text.lower()
    except:
        print(text)

    # Remove line breaks
    text = re.sub(r'\n', '', text)
    # Remove puncuation
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    # Remove stop words
    text = text.split()
    useless_words = nltk.corpus.stopwords.words("english")
    useless_words = useless_words + ['hi', 'im']
    text_filtered = [word for word in text if not word in useless_words]
    # Remove numbers
    text_filtered = [re.sub(r'\w*\d\w*', '', w) for w in text_filtered]
    # Stem or Lemmatize
    if stem == 'Stem':
        stemmer = PorterStemmer()
        text_stemmed = [stemmer.stem(y) for y in text_filtered]
    elif stem == 'Lem':
        lem = WordNetLemmatizer()
        text_stemmed = [lem.lemmatize(y) for y in text_filtered]
    elif stem == 'Spacy':
        text_filtered = nlp(' '.join(text_filtered))
        text_stemmed = [y.lemma_ for y in text_filtered]
    else:
        text_stemmed = text_filtered
    final_string = ' '.join(text_stemmed)
    return final_string

def detect_lang(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    scores = outputs.logits.softmax(dim=1)
    scores = scores.tolist()[0]
    score_table = {lang_table[str(i)]: scores[i] for i in range(len(scores))}
    score_table = dict(sorted(score_table.items(), key=lambda item: item[1], reverse=True))
    return score_table

non_en_count = 0

for index, issue in df_issue.iterrows():
    if df_issue.at[index, "English"] in [True, False]:
        continue
    text = clean_string(issue["Title"], stem="Spacy")
    lang_result = detect_lang(text)
    print(f"{index}-{lang_result}")
    df_issue.at[index, "English"] = (list(lang_result.keys())[0] == 'en')
    df_issue.at[index, "Language_Prediction"] = str(lang_result.keys())
    if list(lang_result.keys())[0] != 'en':
        non_en_count += 1
    if index % 500 == 0:
        print(f"Saving at {index}")
        df_issue.to_csv(db_file, index=False)
df_issue.to_csv(db_file, index=False)
print(non_en_count / len(df_issue))