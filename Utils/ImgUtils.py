import numpy as np


def ConvertPixelCoords2UnityCoords(pixelX, pixelY, imgWidth=256, imgHeight=256):
    unityXMin = -11
    unityXMax = 11
    
    unityYMin = 11
    unityYMax = -11

    # Calculate the ratios
    xRatio = pixelX / imgWidth
    yRatio = pixelY / imgHeight

    # Map ratios to Unity ranges
    unityX = xRatio * (unityXMax - unityXMin) + unityXMin
    unityY = yRatio * (unityYMax - unityYMin) + unityYMin

    return (unityX, 0.5, unityY)

