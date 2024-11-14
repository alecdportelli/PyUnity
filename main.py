from Networking.ImageServer import ImageServer


if __name__ == "__main__":
    unityServer = ImageServer()
    unityServer.Start()
    unityServer.Recieve()
    