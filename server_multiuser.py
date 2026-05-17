import socket
import threading
import random
import time

HOST = '10.10.10.194'
PORT = 8000

def get_client_choice(conn, user_name, choices_dict):
    try:
        data = conn.recv(1024).decode().strip().lower()
        if data in ['rock', 'paper', 'scissors']:
            choices_dict[user_name] = data
        else:
            choices_dict[user_name] = 'invalid'
    except:
        choices_dict[user_name] = 'error'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Multi-user Server started on {HOST}:{PORT}")
    print("Waiting for exactly 2 clients to connect...")

    clients = []
    user_names = []

    # request 2 clients to connect and enter their names
    while len(clients) < 2:
        conn, addr = server_socket.accept()
        clients.append(conn)
        
        # receive user name
        name = conn.recv(1024).decode().strip()
        user_names.append(name)
        print(f"Player '{name}' connected from {addr}")
        
        # send welcome message to the newly connected client
        welcome_msg = f"Welcome Game {name}. Waiting for the other player..."
        conn.sendall(welcome_msg.encode())

    # initiate scores for Server and both clients
    scores = {"Server": 0, user_names[0]: 0, user_names[1]: 0}
    for conn in clients:
        conn.sendall("\nBoth players connected! Game starts now. (3 Rounds)\n".encode())

    # game loop for 3 rounds
    for round_num in range(1, 4):
        print(f"\n--- Starting Round {round_num} ---")
        choices = {}

        # wait for clients
        t1 = threading.Thread(target=get_client_choice, args=(clients[0], user_names[0], choices))
        t2 = threading.Thread(target=get_client_choice, args=(clients[1], user_names[1], choices))
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()

        # server randomly chooses rock, paper, or scissors
        server_choice = random.choice(['rock', 'paper', 'scissors'])
        choices["Server"] = server_choice

        print(f"Round {round_num} choices: {choices}")

        unique_choices = set(choices.values())

        round_result_msg = ""
        if len(unique_choices) == 1 or len(unique_choices) == 3 or 'invalid' in unique_choices:
            round_result_msg = "Draw! (No points awarded)"
        
        else:
            if 'rock' in unique_choices and 'scissors' in unique_choices:
                winning_gesture = 'rock'
            elif 'paper' in unique_choices and 'rock' in unique_choices:
                winning_gesture = 'paper'
            else: # scissors and paper
                winning_gesture = 'scissors'

            # find winner(s) and update scores
            winners = [player for player, choice in choices.items() if choice == winning_gesture]
            for w in winners:
                scores[w] += 1
            
            round_result_msg = f"Winners this round: {', '.join(winners)} (+1 pt)"

        # round summary to send to clients
        round_summary = f"\n[Round {round_num} Result]\n"
        round_summary += f"Server: {server_choice} | {user_names[0]}: {choices[user_names[0]]} | {user_names[1]}: {choices[user_names[1]]}\n"
        round_summary += f"-> {round_result_msg}\n"
        
        for conn in clients:
            conn.sendall(round_summary.encode())
            
        # avoid overwhelming clients with messages
        time.sleep(0.5) 

    # game over, send final scoreboard to clients and close connections
    scoreboard = f"\nGame Over! Final Scoreboard:\n"
    scoreboard += f"Name   | Score\n"
    scoreboard += f"-------|-------\n"
    scoreboard += f"Server |  {scores['Server']}\n"
    scoreboard += f"{user_names[0]:<6} |  {scores[user_names[0]]}\n"
    scoreboard += f"{user_names[1]:<6} |  {scores[user_names[1]]}\n"
    scoreboard += f"Disconnecting...\n Game Over"

    print(scoreboard)
    for conn in clients:
        conn.sendall(scoreboard.encode())
        conn.close()

    print("\nServer closed.")