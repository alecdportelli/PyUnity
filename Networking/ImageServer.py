from .Server import Server

from PIL import Image
from io import BytesIO
import os


class ImageServer( Server ):
    def __init__(self, host="127.0.0.1", port=65432, logging=True, collectPath=None):
        super().__init__(host, port, logging)
        self.collectPath = collectPath
        self.i = 0


    def Recieve(self):
        """ Start recieving the data """
        while True:
            # Receive the image size (4 bytes)
            sizeBytes = self.conn.recv(4)
            if not sizeBytes:
                break

            # Convert size bytes to integer (image size)
            imgSize = int.from_bytes(sizeBytes, byteorder='little')
            print(f"Receiving image of size: {imgSize} bytes")

            # Receive the image data in chunks
            imgData = b""
            while len(imgData) < imgSize:
                packet = self.conn.recv(4096)  # Receive in chunks
                if not packet:
                    break
                imgData += packet

            if len(imgData) == imgSize:
                # Convert the received byte data to an image
                image = Image.open(BytesIO(imgData))
                # image.show() # TODO: Can process more here

                if self.collectPath is not None:
                    imgPath = os.path.join(self.collectPath, f'img_{self.i}.png')
                    image.save(imgPath)
                    self.i += 1
            else:
                print("Image data is incomplete!")
        
        # Close the connection when done
        print("Connection closed.")
        self.conn.close()
        self.Stop()