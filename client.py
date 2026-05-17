import socket

HOST = '10.10.10.194'
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print(f"connect to {HOST}")

    # enter name
    user_name = input("name : ")
    client_socket.sendall(user_name.encode())

    # receive welcome message
    welcome_msg = client_socket.recv(1024).decode()
    print(welcome_msg)

    # game loop
    while True:
        # enter choice
        message = input("Enter your choice (rock/paper/scissors): ").strip()
        client_socket.sendall(message.encode())

        # receive result
        result = client_socket.recv(1024).decode()
        print(result)

        # game over check
        if "Game Over" in result:
            print("Connection closed.")
            break