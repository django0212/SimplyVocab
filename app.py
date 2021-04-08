from flask import Flask, redirect, url_for, render_template, request
import requests
import jsonpath_ng
import json, itertools
import eng_to_ipa as p

"""To run this app, type "python -m flask run" in the terminal, provided that you have named this file "app.py".
In case it is named something else, type "set FLASK_APP=<name of the python file>" before typing "python -m flask run" in the terminal. On Mac or Linux, use "export" instead of "set" for the previous command."""

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    return defn(text)

def defn(name):
    url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/{}".format(name)

    response = requests.get(url)

    entries = response.json()

    try:
        query_word = jsonpath_ng.parse('[0].word[*]')
        for match in query_word.find(entries):
                word = (json.dumps(match.value)).strip('"')

        query_pronun = jsonpath_ng.parse('[0].phonetics[*].text[*]')
        for match in query_pronun.find(entries):
                pronun = json.loads(json.dumps(match.value))
        query_audio = jsonpath_ng.parse('[0].phonetics[*].audio[*]')
        for match in query_audio.find(entries):
                audio_link = (json.dumps(match.value)).strip('"')

        pos = []
        defs = []
        expl = []

        for entry in entries:
            for meaning in entry["meanings"]:
                for definition in meaning["definitions"]:
                    pos.append(meaning["partOfSpeech"]) 
                    defs.append(definition["definition"])
                    if "example" in definition:
                        expl.append(definition["example"])
        ding = itertools.zip_longest(pos, defs, expl)
        aun = None
    except KeyError:
        return render_template("lol.html")
    return render_template("index.html", name=word, pronun=pronun, audio=audio_link, ding=ding, aun=aun)
