import numpy as np
import cv2
import socket
import time

# listening to all available interfaces
HOST = '0.0.0.0'
PORT = 65432


def server_stream():

    # setting up the socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5) # listening to a specific number of connections
    print(f"Server listening on {HOST} {PORT}")


    # wait for client connection
    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")


    # opening the webcam
    capture = cv2.VideoCapture(0)   
    if not capture.isOpened():
        print("Error reading frame.")


    # setting up the loop for reading and sending the frames
    try:
        while True:
            ret, frame = capture.read()
            if not ret:
                print("Error loading the frame.")
                break

            # encode the frame to jpeg low quality like quality=50 means higher compression and high quality like quality=90 is lower compression
            result, encoded_frame = cv2.imencode('.jpg', frame)


            if result: 
                # conversion of the encoded frame to bytes
                data = encoded_frame.tobytes()

                # prepend the size of the frame data and send the size of 4 bytes first so, the client knows how much to receive
                size = len(data)
                conn.sendall(size.tobytes(4, 'big'))

                #sending the actual data
                conn.sendall(data)
