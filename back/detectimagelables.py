import google.cloud

def detect_labels(path):
    """Detects labels in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
        return 0
    
    result = []
    for label in labels:
        result += [label.description]
    return result


if __name__ == "__main__":
    # annotate image
    pathToImage = './test_image.jpg'
    resultLables = detect_labels(pathToImage)
    print(resultLables)