import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 12345))

    score = 0

    while True:
        question = client.recv(1024).decode()
        if not question:
            break

        options = client.recv(1024).decode()       
        print(f"{question}\n{options}")

        if options == "END_OF_TEST":
            print("Prueba completada. Saliendo del programa.")
            break

        response = input("Your answer: ").upper()
        client.send(response.encode())

    final_score = client.recv(1024).decode()
    print(final_score)
    client.close()

if __name__ == "__main__":
    start_client()
