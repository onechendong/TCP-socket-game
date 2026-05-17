# Concurrent TCP Socket Game (Python)

A multi-threaded client-server Rock-Paper-Scissors game built with Python's `socket` and `threading` libraries. This project serves as a hands-on implementation to explore concurrent networking concepts, thread synchronization, and asynchronous message handling.

## 🚀 Architecture & Features

This repository includes two variations of the game:

### 1. Single-Player Mode (`server.py` & `client.py`)
* **Connection & Authentication:** Establishes a standard IPv4/TCP socket binding. The server authenticates the client via student ID input before unlocking the game loop.
* **Game Loop:** Handles terminal I/O via `sendall()` and `recv()`. The server implements foolproof checks on client inputs, evaluates the round against randomized server choices, and manages the win-state condition (3 wins to terminate).

### 2. Multi-Player Concurrent Mode (`server_multiuser.py` & `client.py`)
* **Concurrent Connections:** The server waits for exactly 2 clients to establish a connection before initiating the game state.
* **Multi-threading & Non-blocking I/O:** During the interaction phase, if a single thread is used, the server blocks while waiting for the first player's input. To solve this, the server spawns independent sub-threads (`t1`, `t2`) for each client, enabling asynchronous reception of inputs.
* **Thread Synchronization (`join()`):** To prevent the server from calculating results before all clients have submitted their choices, `t1.join()` and `t2.join()` are utilized. This forces the main thread to pause and wait, ensuring state consistency across the shared data structures before proceeding to the evaluation logic.

## 🧠 Key Technical Takeaways

This implementation was designed to solidify fundamental concepts necessary for building concurrent backend services:

* **Concurrency Control:** Managed concurrent state transitions safely by dispatching separate threads and synchronizing them using `.join()`. This mimics real-world scenarios where backend services must wait for multiple asynchronous network responses before aggregating data.
* **Preventing Packet Coalescing (TCP Stream Handling):** Because TCP is a stream-oriented protocol, sending data intensively can cause the OS to merge consecutive messages (e.g., round results and next round prompts) into a single packet, leading to parsing errors on the client side. I implemented a strategic `time.sleep(0.5)` delay to force packet separation, ensuring robust message boundary handling.
* **State Management (Shared Memory):** Safely passed shared data structures (dictionaries) across threads to collect client choices.



## 🛠️ How to Run

You will need multiple terminal windows (or tabs) to simulate the server and the clients.

**1. Start the Server**
For the multi-player mode, run the multi-user server script:
```bash
python server_multiuser.py
```
*(The server will start and wait for 2 clients to connect.)*

**2. Start the Clients**
Open two new terminal windows and run the client script in each:
```bash
python client.py
```

**3. Play the Game**
* Enter your username/student ID in each client terminal.
* Once both clients are connected, the 3-round game will begin.
* Follow the on-screen prompts to enter `rock`, `paper`, or `scissors`.

## 📸 Demonstration

* Server
  <img width="866" height="394" alt="image" src="https://github.com/user-attachments/assets/9cc057dc-138c-44ac-b266-148224494377" />

* Clients
  <img width="1287" height="724" alt="圖片1" src="https://github.com/user-attachments/assets/92c3a094-f2cc-4a2f-a37f-b4dee818461d" />
