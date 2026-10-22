from unittest import TestCase
import numpy as np
import image_processing_expanded as improc

class TestImageProcessing(TestCase):
    jpg_image = improc.JPGImage("iris_versicolor.jpg")
    png_image = improc.PNGImage("iris_versicolor.png")

    # General

    def test_input(self):
        with self.assertRaises(FileNotFoundError):
            image = improc.JPGImage("not_existing.jpg")

    def test_save(self):
        with self.assertRaises(ValueError):
            self.jpg_image.save("existing_file")

    # JPG

    def test_jpg_type(self):
        with self.assertRaises(TypeError):
            image = improc.JPGImage("iris_versicolor.png")

    def test_jpg_histogram(self):
        for value in 1.4, [], "ciao":
            with self.assertRaises(TypeError):
                self.jpg_image.histogram(single_channel=value)
            with self.assertRaises(TypeError):
                self.jpg_image.histogram(force_bins=value)

    def test_jpg_contrast(self):
        for value in [], "ciao":
            with self.assertRaises(TypeError):
                self.jpg_image.contrast(shift=value)

    # PNG

    def test_png_type(self):
        with self.assertRaises(TypeError):
            image = improc.PNGImage("iris_versicolor.jpg")

    def test_png_range(self):
        self.assertTrue(np.max(self.png_image.image) <= 1.0)
        self.assertTrue(np.min(self.png_image.image) >= 0.0)

    def test_png_clip_threshold(self):
        for value in [], "ciao":
            with self.assertRaises(TypeError):
                self.png_image.clip(threshold=value, method="black")
        for value in -0.5, 1.5:
            with self.assertRaises(ValueError):
                self.png_image.clip(threshold=value, method="black")

    def test_png_clip_method(self):
        for value in 1.4, [], "ciao":
            with self.assertRaises(ValueError):
                self.png_image.clip(threshold=0.1, method=value)
