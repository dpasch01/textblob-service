#!/usr/bin/python

from flask import Flask, request, jsonify
from textblob import TextBlob, Word
from textblob.exceptions import NotTranslated
app = Flask(__name__)

from signal import *

@app.route("/sentiment")
def singularize():
	text = request.args.get('text').strip().encode('utf-8', "ignore")
	blob = TextBlob(text)
	
	return jsonify(blob.sentiment)

@app.route("/singularize")
def sentiment():
	text = request.args.get('text').strip().encode('utf-8', "ignore")
	blob = TextBlob(text)
	
	return jsonify(blob.words.singularize())

@app.route("/lemmatize")
def lemmatize():
	text = request.args.get('text').strip().encode('utf-8', "ignore")
	blob = TextBlob(text)
	
	return jsonify(blob.words.lemmatize())

@app.route("/correct")
def correct():
	text = request.args.get('text').strip().encode('utf-8', "ignore")
	blob = TextBlob(text)
	
	return jsonify({'correct':str(blob.correct())})

@app.route("/spelling")
def spelling():
	text = request.args.get('text').strip().encode('utf-8', "ignore")
	blob = TextBlob(text)

	suggestions = {}
	for token in blob.words:
		word = Word(token)
		suggestions[token] = word.spellcheck()
		
	return jsonify(suggestions)

@app.route("/language")
def language():
	text = request.args.get('text').strip()
	blob = TextBlob(text)
	
	return jsonify({"language":blob.detect_language()})

@app.route("/translate")
def translate():
	text = request.args.get('text').strip()
	l_from = request.args.get('from')
	l_to = request.args.get('to')

	blob = TextBlob(text)

	if l_from is None:
		l_from = blob.detect_language()
	
	try:
		translated = blob.translate(from_lang = l_from, to = l_to)
	except NotTranslated:
		translated = text		

	return jsonify({"translation":str(translated)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8593)


