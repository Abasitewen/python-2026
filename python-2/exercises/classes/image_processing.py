from matplotlib import pyplot as plt
import numpy as np

class Image():
    """General class for an image to be read and shown with pyplot."""

    def __init__(self, file_name: str = None) -> None:
        """Initialize class, accepts a file name as argument."""
        if file_name is not None:
            self.load(file_name)

    def load(self, file_name: str) -> None:
        """Load file as image."""
        self.filename = file_name
        self.image = plt.imread(file_name)

    def show(self) -> None:
        """Plot image."""
        plt.imshow(self.image)
        plt.xlabel("")
        plt.ylabel("")
        plt.xticks([])
        plt.yticks([])
        plt.title("Image")
        plt.show()


class JPGImage(Image):
    """Class for 3-channel jpg images with photography editing tools. Inherits from Image."""

    def load(self, file_name: str) -> None:
        """Load file as image."""
        super().load(file_name)
        self.dtype = "uint8"
        self.black = 0
        self.white = 255
        self.range = self.white - self.black
        self.midpoint = self.black + self.range/2.
        self.is_bw = False

    def histogram(self) -> None:
        """Print histogram of exposure values."""
        if self.is_bw:
            colors = "black", "black", "black"
        else:
            colors = "r", "g", "b"
        alpha = 0.15
        channel_values = [self.image[:, :, i].flatten() for i in range(3)]
        histograms = [np.histogram(values, self.range) for values in channel_values]
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
        """Get black and white version of image."""
        bw_image = np.mean(self.image[:, :, :3], axis=-1).astype(self.dtype)
        self.image = np.stack([bw_image]*3, axis=-1)
        self.is_bw = True

