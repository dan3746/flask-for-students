import os

from PIL import Image
from flask import url_for


def image_is_png(img, app):
    try:
        ext = img.filename.rsplit('.', 1)[1]
        if ext == "png" or ext == "PNG":
            return img.read()
        if ext == "jpg" or ext == "JPG" or ext == "jpeg" or ext == "JPG":
            im = Image.open(img)
            filename = img.filename.rsplit('.', 1)[0]
            im.save(f'./api/blueprints/profile/static/images/{filename}.png')
            with app.open_resource(app.blueprints['profile'].static_folder + f'/images/{filename}.png', "rb") as f:
                im = f.read()
            os.remove(f'./api/blueprints/profile/static/images/{filename}.png')
            return im
        raise Exception(f"Unknown file type: {ext} !!!")
    except Exception as ex:
        print(f"Error with image: {ex}")
        return None
