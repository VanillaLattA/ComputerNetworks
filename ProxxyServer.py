from socket import *
import os
# Optional: take ip address and port as command line arguments or 
# hardcode them in your program, you have various options: localhost,
# custom ip address or ip address of your machine, the latter lets you
# access your server from other devices in the same network

# Create a server socket, bind it to a port and start listening
# use AF_INET for address family and SOCK_STREAM for protocol

serverSocket = socket(AF_INET, SOCK_STREAM)

# Optional but recommended: Print out statements at every significant 
# step of your program, for example: print out the ip address and port
# once you bind the socket
ipAddress = "localhost"
serverPort = 8888
serverSocket.bind((ipAddress, serverPort))

print("socket binded to {}:{}".format(ipAddress,serverPort))

# put the socket into listening mode
serverSocket.listen(1)
print("socket is listening")


def parseURL(url):
    url = url[1:]
    website = url.split("/")
    return website

while True:
    print('Ready to serve...')
    # Establish connection with client
    clientSocket, clientAddress = serverSocket.accept()
    print('Received a connection from:', clientSocket, clientAddress)

    # Receive requests (HTTP GET) from the client
    request = clientSocket.recv(2048)
    # Extract the required information from the client request:
    # eg. webpage and file names
    url = request.split()[1].decode()
    destination = parseURL(url)

    
    try:
        # Check whether the required files exist in the cache
        # if yes,load the file and send a response back to the client
        path = "./cache" + url
        print('Read file from cache')
        with open(path, "rb") as file:
            data = file.read(2048)
            clientSocket.send(data)

        
        # Error handling for file not found in cache
    except IOError:
        # Since the required files were not found in cache,
        # create a socket on the proxy server to send the request
        # to the actual webserver
        proxySocket = socket(AF_INET, SOCK_STREAM)
        try:
            # Connect your client socket to the webserver at port 80
            proxySocket.connect((destination[0], 80))
                
            if len(destination) > 1:
                new_request = ["/" + x for x in destination[1:]]
            else:
                new_request = ["/"]
            # send request to the webserver
            new_request_string = "GET "+"".join(new_request)+" HTTP/1.1\r\nHost: "+ destination[0]+"\r\n\r\n"
            print("".join(new_request))
            proxySocket.sendall(("GET "+"".join(new_request)+" HTTP/1.1\r\nHost: "+ destination[0]+"\r\n\r\n").encode())
            # recieve response from the webserver
            response = proxySocket.recv(2048)
            print("Received response from webserver")
            # relay response back to the client
            clientSocket.send(response)
            print("relayed")

            # Create a new file in the cache for the requested file
            # and save the response for any future requests from the client
            try:
                os.mkdir(os.path.dirname(path))
            except:
                pass
            with open(path) as file:
                file.write(response)



            # Close the client socket
            clientSocket.close()

        except:
           # Unable to connect to the webserver
           print("Unable to connect to the webserver")
