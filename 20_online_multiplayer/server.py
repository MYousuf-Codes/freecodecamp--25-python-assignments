import socket
import threading
import pickle

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', 5555))
        self.server.listen()
        print("Server started, connecting...")
        
        self.clients = []
        self.players = {}
        self.game_state = {
            "players": {},
            "bullets": [],
            "powerups": []
        }
        
    def handle_client(self, client, addr):
        print(f"New connection from {addr}")
        self.clients.append(client)
        
        # initial game state
        client.send(pickle.dumps(self.game_state))
        
        while True:
            try:
                data = client.recv(4096)
                if not data:
                    break
                    
                player_data = pickle.loads(data)
                self.game_state["players"][addr] = player_data
                
                # Broadcast updated game state to all clients
                for c in self.clients:
                    if c != client:
                        c.send(pickle.dumps(self.game_state))
                        
            except:
                break
                
        print(f"Client {addr} disconnected")
        self.clients.remove(client)
        if addr in self.game_state["players"]:
            del self.game_state["players"][addr]
        client.close()
        
    def start(self):
        while True:
            client, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(client, addr))
            thread.start()

if __name__ == "__main__":
    server = Server()
    server.start() 