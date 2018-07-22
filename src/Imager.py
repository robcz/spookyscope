from PIL import Image
import numpy

class Imager:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    # generate a single RGB image
    def generateOneRGB(self):
        factor = 1
        ih = self.height * factor
        iw = self.width * factor
        # make a pixel array
        pixels = numpy.zeros(shape=(ih, iw, 3), dtype=numpy.uint8)
        # fill it with RGB information
        for columns in pixels:
            for pixel in columns:
                pixel[...] = numpy.random.random_integers(0,255, 3)

        # convert array to image
        img = Image.fromarray(pixels, 'RGB') 

        # return the generated image
        return img

    # generate a single grayscale image
    def generateOneGrey(self):
        factor = 1
        ih = self.height * factor
        iw = self.width * factor
        # make a pixel array
        pixels = numpy.zeros(shape=(ih, iw), dtype=numpy.uint8)
        # fill it with Grey information
        for pixelcols in pixels:
            pixelcols[...] = numpy.random.random_integers(0,255, iw)

        # convert array to image
        img = Image.fromarray(pixels, 'L') 

        # return the generated image
        return img
        
