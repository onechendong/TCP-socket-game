import socket
import random

HOST = '10.10.10.194'
PORT = 8000

def determine_winner(client_choice, server_choice):
    if client_choice == server_choice:
        return "draw"
    elif (client_choice == 'rock' and server_choice == 'scissors') or \
         (client_choice == 'paper' and server_choice == 'rock') or \
         (client_choice == 'scissors' and server_choice == 'paper'):
        return "client win"
    else:
        return "client lose"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Waiting for connection on {HOST}:{PORT}...")

    conn, addr = server_socket.accept()
    with conn:
        print(f"Add connection from {addr}")

        # receive user name
        user_name = conn.recv(1024).decode().strip()
        print(f"Received user_name: {user_name}")

        # return welcome message
        welcome_msg = f"Welcome Game {user_name}"
        conn.sendall(welcome_msg.encode())
        print(f"Sent: {welcome_msg}")

        client_wins = 0

        # game loop
        while client_wins < 3:
            # receive client's choice
            data = conn.recv(1024).decode().strip().lower()
            if not data:
                print("Client disconnected unexpectedly.")
                break

            # check if input is valid
            if data not in ['rock', 'paper', 'scissors']:
                conn.sendall("Invalid input. Please choose rock, paper, or scissors.".encode())
                continue

            # determine server's choice and round result    
            server_choice = random.choice(['rock', 'paper', 'scissors'])
            client_result = determine_winner(data, server_choice)
            
            # result for server
            if client_result == "client win":
                client_wins += 1
                server_result = "server lose"
            elif client_result == "client lose":
                server_result = "server win"
            else:
                server_result = "draw"

            # print round result and send response to client
            print(f"Client: {data}, Server: {server_choice} -> {server_result}")
            response_msg = f"Server choice: {server_choice}, Result: {client_result}"
            
            # check if client wins 3 times
            if client_wins == 3:
                response_msg += "\nCongratulations! You won 3 times. Game Over."
                conn.sendall(response_msg.encode())
                print("Client won 3 times. Game Over.")
                break
            else:
                conn.sendall(response_msg.encode())