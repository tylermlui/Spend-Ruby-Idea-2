from google.cloud import vision


def run_quickstart(file_uri):

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = file_uri
    
    # Performs label detection on the image file
    label_response = client.label_detection(image=image)
    labels = label_response.label_annotations

    # Performs text detection on the image file
    text_response = client.text_detection(image=image)
    texts = text_response.text_annotations

    return labels, texts

# Call the function
