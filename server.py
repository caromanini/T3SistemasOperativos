import socket
import threading
import json

def handle_client(client_socket):
    test_data = load_test()

    if test_data is None:
        print("[*] No hay pruebas disponibles. Se entregará una prueba estandar.")

        test_data = {
            "question1": {
                "question": "Capital de Chile?",
                "options": ["A. London", "B. Paris", "C. Santiago", "D. Madrid"],
                "correct_answer": "C"
            },
            "question2": {
                "question": "Que año es?",
                "options": ["A. 2012", "B. 2023", "C. 1999", "D. 1800"],
                "correct_answer": "B"
            }
        }

    score = 0

    for _, question_data in test_data.items():
        question = question_data["question"]
        options = "\n".join(question_data["options"])

        client_socket.send(question.encode())
        client_socket.send(options.encode())

        response = client_socket.recv(1024).decode().upper()
        correct_answer = question_data["correct_answer"]

        if response == correct_answer:
            score += 1

    client_socket.send(f"Your score: {score}/{len(test_data)}".encode())
    client_socket.send("END_OF_TEST".encode())

    client_socket.close()

def load_test():
    try:
        with open('test.json', 'r') as file:
            test_data = json.load(file)
        return test_data
    
    except FileNotFoundError:
        return None
    
def save_test(test_data):
    with open('test.json', 'w') as file:
        json.dump(test_data, file)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print("[*] Server listening on port 12345")

    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
