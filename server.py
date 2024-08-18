from flask import Flask
from typing import Sequence
from google.cloud import texttospeech as tts
from datetime import datetime
from vision import run_quickstart
from speech import speech_to_text, print_response
from video import process_video_text_and_labels
from text import text_process
from google.cloud import speech
import psycopg2
import os
import uuid
app = Flask(__name__)

conn = psycopg2.connect(database=os.getenv('DATABASE'),
user=os.getenv('USER'),
host =os.getenv('HOST'),
password= os.getenv('PASSWORD'),
port=os.getenv('PORT'))

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

    cur = conn.cursor()
    complaint_info = text_process("Flight delay printer broke")
    unique_id = str(uuid.uuid4())

    # Insert into the PostgreSQL table
    cur.execute("""
        INSERT INTO complaints9(id, complaint, topic, severity)
        VALUES (%s, %s, %s, %s)
    """, (unique_id, complaint_info.get('Complaint Type', ''), complaint_info.get('Topic', ''), complaint_info.get('Severity', '')))
    conn.commit()
    cur.close()
    conn.close()
    return f"<p>{complaint_info}</p>"

@app.route("/fetch")
def fetching():
    try:
        # Use context managers to handle the database connection and cursor
        with psycopg2.connect(
            database="postgres",
            user="postgres",
            host="localhost",
            password="intense1",
            port=5432
        ) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM complaints9;')
                rows = cur.fetchall()
        return f'<p>{rows}</p>'
    except psycopg2.Error as e:
        return f"<p>Error: {e}</p>"

@app.route("/createdb")
def database():
    cur = conn.cursor()

    cur.execute("""CREATE TABLE complaints9(
        id UUID PRIMARY KEY, 
        complaint VARCHAR (200) NOT NULL,
        topic VARCHAR (100) NOT NULL,
        severity VARCHAR (20) NOT NULL
    );
    """)
    # Make the changes to the database persistent
    conn.commit()
    # Close cursor and communication with the database
    cur.close()
    conn.close()
    return '<p> finished </p>'