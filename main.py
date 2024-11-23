from Networking.RobotServer import RobotServer
from Robots.Phugoid7 import Phugoid7

DATA_PATH = "/Users/alecportelli/Desktop/Projects/robotics/AI4RobotFinalProj/TrainingData/"
MODEL_PATH = "/Users/alecportelli/Desktop/Projects/robotics/AI4RobotFinalProj/Models/BlockDetectionModel.pth"


if __name__ == "__main__":
    ''' Build robot '''
    p7 = Phugoid7( "p7", 0, 0.1, 0 ) 

    ''' Create server and start getting msgs '''
    unityServer = RobotServer( collectPath=DATA_PATH, robot=p7, modelPath=MODEL_PATH, PROCESS=True )
    unityServer.Start()
    unityServer.Recieve()
