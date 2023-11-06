import os
import secrets
from pathlib import Path

from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = BASE_DIR / 'productionfiles'


def save_picture(form_picture):
    """Method to save the documents submitted by the user. It takes an input as a se"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.name)
    picture_fn = random_hex + f_ext
    """
    Here first the picture path is saved in the folder and picture size is mentioned.
    """
    picture_path = f'{STATIC_ROOT}/id_proofs/{picture_fn}'
    output_size = (500, 5000)
    picture = Image.open(form_picture)
    picture.thumbnail(output_size)
    picture.save(picture_path)
    return picture_fn
