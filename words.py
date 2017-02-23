# -*- coding: utf8 -*-
# from flask import Flask, request, render_template, jsonify
from flask import Flask, render_template, jsonify
import requests
import logging
# Hay imports locales
# pip install -r requirements.txt

app = Flask(__name__)

@app.route("/home")
def index():
    return render_template("home.html")

@app.route("/word/<word>")
def words(word):
    params = get_params_for_word(word)
    # definition=pelabras.get(word)
    return render_template("words.html", **params)

@app.route("/api/word/<word>")
def api_words(word):
    params = get_params_for_word(word)
    return jsonify(params)

def get_params_for_word(word):
    headers = {
        'app_id':'7b4f6559',
        'app_key':'40bf7509b9f21f11c90e81fc8a75615d'
    }
    response = requests.get("https://od-api.oxforddictionaries.com:443/api/v1/entries/es/" + word.lower(), headers=headers)
    # print(respuesta.text)
    if response.status_code == 200:
        response_dict = response.json()
        results = response_dict["results"][0]
        lexicalEntries = results["lexicalEntries"]
        # definitions = [le["entries"]["senses"][] for le in lexicalEntries]
        definitions = []
        for le in lexicalEntries:
            entries = le["entries"]
            for entry in entries:
                senses = entry["senses"]
                for sense in senses:
                    defs = sense["definitions"]
                    for definition in defs:
                        definitions.append(definition)

        print("Response - - - - - - - - - - - ")
        # print(results.keys())
        #print(response.text)
    else:
        definitions = []
        print('ERROR! - - -')
    # response_dict = response.json()
    # respuesta = respuesta.json()
    params = {
        "word": word,
        "definitions":definitions
        # "definition": respuesta.get("definition")
    }
    return params

if __name__ == "__main__":
    app.run(debug = True)
