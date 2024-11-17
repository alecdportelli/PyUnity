from Networking.ImageServer import ImageServer

PATH = "/Users/alecportelli/Desktop/Projects/robotics/AI4RobotFinalProj/Imgs"


if __name__ == "__main__":
    unityServer = ImageServer( collectPath=PATH )
    unityServer.Start()
    unityServer.Recieve()