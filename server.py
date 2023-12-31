import socket
import threading
import json
import logging
import os
import time
import datetime

BUFFER_SIZE = 1024
SERVER_ADDRESS = ('127.0.0.1', 12345)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def list_tests():
    try:
        test_files = [file for file in os.listdir() if file.endswith(".json")]

        return test_files
    except Exception as e:
        logger.error(f"Error listing tests: {e}")
        return []
    
def send_test_list(client_socket):
    test_list = list_tests()
    if test_list:
        client_socket.send(json.dumps(test_list).encode())
    else:
        client_socket.send("NO_TESTS_AVAILABLE".encode())

def take_test(client_socket, test_name):
    try:
        test_data = load_test(test_name)

        if test_data is None:
            client_socket.send("NO_TEST_FOUND".encode())
            return
        
        client_socket.send("TEST_START".encode())

        score = 0
        start_time = time.time()
        time_aux = False

        time_limit = test_data["question1"]["time_limit"] * 60
        time_left = int(time_limit - (time.time() - start_time))

        for _, question_data in test_data.items():
            question = question_data["question"]
            options = "\n".join(question_data["options"])

            client_socket.send(question.encode())
            client_socket.send(options.encode())

            time_left = time_limit - (time.time() - start_time)
            client_socket.send(f"Time remaining: {str(datetime.timedelta(seconds=int(time_left)))}".encode())

            response = client_socket.recv(BUFFER_SIZE).decode().upper()
            time_left = time_limit - (time.time() - start_time)

            if time_left <= 0:
                print("Time exceeded.")
                time_aux = True
                client_socket.send("TIME_EXCEEDED".encode())
                break

            if response == question_data["correct_answer"]:
                score += 1

        if time_aux:
            client_socket.send("TIME_EXCEEDED".encode())
        else:
            client_socket.send("END_OF_TEST".encode())

        client_socket.send(f"\nYour score: {score}/{len(test_data)}".encode())

    except Exception as e:
        logger.error(f"Error taking test: {e}")

def handle_client(client_socket, lock):
    try:
        while True:
            respuesta_cliente = client_socket.recv(BUFFER_SIZE).decode()

            if respuesta_cliente == "1":
                prueba = client_socket.recv(BUFFER_SIZE).decode()

                if prueba == "CREATE_TEST":
                    create_test(client_socket, lock)

            elif respuesta_cliente == "2":
                send_test_list(client_socket)
                aux = client_socket.recv(BUFFER_SIZE).decode()
                test_choice = client_socket.recv(BUFFER_SIZE).decode()

                if test_choice in list_tests():
                    take_test(client_socket, test_choice)
                else:
                    client_socket.send("INVALID_TEST_CHOICE".encode())

            elif respuesta_cliente == "3":
                logger.info("Terminating connection.")
                client_socket.send("EXIT_APPROVED".encode())
                break
            else:
                logger.warning("Invalid client response.")
        
    except Exception as e:
        logger.error(f"Error handling client: {e}")

    finally:
        client_socket.close()

def create_test(client_socket, lock):
    try:
        test_name = client_socket.recv(BUFFER_SIZE).decode()
        time_limit = int(client_socket.recv(BUFFER_SIZE).decode())
        test_data = {}

        while True:
            question_json = client_socket.recv(BUFFER_SIZE).decode()
            if question_json == "END_OF_TEST_CREATION":
                break

            client_socket.send("ACK".encode())

            question_data = json.loads(question_json)
            with lock:
                test_data[f"question{len(test_data) + 1}"] = question_data

        save_test(test_name, test_data)
        logger.info(f"Test '{test_name}' created successfully")

    except Exception as e:
        logger.error(f"Error creating test: {e}")

def load_test(test_name):
    try:
        with open(f'{test_name}', 'r') as file:
            test_data = json.load(file)
        return test_data

    except FileNotFoundError:
        return None

def save_test(test_name, test_data):
    with open(f'{test_name}.json', 'w') as file:
        json.dump(test_data, file)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(SERVER_ADDRESS)
    server.listen(5)
    logger.info("[*] Server listening on port 12345")

    lock = threading.Lock()

    while True:
        client, addr = server.accept()
        logger.info(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client, lock))
        client_handler.start()

if __name__ == "__main__":
    start_server()
