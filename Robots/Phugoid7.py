import math

from Robots.Robot import Robot


class Phugoid7(Robot):
    """
    Represents the Phugoid7 robot, a three-link robotic arm with specific link lengths,
    joint constraints, and an end effector position. Inherits from the base Robot class.
    """

    def __init__(self, name, x, y, z):
        """
        Initializes a new instance of the Phugoid7 robot with predefined properties.

        Args:
            name (str): The name of the robot.
            x (float): The initial x-coordinate of the robot's position.
            y (float): The initial y-coordinate of the robot's position.
            z (float): The initial z-coordinate of the robot's position.

        Attributes:
            LINK1_LENGTH (float): The length of the first link.
            LINK2_LENGTH (float): The length of the second link.
            BASE_HEIGHT (float): The height of the robot's base.

            LINK_1_MIN (int): Minimum rotation angle (in degrees) for the first link.
            LINK_1_MAX (int): Maximum rotation angle (in degrees) for the first link.
            LINK_2_MIN (int): Minimum rotation angle (in degrees) for the second link.
            LINK_2_MAX (int): Maximum rotation angle (in degrees) for the second link.
            LINK_3_MIN (int): Minimum rotation angle (in degrees) for the third link.
            LINK_3_MAX (int): Maximum rotation angle (in degrees) for the third link.

            link1Rotation (float): Current rotation of the first link.
            link2Rotation (float): Current rotation of the second link.
            link3Rotation (float): Current rotation of the third link.
            endEffectorPos (list[float]): The position [x, y, z] of the robot's end effector.
        """
        super().__init__(name, x, y, z)

        # Link lengths
        self.LINK1_LENGTH = 5
        self.LINK2_LENGTH = 5
        self.BASE_HEIGHT = 1.35
        self.LINK_OFFSET = 0.25

        # Joint constraints
        self.LINK_1_MIN = -180
        self.LINK_1_MAX = 180

        self.LINK_2_MIN = 0
        self.LINK_2_MAX = 35

        self.LINK_3_MIN = 0
        self.LINK_3_MAX = 90

        # Position and rotation
        self.link1Rotation = 0
        self.link2Rotation = 0
        self.link3Rotation = 0
        self.endEffectorPos = [0, 0, 0]
