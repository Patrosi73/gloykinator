import requests
import json
message = "Hello bro"
translate = requests.get(f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&dj=1&source=input&q={message}")
print(translate.text)
gtranslate_result = json.loads(translate.text)
sentences = gtranslate_result['sentences']
print(sentences)
sentences_json = sentences[0]
print(sentences_json)
final_sentence = sentences_json['trans']
print(final_sentence)