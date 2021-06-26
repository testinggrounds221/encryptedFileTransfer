import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!EXIT"

FORMAT = "utf-8"

server = socket.socket()
server.bind(("", PORT))


def Decrypt(filename, key):
    print(type(filename))
    file_format = filename.strip()[-3:]
    file = open(filename, "rb")
    data = file.read()
    file.close()

    data = bytearray(data)
    for index, value in enumerate(data):
        data[index] = value ^ key

    file1 = open("decrypted_file." + file_format, "wb")
    print("decrypted_file." + filename[-3:])
    print(filename)

    file1.write(data)
    file1.close()


def handle_client(conn, addr):  # handle Individual Client
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True

    while connected:
        data_format = conn.recv(64).decode(FORMAT)

        if data_format:
            if data_format == DISCONNECT_MESSAGE:
                break
            data_length = conn.recv(1024).decode(FORMAT)
            filename = "received_encrypted." + data_format
            file = open(filename, "wb")
            RecvData = conn.recv((int)(data_length))
            file.write(RecvData)
            file.close()
            print(f"Encrypted File has been Received successfully as {filename}\n")
            Decrypt(filename, 10)
            print("Decrypted File Successfully\n")

    conn.close()


def start():
    server.listen()
    print(f"Server is UP on {SERVER}")

    while True:
        conn, addr = server.accept()  # conn -> connection Object, blocking point
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONECTIONS] {threading.active_count() - 1}")


print("SERVER IS STARTING")
start()
