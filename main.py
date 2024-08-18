from typing import Sequence
from google.cloud import texttospeech as tts
import textwrap
import wave
import os
from datetime import datetime

# Ensure that the Google Cloud credentials are set

def unique_languages_from_voices(voices: Sequence[tts.Voice]):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set

def list_languages():
    client = tts.TextToSpeechClient()
    response = client.list_voices()
    languages = unique_languages_from_voices(response.voices)
    print("Languages available:")
    print(f"{len(languages)} languages found.".center(60, "-"))
    for i, language in enumerate(sorted(languages)):
        print(f"{language:>10}", end="\n" if i % 5 == 4 else "")

def text_to_wav(voice_name: str, text: str, output_filename: str, speaking_rate: float = 1.0, speaking_pitch: float = 0.0):
    client = tts.TextToSpeechClient()

    # Set the text input and voice parameters
    synthesis_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code='-'.join(voice_name.split('-')[:2]),  # Extract language code from voice_name
        name=voice_name
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.LINEAR16,
        speaking_rate=speaking_rate,
        pitch=speaking_pitch
    )

    try:
        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice_params,
            audio_config=audio_config
        )

        # Save the audio content to a WAV file
        with open(output_filename, "wb") as out:
            out.write(response.audio_content)
        print(f"Audio content written to file '{output_filename}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

def merge_wav_files(input_files: Sequence[str], output_file: str):
    data = []
    for infile in input_files:
        try:
            with wave.open(infile, 'rb') as w:
                params = w.getparams()
                frames = w.readframes(w.getnframes())
                data.append([params, frames])
        except Exception as e:
            print(f"An error occurred while processing '{infile}': {e}")

    try:
        with wave.open(output_file, 'wb') as output:
            if data:
                output.setparams(data[0][0])
                for params, frames in data:
                    output.writeframes(frames)
            else:
                print(f"No data to write to '{output_file}'.")
    except Exception as e:
        print(f"An error occurred while writing '{output_file}': {e}")

    print(f'Audio content written to {output_file}.')

def main():
    list_languages()

    input_text_file = "input-text.txt"
    if not os.path.exists(input_text_file):
        print(f"Error: '{input_text_file}' does not exist.")
        return

    speaking_rate = float(input("Enter the Speaking Rate (e.g., 1.0): "))
    speaking_pitch = float(input("Enter the Pitch (e.g., 0.0): "))
    voice_name = input("Enter the Speaker Voice (default is 'en-AU-Wavenet-D'): ") or "en-AU-Wavenet-D"

    # Read input text
    with open(input_text_file, 'r', encoding='utf8') as f:
        text = f.read()

    character_length = 1000 + (((speaking_rate - 1) / 0.5) * 1000)
    lines = textwrap.wrap(text, width=character_length, break_long_words=False)

    temp_files = []
    for i, line in enumerate(lines, start=1):
        temp_file = f'temp/File_{i}.wav'
        text_to_wav(voice_name, line, temp_file, speaking_rate, speaking_pitch)
        temp_files.append(temp_file)
        print(f"Got Audio, ({round((i / len(lines)) * 100)}%) done.")

    # Ensure the Output directory exists
    output_directory = 'Output'
    os.makedirs(output_directory, exist_ok=True)

    output_file_name = os.path.join(output_directory, f'Output_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.wav')
    merge_wav_files(temp_files, output_file_name)

    # Clean up temporary files
    for temp_file in temp_files:
        os.remove(temp_file)

if __name__ == "__main__":
    main()
