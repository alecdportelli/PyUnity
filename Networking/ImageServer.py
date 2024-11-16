from .Server import Server

from PIL import Image
from io import BytesIO
import json
import os 


class ImageServer( Server ):
    def __init__(self, host="127.0.0.1", port=65432, logging=True, collectPath=None):
        super().__init__(host, port, logging)
        self.collectPath = collectPath
        self.i = 0


    def Recieve(self):
        """ Start recieving the data """
        while True:
            # Receive a header byte to determine the type of incoming data (e.g., image or state vector)
            header = self.conn.recv(1)
            if not header:
                break

            # Header value
            dataType = header[0]

            if dataType == 1:  # Image data
                self.ReceiveImage()
            elif dataType == 2:  # State vector data
                self.ReceiveStateVector()
        
        # Close the connection when done
        print("Connection closed.")
        self.conn.close()
        self.Stop()


    def ReceiveImage(self):
        """ Receive image data """
        sizeBytes = self.conn.recv(4)
        imgSize = int.from_bytes(sizeBytes, byteorder='little')
        imgData = b""
        
        while len(imgData) < imgSize:
            packet = self.conn.recv(4096)
            if not packet:
                break
            imgData += packet

        if len(imgData) == imgSize:
            # Process image data
            image = Image.open(BytesIO(imgData))
            if self.collectPath is not None:
                img_path = os.path.join(self.collectPath, f"image_{self.i}.png")
                image.save(img_path)
                print(f"Image saved to: {img_path}")
                self.i += 1
            else:
                print("Image data is incomplete!")


    def ReceiveStateVector(self):
        """ Receive state vector data """
        sizeBytes = self.conn.recv(4)
        stateSize = int.from_bytes(sizeBytes, byteorder='little')
        stateData = b""

        while len(stateData) < stateSize:
            packet = self.conn.recv(4096)
            if not packet:
                break
            stateData += packet

        if len(stateData) == stateSize:
            stateJson = stateData.decode("utf-8")
            # Deserialize JSON to state vector
            stateVector = json.loads(stateJson)
            # Process the state vector as needed
            print(stateVector)