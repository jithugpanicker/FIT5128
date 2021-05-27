import socket
import tqdm
import os

# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# create the server socket
# TCP socket
s = socket.socket()

# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print("[*] Listening as {}:{}".format(SERVER_HOST, SERVER_PORT))

# accept connection if there is any
client_socket, address = s.accept() 
# if below code is executed, that means the sender is connected
print("[+] {} is connected.".format(address))

# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)

# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), "Receiving {}".format(filename), unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

# close the client socket
client_socket.close()
# close the server socket
s.close()

stream = os.popen("openssl verify -verbose -CAfile CA_VicRoads.crt {}".format(filename))
output = stream.read()
#print (output)

if output[-3:-1] == "OK":
    print ("\n***************\n\nThe certificate of {} is verified and is safe to communicate.".format(filename))
    stream2 = os.popen("openssl x509 -noout -subject -in {}".format(filename))
    output2 = stream2.read()

    if output2[-11:-1] == "b123de2c4c":
        #print (output2[-11:-1])
        print ("\nThe attributes of the device seem fine to me.")
    else:
        #print (output2[-11:-1])
        print ("\nThe attributes of the device dosn't look great to me.\n")

else:
    print ("***************\n\nThe certificate of {} is not verified. The device can be malicious".format(filename))