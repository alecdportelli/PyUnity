class Robot:
    """
    Represents a robot in a 3D space.

    Attributes:
        name (str): The name of the robot.
        x (float): The x-coordinate of the robot's position.
        y (float): The y-coordinate of the robot's position.
        z (float): The z-coordinate of the robot's position.
    """

    def __init__(self, name, x, y, z):
        """
        Initializes a new Robot instance.

        Args:
            name (str): The name of the robot.
            x (float): The initial x-coordinate of the robot's position.
            y (float): The initial y-coordinate of the robot's position.
            z (float): The initial z-coordinate of the robot's position.
        """
        self.name = name
        
        self.x = x
        self.y = y
        self.z = z
