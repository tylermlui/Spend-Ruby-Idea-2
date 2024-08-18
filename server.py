from flask import Flask
from typing import Sequence
from google.cloud import texttospeech as tts
from datetime import datetime
from vision import run_quickstart
from speech import speech_to_text, print_response
from video import process_video_text_and_labels
from text import text_process
from google.cloud import speech

app = Flask(__name__)

@app.route("/")
def main():
    return "<p>home</p>"

@app.route("/voice")
def voice():
    response = speech_to_text("en", "gs://cloud-samples-data/speech/brooklyn_bridge.flac")
    aggregate = print_response(response)
    process = text_process(aggregate)
    return f"<p>{process}</p>"

@app.route("/vision")
def vision():
    labels,text = run_quickstart("https://cdn.ebaumsworld.com/mediaFiles/picture/2165492/84584090.jpg")
    combined_list = [label.description for label in labels] + [t.description for t in text]
    process = text_process(combined_list)
    return f"<p>{process}</p>"


@app.route("/video")
def video():
    labels, description= process_video_text_and_labels("gs://cloud-samples-data/video/cat.mp4")
    combined_list = [label.description for label in labels] + [d.description for d in description]
    process = text_process(combined_list)
    return f"<p>{process}</p>"

@app.route("/text")
def text():
    response = text_process("Computer broke as and is giving me an issue where i cant log in")
    return f"<p>{response}</p>"
