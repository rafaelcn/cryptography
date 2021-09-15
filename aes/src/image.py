from PIL import Image


class StrippedImage:
    """StrippedImage represents a image with all of its data stripped out.

    This is quite useful in our context, but it only works with bitmap (.bmp)
    images with a header of 54 bytes. There is some properties of the picture in
    this class, better described as:

    - `width`: the width of the image
    - `height`: the height of the image
    - `resolution`: the resolution of the image (width, height)
    - `body`: the body of the image, without the header
    - `size`: the size of the image, specifically, the size of the body of the
      image
    - `path`: the path of the image
    """
    def __init__(self, path):
        self.path = path
        self.header = b''
        self.body = b''

        with Image.open(self.path) as im:
            self.width, self.height = im.size
            self.resolution = (self.width, self.height)

            self.body = im.tobytes()[54:]

            # capture the header of the bitmap image
            self.header = self.body[:54]

        self.size = len(self.body)
