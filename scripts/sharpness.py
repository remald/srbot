
import os
import shutil

import numpy as np
from PIL import Image


def grad(filename):
    im = Image.open(filename).convert('L')
    array = np.asarray(im, dtype=np.int32)

    gy, gx = np.gradient(array)
    return np.sqrt(gx**2 + gy**2)


def sharpness_max(filename):
    return np.amax(grad(filename))


def sharpness_mean(filename):
    return np.average(grad(filename))


def filter_dataset(src_path, dst_path, mean_threshold=30, max_threshold=120, max_threshold1=140):
    src_files = os.listdir(src_path)
    src_files.sort()
    target_filenames = [os.path.join(src_path, x) for x in src_files]

    for file in target_filenames:
        gradient = grad(file)
        max_sharpness = np.amax(gradient)
        mean_sharpness = np.average(gradient)
        if (mean_sharpness > mean_threshold and max_sharpness > max_threshold) or (max_sharpness > max_threshold1):
            shutil.copy(file, dst_path)

