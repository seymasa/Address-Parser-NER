import re
from promptify import OpenAI
from promptify import Prompter
import os


def set_sentence(sentence: str):
    character_dict = {'ö': 'o', 'ı': 'i', 'ü': 'u', 'ç': 'c', 'ğ': 'g', 'ş': 's'}
    return ''.join([character_dict.get(char, char) for char in sentence.lower()]).title()


key = os.getenv('key')

# Her kelimeyi capitalize yapıp Turkce karakterleri kaldırınca daha iyi çalışır decoderlar.
sentence = set_sentence("Meşrutiyet cad. 24/5-6 Yenişehir 06640 ANKARA")
print(sentence)
model = OpenAI(key)
nlp_prompter = Prompter(model)

train_model = nlp_prompter.fit('ner.jinja', domain='Address', text_input=sentence, labels=None)

text = train_model['text'].strip('"""')
matches = re.findall(r'\{(.*?)}', text)

results = []

for match in matches:
    if "'branch'" in match:
        continue
    match = match.strip().rstrip(',').split(',')
    match_dict = {}
    for item in match:
        key, value = item.split(':')
        match_dict[key.strip()] = value.strip().strip("'")
    results.append(match_dict)

print(results)

"""
Output:

Mesrutiyet Cad. 24/5-6 Yenisehir 06640 Ankara

           'T'              'E'
0       Street  Meşrutiyet Cad.
1       Building Number  24/5-6
2         City        Yenişehir
3  Postal Code            06640
4      Country           ANKARA

"""