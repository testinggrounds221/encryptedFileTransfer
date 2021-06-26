import socket

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = "49.205.86.140"

ADDR = (SERVER, PORT)

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"  # msg sent to server to disconnect
DATA_CHUNK = 64

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
except ConnectionRefusedError:
    print("Check Port Number and Address or Server is Unaivalable currently")
    exit()
except:
    print("Server Error")
    exit()


def Encrypt(filename, key):
    file = open(filename, "rb")
    data = file.read()
    file.close()

    data = bytearray(data)
    for index, value in enumerate(data):
        data[index] = value ^ key
    encrypted_filename = "enrypt - " + filename
    file = open(encrypted_filename, "wb")
    file.write(data)
    file.close()
    return encrypted_filename


def terminate_connection():
    print("Client Terminated Gracefullly !")
    client.send(DISCONNECT_MESSAGE)
    client.close()


def sendFile(filename):
    Encrypt(filename, 10)
    encrypted_filename = "enrypt - " + filename
    file = open(encrypted_filename, "rb")
    file_format = encrypted_filename[-3:]
    send_format = file_format.encode(FORMAT)
    send_format += b" " * (HEADER - len(send_format))

    SendData = file.read()
    send_data_lenght = (str)(len(SendData)).encode(FORMAT)
    send_data_lenght += b" " * (1024 - len(send_data_lenght))

    client.send(send_format)
    client.send(send_data_lenght)
    client.send(SendData)

    # print(client.recv(2048).decode(FORMAT))


print('Socket Connection Demonstration. Enter "!EXIT" to terminate connection ')
while True:
    try:
        filename = input("Enter filename with extension:\n")
        if filename == DISCONNECT_MESSAGE:
            terminate_connection()
            break
        if filename[-3:] not in ["jpg", "pdf", "mp3", "txt", "mp4"]:
            print("Invalid File Extension! Try Again")
            continue
        sendFile(filename)
    except KeyboardInterrupt:
        terminate_connection()
        break
    except ConnectionResetError:
        print("Server is Unaivalable currently")
        terminate_connection()
    except ConnectionRefusedError:
        print("Server is Unaivalable currently")
    except:
        print("Unknown Error Occured ! Try Again")
        continue
