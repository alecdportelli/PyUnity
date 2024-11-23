from .Server import Server
from Utils.Constants import *
from Utils.Kinematics import *
from Utils.ImgUtils import *
from ML.ModelLoader import ModelLoader

from PIL import Image
from io import BytesIO
import json
import os 
import struct


class RobotServer( Server ):
    def __init__( 
            self, 
            host="127.0.0.1", 
            port=65432, 
            logging=True, 
            collectPath=None, 
            robot=None,
            modelPath=None,
            PROCESS=False
        ):
        super().__init__(host, port, logging)

        ''' Server attributes to save during simulation '''
        self.collectPath = collectPath
        self.robot = robot
        self.i = 0

        self.PROCESS = PROCESS

        self.goalPosition = None  # TODO: Temporary - populate from CNN
        self.robotRotations = None 
        self.eePos = None 

        ''' Create model loader for img processing '''
        if modelPath is not None:
            self.modelLoader = ModelLoader( modelPath=modelPath )


    def Recieve(self):
        """ Start recieving the data """
        try:
            while True:
                '''
                Receive a header byte to determine the type of 
                incoming data (e.g., image or state vector)
                '''
                header = self.conn.recv(1)
                if not header:
                    break

                # Header value
                dataType = header[0]

                if dataType == IMAGE_DATA_TYPE and self.PROCESS:  # Image data
                    self.ReceiveAndProcessImage()
                elif dataType == IMAGE_DATA_TYPE and not self.PROCESS:
                    self.SaveImage()
                elif dataType == STATE_VEC_DATA_TYPE:  # State vector data
                    self.ReceiveStateVector()
                elif dataType == TARGET_PIXEL_POSITION:
                    self.ReceiveTargetPosition()

        except KeyboardInterrupt:
            print("\nServer is shutting down...")
            self.conn.close()
            self.server.close()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close the connection when done
            print("Connection closed.")
            self.conn.close()
            self.Stop()


    def ReceiveAndProcessImage(self):
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

            '''
            TODO: Pass image into trained PyTorch model
            to get the goal position from the image 
            '''
            self.predicted = self.modelLoader.Predict( image )

            self.goalPosition = ConvertPixelCoords2UnityCoords(self.predicted[0][0], self.predicted[0][1])

            print(f"Goal position: {self.goalPosition[0]} --- {self.goalPosition[1]} --- {self.goalPosition[2]}")

            # Do inverse kinematics to determine the angle setpoint
            # to reach the end effector goal position 
            angleCmd = IK3D( 
                # Account for offsets 
                self.goalPosition[0], 
                self.goalPosition[1] - self.robot.BASE_HEIGHT, 
                self.goalPosition[2], 
                
                self.robot.LINK1_LENGTH, 
                self.robot.LINK2_LENGTH 
            )

            # Convert into dictionary
            cmds = {"Link1" : angleCmd[0], "Link2" : angleCmd[1], "Link3" : angleCmd[2]}
            self.SendMessage( cmds )


    def SaveImage(self):
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
                img_path = os.path.join(self.collectPath + 'Imgs/', f"image_{self.i}.png")
                image.save(img_path)
                print(f"Image saved to: {img_path}")
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
            self.robotRotations = stateVector['Rotations']
            self.eePos = stateVector['EndEffectorPosition']


    def ReceiveTargetPosition(self):
        """ Receive state vector data """
        sizeBytes = self.conn.recv(4)
        stateSize = int.from_bytes(sizeBytes, byteorder='little')
        positionData = b""

        while len(positionData) < stateSize:
            packet = self.conn.recv(4096)
            if not packet:
                break
            positionData += packet

        if len(positionData) == stateSize:
            positionJson = positionData.decode("utf-8")
            targetPosition = json.loads(positionJson)
            
            jsonPATH = os.path.join(self.collectPath + "JSON/", f"image_{self.i}.json")
            with open(jsonPATH, 'w') as metadata_file:
                json.dump(targetPosition, metadata_file, indent=4)

            print(f"Metadata saved to: {jsonPATH}")
            self.i += 1


    def SendMessage(self, message):
        """ Send a response back to Unity """
        message_data = json.dumps(message)
        response = message_data.encode('utf-8')
        self.conn.sendall(response)
        print("Sent message:", message_data)
