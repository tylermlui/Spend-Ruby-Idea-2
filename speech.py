from google.cloud import speech


def speech_to_text(
    language_code: str, 
    audio_uri: str
) -> speech.RecognizeResponse:
    
    config = speech.RecognitionConfig(
        language_code=language_code,  
    )

    audio = speech.RecognitionAudio(
        uri=audio_uri,  # Use the passed URI for the audio file
    )

    client = speech.SpeechClient()

    response = client.recognize(config=config, audio=audio)

    return response


def print_response(response: speech.RecognizeResponse):
    for result in response.results:
        print(result.alternatives[0].transcript)
    
    return result.alternatives[0].transcript