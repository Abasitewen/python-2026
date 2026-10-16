from matplotlib import pyplot as plt
import numpy as np
from abc import ABC, abstractmethod

class Image(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def show(self):
        pass

class JpegImage(Image):
    def __init__(self, file_name: str = None) -> None:
        """Initialize class, accepts a file name as argument"""
        if file_name is not None:
            self.load(file_name)
        else:
            print("Initialized empty Picture class, load data with `load` method.")

    def load(self, file_name: str) -> None:
        """Load file as image"""
        self.filename = file_name
        self.image = plt.imread(file_name)
        self.dtype = self.image.dtype
        self.black = np.iinfo(self.dtype).min
        self.white = np.iinfo(self.dtype).max
        self.range = self.white - self.black
        self.midpoint = self.black + self.range/2. 

    def show(self) -> None:
        """Plot image"""
        plt.imshow(self.image)
        plt.xlabel("")
        plt.ylabel("")
        plt.xticks([])
        plt.yticks([])
        plt.title("Image")
        plt.show()

    def commit_edits(self) -> None:
        """Overwrite image with last edit"""
        self.image = self.edited_image

    def histogram(self, single_channel: bool = False, force_bins: bool = False) -> None:
        """Print histogram of exposure values"""
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
        plt.xlim(self.black, self.white)
        plt.ylim(0, max(max_heights)*1.1)
        plt.xticks([self.black, self.midpoint, self.white], ["Blacks", "Mids", "Whites"])
        plt.yticks([])
        plt.show()

    def bw(self) -> None:
        """Get black and white version of image. Needs be committed."""
        self.edited_image = self._bw_filter()

    def contrast(self, shift: float) -> None:
        """Modify contrast passing percentage shift. Needs be committed"""
        self.edited_image = self._contrast_filter(shift)

    def _float_to_uint8(self, float_image: np.array) -> np.array:
        float_image[float_image < self.black] = self.black
        float_image[float_image > self.white] = self.white
        return float_image.astype("uint8")

    def _get_histogram(self, single_channel: bool, force_bins: bool) -> list:
        if single_channel:
            bw_image = self._bw_filter()
            channel_values = [bw_image[:, :, 0].flatten()]
        else:
            channel_values = [self.image[:, :, i].flatten() for i in range(3)]
        return [np.histogram(values, self.range if force_bins else "auto") for values in channel_values]

    def _bw_filter(self) -> np.array:
        single_channel = np.mean(self.image, axis=2).astype("uint8")
        return np.stack([single_channel]*3, axis=-1)

    def _contrast_filter(self, percentage_shift: float) -> np.array:
        float_image = self.image.copy().astype("float")
        float_image += (float_image - self.midpoint) * (percentage_shift / 100.)
        return self._float_to_uint8(float_image)

if __name__ == "__main__":
    picture = JpegImage("/home/jacopo-salvalaggio/Code/mdmc/python-2026/python-1/iris_versicolor.jpg")
    picture.contrast(50)
    picture.commit_edits()
    picture.show()
    picture.histogram(single_channel=False)
    picture.histogram(single_channel=False, force_bins=True)
