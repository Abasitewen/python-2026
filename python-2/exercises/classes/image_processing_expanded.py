from matplotlib import pyplot as plt
import numpy as np
from abc import ABC, abstractmethod

# Abstract class definitions

class Bitmap(ABC):
    """Abstract class for any Bitmap that can be read and shown."""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def show(self):
        pass


class EditableBitmap(Bitmap):
    """Abstract class for any Bitmap that can be edited."""

    @abstractmethod
    def commit_edits(self):
        pass
    
    @abstractmethod
    def delete_edits(self):
        pass

    @abstractmethod
    def save(self):
        pass


# Class definitions

class Image(Bitmap):
    """General class for an image to be read and shown with pyplot."""

    def __init__(self, file_name: str = None) -> None:
        """Initialize class, accepts a file name as argument"""
        if file_name is not None:
            self.load(file_name)

    def load(self, file_name: str) -> None:
        """Load file as image"""
        self.filename = file_name
        self._load_array(plt.imread(file_name))

    def show(self) -> None:
        """Plot image"""
        _show_array(self.image)

    @property
    def shape(self) -> tuple[int]:
        return self.image.shape

    # "Private" methods

    def _load_array(self, image_array: np.ndarray) -> None:
        self.image = image_array

    @staticmethod
    def _show_array(image_array) -> None:
        plt.imshow(image_array)
        plt.xlabel("")
        plt.ylabel("")
        plt.xticks([])
        plt.yticks([])
        plt.title("Image")
        plt.show()


class ColorImage(Image):
    """General class for images with at least 3 channels (assumes they are dimensions [:, :, 0-2] of array)"""

    # "Private" methods

    def _monochrome(self, image_array: np.ndarray) -> np.ndarray:
        return np.mean(image_array[:, :, :3], axis=-1).astype(self.dtype)


class EditableColorImage(ColorImage, EditableBitmap):
    """General class for color images that can be edited."""

    def show(self):
        self._show_array(self._image)

    def commit_edits(self) -> None:
        """Overwrite image with last edit."""
        self.image = self.edited_image

    def delete_edits(self) -> None:
        """Delete edits."""
        if hasattr(self, "edited_image"):
            del self.edited_image
        else:
            print("No edits to delete.")

    def save(self, file_name: str) -> None:
        "Save to file."
        plt.imsave(file_name, self.image)

    # "Private" methods

    @property
    def _image(self) -> np.ndarray:
        """Points to the edited version if it exists."""
        if hasattr(self, "edited_image"):
            return self.edited_image
        else:
            return self.image


class JPGImage(EditableColorImage):
    """Class for 3-channel jpg images with photography editing tools. Inherits from Image."""

    def histogram(self, single_channel: bool = False, force_bins: bool = True) -> None:
        """Print histogram of exposure values."""
        if single_channel:
            colors = "black",
            alpha = 0.3
        else:
            colors = "r", "g", "b"
            alpha = 0.15
        histograms = self._get_histogram(single_channel, force_bins)
        max_heights = []
        for histogram, color in zip(histograms, colors):
            bins = histogram[1][:-1]
            values = histogram[0].astype("float")
            plt.plot(bins, values, color=color, lw=2)
            plt.fill_between(bins, values, color=color, lw=0, alpha=alpha)
            max_heights.append(np.max(values[1:-1]))
        plt.xlim(self.black, self.white-1)
        plt.ylim(0, max(max_heights)*1.1)
        plt.xticks([self.black, self.midpoint, self.white-1], ["Blacks", "Mids", "Whites"])
        plt.yticks([])
        plt.show()

    def bw(self) -> None:
        """Get black and white version of image. Needs be committed."""
        self.edited_image = self._bw_filter()

    def contrast(self, shift: float) -> None:
        """Modify contrast passing the shift (a.u.). Needs be committed."""
        self.edited_image = self._contrast_filter(shift)

    def to_png(self) -> EditableBitmap:
        """Adds fourth channel and returns png version of the image."""
        class_png_image = PNGImage()
        class_png_image._load_array(self._cast_to_png())
        return class_png_image

    # "Private" methods

    def _load_array(self, image_array: np.ndarray) -> None:
        super()._load_array(image_array)
        self.dtype = "uint8"
        self.black = 0
        self.white = 255
        self.range = self.white - self.black
        self.midpoint = self.black + self.range/2.

    def _float_to_uint8(self, float_image: np.ndarray) -> np.ndarray:
        float_image[float_image < self.black] = self.black
        float_image[float_image > self.white] = self.white
        return float_image.astype("uint8")

    def _get_histogram(self, single_channel: bool, force_bins: bool) -> list:
        if single_channel:
            bw_image = self._monochrome(self._image)
            channel_values = [bw_image.flatten()]
        else:
            channel_values = [self._image[:, :, i].flatten() for i in range(3)]
        return [np.histogram(values, self.range if force_bins else "auto") for values in channel_values]

    def _bw_filter(self) -> np.ndarray:
        return np.stack([self._monochrome(self.image)]*3, axis=-1)

    def _contrast_filter(self, shift: float) -> np.ndarray:
        float_image = self.image.astype("float")
        deviation = float_image - self.midpoint
        float_image += deviation * (shift / 10.)
        return self._float_to_uint8(float_image)

    def _cast_to_png(self) -> np.ndarray:
        raw_png_image = (self.image.astype("float32") - self.black) / self.range
        raw_png_image = np.concat(
            (raw_png_image, np.ones((self.shape[0], self.shape[1], 1), dtype="float32")),
            axis=-1
        )
        return raw_png_image


class PNGImage(EditableColorImage):
    """Class for 4-channel png images with a clipping tool."""

    def clip(self, threshold: np.float32, method: str = "white") -> None:
        """
        Clip (make transparent) parts of the image.
        
        Parameters
        ----------
        threshold : np.float32
            exposure threshold to use as reference to clip, must be a float between 0 and 1

        method: str
            method for clipping; can either be black (clip everything below threshold) or white (clip everything above threshold)
        """
        self.edited_image = self._clip_filter(threshold, method)

    def to_jpg(self) -> EditableBitmap:
        """Removes fourth channel and returns jpg version of the image."""
        class_jpg_image = JPGImage()
        class_jpg_image._load_array(self._cast_to_jpg())
        return class_jpg_image

    # "Private" methods

    def _load_array(self, image_array: np.ndarray) -> None:
        super()._load_array(image_array)
        self.dtype = "float32"
        self.black = 0.
        self.white = 1.
        self.range = self.white - self.black
        self.midpoint = self.black + self.range/2.

    def _clip_filter(self, threshold: np.float32, method: str) -> np.ndarray:
        mono_image = self._monochrome(self.image)
        if method.lower()[0:5] == "black":
            mask = mono_image < threshold
        elif method.lower()[0:5] == "white":
            mask = mono_image > threshold
        # else: ...
        clipped_image = self.image.copy()
        clipped_image[mask, -1] = 0.
        return clipped_image

    def _cast_to_jpg(self) -> np.ndarray:
        raw_jpg_image = self.image[:, :, :3] * self.image[:, :, 3:4] * 255
        return raw_jpg_image.astype("uint8")

