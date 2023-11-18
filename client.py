import socket
import json
import logging

BUFFER_SIZE = 1024
SERVER_ADDRESS = ('127.0.0.1', 12345)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def list_tests(client):
    client.send("LIST_TESTS".encode())
    test_list_json = client.recv(BUFFER_SIZE).decode()
    test_list = json.loads(test_list_json)
    return test_list

def choose_test(client):
    test_list = list_tests(client)
    if not test_list:
        print("No tests available.")
        return None

    print("Available Tests:")
    for i, test_name in enumerate(test_list, start=1):
        print(f"{i}. {test_name}")

    while True:
        try:
            choice = int(input("Choose a test (enter the corresponding number): "))
            if 1 <= choice <= len(test_list):
                return test_list[choice - 1]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def authentication(client):
    while True:
        username = input("Enter username (@miuandes.cl): ")

        if "@miuandes.cl" in username:
            return username
        else:
            print("Please enter a valid username (@miuandes.cl)")

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(SERVER_ADDRESS)

    username = authentication(client)

    if username:
        print("Authentication verified.")
    else:
        print("Authentication failed.")
        client.close()
    
    terminate_client = False

    while not terminate_client:
        print("Options:")
        print("1. Create test")
        print("2. Take test")
        print("3. Exit")

        opciones_cliente = input("Choose option: ")
        client.send(opciones_cliente.encode())

        if opciones_cliente == "1":
            client.send("CREATE_TEST".encode())
            create_test(client)

        elif opciones_cliente == "2":
            test_name = choose_test(client)
            client.send(test_name.encode())

            try:
                test_start = client.recv(1024).decode()
                
                if test_start == "TEST_START":
                    i=1
                    while True:
                        question = client.recv(1024).decode()

                        if question == "END_OF_TEST":
                            print("Test completed.")
                            break
                        elif question == "TIME_EXCEEDED":
                            print("Time exceeded.")
                            break

                        options = client.recv(1024).decode()
                        remaining_time = client.recv(1024).decode()

                        if not question:
                            break

                        print(f"{remaining_time}")
                        print(f"{i}. {question}\n{options}")

                        response = input("Your answer: ").upper()
                        client.send(response.encode())

                        i+=1

                    score = client.recv(1024).decode()
                    print(score)

            except ConnectionAbortedError:
                print("Connection with the server has been terminated.")
                terminate_client = True

        elif opciones_cliente == "3":
            client.send("EXIT_CONNECTION".encode())
            exit = client.recv(1024).decode()

            if exit == "EXIT_APPROVED":
                terminate_client = True

        else:
            logger.warning("Invalid option. Please enter a valid option.")
            continue

    logger.info("Client terminated.")
    client.close()

def create_test(client):
    test_name = input("Enter the name for the test: ")
    client.send(test_name.encode())

    time_limit = int(input("Enter the time limit, in minutes, for the test: "))
    client.send(str(time_limit).encode())

    num_questions = int(input("Enter the number of questions for the test: "))
    for i in range(1, num_questions + 1):
        question = input(f"Enter the question for question {i}: ")
        options = [input(f"Enter option {j} for question {i}: ") for j in ["A", "B", "C", "D"]]
        correct_answer = input(f"Enter the correct answer (A, B, C or D) for question {i}: ").upper()

        question_data = {
            "question": question,
            "options": options,
            "correct_answer": correct_answer,
            "time_limit": time_limit
        }

        client.send(json.dumps(question_data).encode())

        ack = client.recv(BUFFER_SIZE).decode()
        if ack != "ACK":
            logger.error("Error: Server did not acknowledge the data. Test creation failed.")
            return

    client.send("END_OF_TEST_CREATION".encode())

    logger.info("Test created successfully")

if __name__ == "__main__":
    start_client()
