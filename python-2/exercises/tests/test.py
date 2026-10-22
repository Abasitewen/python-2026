from unittest import TestCase
import numpy as np
import image_processing as improc

class TestImageProcessing(TestCase):
    def test_input(self):
        with self.assertRaises(FileNotFoundError):
            x = improc.JPGImage("not_existing.jpg")

    def test_jpg_shape(self):
        x = improc.JPGImage("iris_versicolor.jpg")
        self.assertEqual(x.image.shape[-1], 3)

    def test_jpg_type(self):
        x = improc.JPGImage("iris_versicolor.jpg")
        self.assertEqual(x.image.dtype, "uint8")

    def test_jpg_range(self):
        x = improc.JPGImage("iris_versicolor.jpg")
        self.assertTrue(np.max(x.image) <= 255)
        self.assertTrue(np.min(x.image) >= 0)
