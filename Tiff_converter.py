import tifffile
import numpy as np
import tifffile as tiff

def load_tiff(file, normalise):
    # Read the TIFF image using tifffile
    tiff_image = tifffile.imread(file)

    if normalise:
        lowest=(np.quantile(tiff_image,0.05))
        highest = (np.quantile(tiff_image, 0.95))
        tiff_image[np.where(tiff_image<lowest)]=lowest
        tiff_image[np.where(tiff_image >highest)] = highest
        tiff_image=tiff_image-lowest
        to_div=highest-lowest
    else:
        to_div=4095

    # Convert the image to 8-bit unsigned integer format (0-255)
    image_8bit = ((tiff_image/to_div) * 255).astype(np.uint8)

    return(image_8bit)


def load_multi_tiff(file):
    # Read the TIFF image using tifffile
    tiff_images = tiff.imread(file)

    return tiff.imread(file)


def convert_img(img, normalise):
    if normalise:
        lowest=(np.quantile(img,0.05))
        highest = (np.quantile(img, 0.95))
        img[np.where(img<lowest)]=lowest
        img[np.where(img >highest)] = highest
        img=img-lowest
        to_div=highest-lowest
    else:
        to_div=65535

    # Convert the image to 8-bit unsigned integer format (0-255)
    image_8bit = ((img/to_div) * 255).astype(np.uint8)

    return(image_8bit)
