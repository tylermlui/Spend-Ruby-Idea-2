from flask import Flask, redirect, url_for, request, render_template_string
from typing import Sequence
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
        return render_template_string('''
                <body>
                    <h1>Complaint Processing Forms</h1>
                    
                    <!-- Text Complaint Form -->
                    <form action="/text" method="POST">
                        <div>Complaint in Text</div>
                        <input type="text" name="complaint" placeholder="Enter complaint">
                        <input type="submit" value="Submit">
                    </form>

                    <!-- Voice Processing Form -->
                    <form action="/voice" method="POST">
                        <input type="text" name="url" placeholder="Enter URL for voice processing">
                        <input type="submit" value="Submit">
                    </form>

                    <!-- Vision Processing Form -->
                    <form action="/vision" method="POST">
                        <input type="text" name="url" placeholder="Enter URL for vision processing">
                        <input type="submit" value="Submit">
                    </form>

                    <!-- Video Processing Form -->
                    <form action="/video" method="POST">
                        <input type="text" name="url" placeholder="Enter URL for video processing">
                        <input type="submit" value="Submit">
                    </form>
                </body>
    ''')

@app.route("/voice", methods=['POST'])
def voice():
    cur = conn.cursor()
    url = request.form['url']
    response = speech_to_text("en", url)
    aggregate = print_response(response)
    process = text_process(aggregate)
    
    unique_id = str(uuid.uuid4())
    
    # Insert into the PostgreSQL table
    cur.execute("""
        INSERT INTO complaints10(id, complaint, topic, severity)
        VALUES (%s, %s, %s, %s)
    """, (unique_id, process.get('Complaint Type', ''), process.get('Topic', ''), process.get('Severity', '')))
    conn.commit()
    cur.close()
    conn.close()
    return f"<p>{process}</p>"

@app.route("/vision", methods=['POST'])
def vision():
    cur = conn.cursor()
    url = request.form['url']
    labels, text = run_quickstart(url)
    combined_list = [label.description for label in labels] + [t.description for t in text]
    print(combined_list)
    process = text_process(combined_list)
    unique_id = str(uuid.uuid4())

    # Insert into the PostgreSQL table
    cur.execute("""
        INSERT INTO complaints9(id, complaint, topic, severity)
        VALUES (%s, %s, %s, %s)
    """, (unique_id, process.get('Complaint Type', ''), process.get('Topic', ''), process.get('Severity', '')))
    conn.commit()
    cur.close()
    conn.close()
    return f"<p>{process}</p>"

@app.route("/video", methods=['POST'])
def video():
    cur = conn.cursor()

    url = request.form['url']
    labels, description = process_video_text_and_labels(url)
    
    # Ensure labels and description are lists of objects with 'description' attributes

    combined_list = labels.extend(description)
    print(combined_list)
    # Process the combined list
    process = text_process(combined_list)
    unique_id = str(uuid.uuid4())

    # Insert into the PostgreSQL table
    cur.execute("""
        INSERT INTO complaints9(id, complaint, topic, severity)
        VALUES (%s, %s, %s, %s)
    """, (unique_id, process.get('Complaint Type', ''), process.get('Topic', ''), process.get('Severity', '')))
    conn.commit()
    cur.close()
    conn.close()
    return f"<p>{process}</p>"

@app.route("/text", methods=['POST'])
def text():

    cur = conn.cursor()
    complaint = request.form['complaint']
    complaint_info = text_process(complaint)
    unique_id = str(uuid.uuid4())

    # Insert into the PostgreSQL table
    cur.execute("""
        INSERT INTO complaints10(id, complaint, topic, severity)
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
                cur.execute('SELECT * FROM complaints10;')
                rows = cur.fetchall()
        return f'<p>{rows}</p>'
    except psycopg2.Error as e:
        return f"<p>Error: {e}</p>"

@app.route("/createdb")
def database():
    cur = conn.cursor()

    cur.execute("""CREATE TABLE complaints10(
        id UUID PRIMARY KEY, 
        complaint VARCHAR (200) NOT NULL,
        topic VARCHAR (100) NOT NULL,
        severity VARCHAR (100) NOT NULL
    );
    """)
    # Make the changes to the database persistent
    conn.commit()
    # Close cursor and communication with the database
    cur.close()
    conn.close()
    return '<p> finished </p>'