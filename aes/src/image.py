from PIL import Image


class EImage:
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
