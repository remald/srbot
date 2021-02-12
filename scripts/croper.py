import os
import uuid
from os import mkdir

from PIL import Image

PATCH_SIZE = 128


def crop(img: Image) -> [Image]:
    patches = []
    width, height = img.size

    patch_width = PATCH_SIZE
    patch_height = PATCH_SIZE

    padded_width = width - PATCH_SIZE
    padded_width = max(min(padded_width, PATCH_SIZE), 0)  # clamp
    padded_height = height - PATCH_SIZE
    padded_height = max(min(padded_height, PATCH_SIZE), 0)  # clamp

    horisontal_step_count = padded_width // PATCH_SIZE + 1
    vertical_step_count = padded_height // PATCH_SIZE + 1
    horisontal_step = padded_width // horisontal_step_count
    vertical_step = padded_height // vertical_step_count

    print(horisontal_step, vertical_step)
    print(horisontal_step_count, vertical_step_count)

    for i in range(0, horisontal_step_count):
        for j in range(0, vertical_step_count):
            cropped = img.crop((i * horisontal_step, j * vertical_step, i * horisontal_step + patch_width, j * vertical_step + patch_height))
            patches.append(cropped)

    return patches


def save_patch(patch):
    try:
        mkdir('train')
    except Exception:
        pass

    for image in patch:
        filename = str(uuid.uuid4())
        image.save('./train/' + filename + '.jpg', quality=100)


def crop_all(path):
    target_dir = os.listdir(path)
    target_dir.sort()
    target_filenames = [os.path.join(path, x) for x in target_dir]
    for img in target_filenames:
        original = Image.open(img)
        p = crop(original)
        save_patch(p)


crop_all('train-src')





