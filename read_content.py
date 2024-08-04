import json
import base64
import numpy as np
import cv2
import io


def load_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for key in data:
            if key == 'image':
                continue
            print(f"{key}: {data[f'{key}']}")
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None


def decode_base64_image(base64_string):
    try:
        image_data = base64.b64decode(base64_string)
        print(f"Base64 decoded data length: {len(image_data)}")
        return image_data
    except Exception as e:
        print(f"Error decoding base64 string: {e}")
        return None


def convert_to_numpy_array(image_data):
    try:
        # Use BytesIO to mimic a file object for cv2.imdecode
        image_file = io.BytesIO(image_data)
        image_array = np.frombuffer(image_file.getvalue(), dtype=np.uint8)
        print(f"Image array shape: {image_array.shape}")

        # Decode the image array to an image using OpenCV
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if image is None:
            print("Error: OpenCV failed to decode the image.")
        return image
    except Exception as e:
        print(f"Error converting to NumPy array: {e}")
        return None


def display_image(image):
    if image is not None:
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: Image could not be displayed.")


# Load JSON file
json_filename = 'received_data.json'
json_data = load_json(json_filename)

if json_data:
    # Extract base64 string
    base64_image_string = json_data.get('image')

    if base64_image_string:
        # Decode base64 and convert to image
        image_data = decode_base64_image(base64_image_string)
        if image_data:
            image = convert_to_numpy_array(image_data)
            display_image(image)
        else:
            print("Error: Failed to decode base64 image data.")
    else:
        print("Error: No 'image' key found in JSON data.")
else:
    print("Error: Failed to load JSON data.")
