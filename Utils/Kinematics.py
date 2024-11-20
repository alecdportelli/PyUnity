import numpy as np


def IK2D(x, y, z, l1, l2):
    """
    Calculate the inverse kinematics for a 2-link planar robot.
    
    Parameters:
        x (float): Target x-coordinate of the end-effector.
        y (float): Target y-coordinate of the end-effector.
        l1 (float): Length of the first link.
        l2 (float): Length of the second link.

    Returns:
        tuple: Two possible solutions for (theta1, theta2) in radians along with
        the rotation of the first link (theta_0)
    """
    theta_0 = np.rad2deg( np.arctan2(x, z) )
    horizDist = np.sqrt( x**2 + z**2 )

    d = (horizDist**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2)

    if d < -1 or d > 1:
        raise ValueError("Target point is outside the reachable workspace.")

    # Two possible solutions for theta2
    theta2_1 = np.arccos(d)
    theta2_2 = -np.arccos(d)

    # Corresponding theta1 for each theta2
    k1 = l1 + l2 * np.cos(theta2_1)
    k2 = l2 * np.sin(theta2_1)
    theta1_1 = np.arctan2(y, x) - np.arctan2(k2, k1)

    k1 = l1 + l2 * np.cos(theta2_2)
    k2 = l2 * np.sin(theta2_2)
    theta1_2 = np.arctan2(y, x) - np.arctan2(k2, k1)

    return (theta_0, np.rad2deg(theta1_1), np.rad2deg(theta2_1)), (theta_0, np.rad2deg(theta1_2), np.rad2deg(theta2_2))


def FK2D(l1, l2, theta1, theta2):
    """
    Calculate the forward kinematics for a 2-link planar robot.
    
    Parameters:
        l1 (float): Length of the first link.
        l2 (float): Length of the second link.
        theta1 (float): angle of first joint in DEGREES
        theta2 (float): angle of second joint in DEGREES
        
    Returns:
        x and y position of end effector
    """
    theta1Rad = np.deg2rad(theta1)
    theta2Rad = np.deg2rad(theta2)

    # Forward calculation to verify
    x = l1 * np.cos(theta1Rad) + l2 * np.cos(theta1Rad + theta2Rad)
    y = l1 * np.sin(theta1Rad) + l2 * np.sin(theta1Rad + theta2Rad)

    return x, y
