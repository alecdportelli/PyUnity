import socket


class Server:
    def __init__(self, host="127.0.0.1", port=65432, logging=True):
        """ Set host, port, and logging """
        self.host = host
        self.port = port
        self.logging = logging


    def Start(self):
        """ Start the server """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(1)

        print("Waiting for server...")
        self.conn, self.addr = self.server.accept()
        print(f"Connected to {self.addr}")


    def Recieve(self):
        """ Start recieving the data """
        try:
            while True:
                data = self.conn.recv(1024).decode('utf-8')
                if not data:
                    break

                if self.logging:
                    print(f"Received from Unity: {data}")

        except KeyboardInterrupt:
            print("\nServer is shutting down...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.close_connection()

        print("No longer connected!")
        self.conn.close()
        self.Stop()


    def Stop(self):
        """Close the server socket."""
        if self.server:
            self.server.close()
            print("Server stopped.")