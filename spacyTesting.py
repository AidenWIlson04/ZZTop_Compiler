import spacy

nlp = spacy.load("en_core_web_sm")


text = "Hello my name is bob"

doc = nlp(text)

for token in doc:
    print(token.text)
