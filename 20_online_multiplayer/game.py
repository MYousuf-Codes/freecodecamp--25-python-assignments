import pygame
import socket
import pickle
import threading

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
PLAYER_SPEED = 5
BULLET_SPEED = 7
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.health = 100
        self.score = 0
        
    def move(self, dx, dy):
        self.x = max(0, min(WIDTH - PLAYER_SIZE, self.x + dx))
        self.y = max(0, min(HEIGHT - PLAYER_SIZE, self.y + dy))
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw health bar
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, PLAYER_SIZE, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 10, PLAYER_SIZE * (self.health/100), 5))

class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rect = pygame.Rect(x, y, 10, 10)
        
    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Online Multiplayer Game")
        self.clock = pygame.time.Clock()
        
        # Network setup
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', 5555))
        
        # Game objects
        self.player = Player(WIDTH//2, HEIGHT//2, BLUE)
        self.bullets = []
        self.other_players = {}
        
        # Start network thread
        self.network_thread = threading.Thread(target=self.receive_data)
        self.network_thread.start()
        
    def receive_data(self):
        while True:
            try:
                data = self.client.recv(4096)
                if not data:
                    break
                    
                game_state = pickle.loads(data)
                self.other_players = game_state["players"]
                
            except:
                break
                
    def send_data(self):
        player_data = {
            "x": self.player.x,
            "y": self.player.y,
            "health": self.player.health,
            "score": self.player.score
        }
        self.client.send(pickle.dumps(player_data))
        
    def handle_bullets(self):
        for bullet in self.bullets[:]:
            bullet.move()
            if (bullet.x < 0 or bullet.x > WIDTH or 
                bullet.y < 0 or bullet.y > HEIGHT):
                self.bullets.remove(bullet)
                
    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        dx = mouse_x - self.player.x
                        dy = mouse_y - self.player.y
                        distance = (dx**2 + dy**2)**0.5
                        if distance > 0:
                            dx = dx/distance * BULLET_SPEED
                            dy = dy/distance * BULLET_SPEED
                            self.bullets.append(Bullet(self.player.x, self.player.y, dx, dy))
            
            # Handle player movement
            keys = pygame.key.get_pressed()
            dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * PLAYER_SPEED
            dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * PLAYER_SPEED
            self.player.move(dx, dy)
            
            # Update game state
            self.handle_bullets()
            self.send_data()
            
            # Draw everything
            self.screen.fill(BLACK)
            self.player.draw(self.screen)
            
            for bullet in self.bullets:
                bullet.draw(self.screen)
                
            for player_data in self.other_players.values():
                other_player = Player(player_data["x"], player_data["y"], RED)
                other_player.health = player_data["health"]
                other_player.score = player_data["score"]
                other_player.draw(self.screen)
            
            pygame.display.flip()
            
        self.client.close()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run() 