from google.cloud import videointelligence
import io

def process_video_text_and_labels(input_uri=None, path=None):
    """Detects text and labels in the video using Google Cloud Video Intelligence API."""
    video_client = videointelligence.VideoIntelligenceServiceClient()

    features = [
        videointelligence.Feature.TEXT_DETECTION,
        videointelligence.Feature.LABEL_DETECTION,
    ]

    if input_uri:
        operation = video_client.annotate_video(
            request={
                "features": features,
                "input_uri": input_uri,
            }
        )
    elif path:
        with io.open(path, "rb") as movie:
            input_content = movie.read()
        operation = video_client.annotate_video(
            request={
                "features": features,
                "input_content": input_content,
            }
        )
    else:
        raise ValueError("Either input_uri or path must be provided.")

    print("\nProcessing video for text and label annotations:")
    result = operation.result(timeout=300)
    print("\nFinished processing.")

    segment_labels = result.annotation_results[0].segment_label_annotations
    print("Detected Labels:")

    categories = [category_entity.description for segment_label in segment_labels for category_entity in segment_label.category_entities]
    descriptions = [i.entity.description for i in segment_labels]

    text_annotations = result.annotation_results[0].text_annotations

    print("Detected Text:")
    for i, text_annotation in enumerate(text_annotations):
        print(f"Text {i+1}: {text_annotation.text}")
        print("\n")

    return descriptions, categories


