import json
import io
from base64 import encodebytes
from PIL import Image
from flask import Flask, jsonify
from flask import Flask
import glob

DIR_NAME = "../images/dataset/*.png"
IMAGES = glob.glob(DIR_NAME)

# Total Images
TOTAL_IMAGES = 15000
# SIZE OF PAGINATION PER PAGE
SIZE = 10
# TOTAL PAGES
TOTAL_PAGES = int(TOTAL_IMAGES / SIZE) + 1
# CACHE HOLDING START AND END LIMIT
PAGINATION_CACHE = {1: {"start": 0, "end": 9}}


def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r')  # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG')  # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')  # encode as base64
    return encoded_img


def load_pagination_cache():
    for i in range(2, TOTAL_PAGES):
        start = PAGINATION_CACHE[i - 1]["start"] + SIZE
        end = PAGINATION_CACHE[i - 1]["end"] + SIZE
        PAGINATION_CACHE[i] = {"start": start, "end": end}


def load_images(page):
    limit = PAGINATION_CACHE[page]
    start = limit["start"]
    end = limit["end"]
    images = IMAGES[start:end]
    payload = []
    for img in images:
        file_name = img.split("/")[-1]
        encoded_img = get_response_image(img)
        payload.append({"name": file_name, "image": encoded_img})

    return jsonify(payload)


def create_app(test_config=None):
    load_pagination_cache()
    app = Flask(__name__)

    @app.route("/image/<page>", methods=['GET'])
    def load_image(page):
        page = int(page)
        if page not in PAGINATION_CACHE:
            return "Page Not Found", 404
        load_images(page)
        try:
            return load_images(page), 200
        except Exception as e:
            print(e)
            return "An occur occured while processing request", 500

    return app
