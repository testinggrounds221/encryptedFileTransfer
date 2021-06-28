import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!EXIT"

KEY = 0

FORMAT = "utf-8"

server = socket.socket()
server.bind((SERVER, PORT))


def Decrypt(filename, key):

    file_format = filename.strip()[-3:]
    file = open(filename, "rb")
    data = file.read()
    file.close()

    data = bytearray(data)
    for index, value in enumerate(data):
        data[index] = value ^ key

    file1 = open("decrypted_file." + file_format, "wb")

    file1.write(data)
    file1.close()


def handle_client(conn, addr):  # handle Individual Client
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True

    while connected:
        data_format = conn.recv(64)

        if data_format:
            data_format = data_format.decode(FORMAT)
            if data_format == DISCONNECT_MESSAGE:
                break
            data_length = conn.recv(102400).decode(FORMAT)
            filename = "received_encrypted." + data_format
            file = open(filename, "wb")
            RecvData = conn.recv((int)(data_length))
            file.write(RecvData)
            file.close()
            print(f"Encrypted File has been Received successfully as {filename}\n")
            Decrypt(filename, KEY)
            print("Decrypted File Successfully\n")
            data_format = None
            data_length = None

    conn.close()


def start():
    server.listen()
    print(f"Server is UP on {SERVER}")

    while True:
        conn, addr = server.accept()  # conn -> connection Object, blocking point
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONECTIONS] {threading.active_count() - 1}")


KEY = (int)(input("Enter key for Decrypting : "))
print("SERVER IS STARTING")
start()
# UnicodeDecodeError