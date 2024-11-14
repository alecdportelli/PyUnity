from .Server import Server

import socket
from PIL import Image
from io import BytesIO


class ImageServer( Server ):
    def __init__(self, host="127.0.0.1", port=65432, logging=True):
        super().__init__(host, port, logging)


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
                image.show()
            else:
                print("Image data is incomplete!")
        
        # Close the connection when done
        print("Connection closed.")
        self.conn.close()
        self.Stop()