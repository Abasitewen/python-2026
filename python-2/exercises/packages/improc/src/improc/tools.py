from .images import EditableBitmap, JPGImage, PNGImage
import numpy as np

def stitch_together(
    image_1: EditableBitmap,
    image_2: EditableBitmap,
    strategy: str
) -> EditableBitmap:
    """
    Stitch two images together.

    Parameters
    ----------
    image_1, image_2 : EditableBitmap
        two images to stitch together
    strategy : str
        can either be "horizontal" or "vertical"

    Returns
    -------
    stitched_image : EditableBitmap
        stitched image in .png format
    """
    _images = []
    for image in image_1, image_2:
        if isinstance(image, JPGImage):
            _images.append(image.to_png())
        elif isinstance(image, PNGImage):
            _images.append(image)
        else:
            raise TypeError("image_1 and image_2 must be an instance of either JPGImage or PNGImage")
    if strategy == "vertical":
        stitched_shape = (_images[0].shape[0] + _images[1].shape[0], max(_images[0].shape[1], _images[1].shape[1]), 4)
    elif strategy == "horizontal":
        stitched_shape = (max(_images[0].shape[0], _images[1].shape[0]), _images[0].shape[1] + _images[1].shape[1], 4)
    else:
        raise ValueError(f"strategy must be either 'horizontal' or 'vertical', received {strategy}.")
    stitched_array = np.zeros(stitched_shape, dtype="float32")
    stitched_array[:_images[0].shape[0], :_images[0].shape[1], :] = _images[0].image
    if strategy == "vertical":
        stitched_array[_images[0].shape[0]:, :_images[1].shape[1], :] = _images[1].image
    else:
        stitched_array[:_images[1].shape[0], _images[0].shape[1]:, :] = _images[1].image
    stitched_image = PNGImage()
    stitched_image._load_array(stitched_array)
    return stitched_image
