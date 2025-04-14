import pygame
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
RED = (255, 0, 0)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Load assets
car_img = pygame.image.load("car.jpg")  # Ensure correct path
car_img = pygame.transform.scale(car_img, (50, 100))

road_img = pygame.image.load("road.jpg")  # Add road background
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

# Button dimensions
button_width, button_height = 100, 40
pause_rect = pygame.Rect(WIDTH - 220, 10, button_width, button_height)
stop_rect = pygame.Rect(WIDTH - 110, 10, button_width, button_height)

# Car position (fixed)
car_x, car_y = WIDTH // 2 - 25, HEIGHT - 150

# Background position
road_y1 = 0
road_y2 = -HEIGHT  # Second image for smooth scrolling

# Game variables
speed = 0
max_speed = 10
distance = 0
time_start = 0  # Start after pressing "Start"
paused = False
running = True
game_active = False  # Controls if the game starts

def draw_dashboard():
    font = pygame.font.Font(None, 30)
    time_elapsed = int(time.time() - time_start) if game_active else 0
    speed_text = font.render(f"Speed: {speed:.1f} km/h", True, WHITE)
    distance_text = font.render(f"Distance: {distance} m", True, WHITE)
    time_text = font.render(f"Time: {time_elapsed} s", True, WHITE)
    screen.blit(speed_text, (10, 10))
    screen.blit(distance_text, (10, 40))
    screen.blit(time_text, (10, 70))

def draw_buttons():
    font = pygame.font.Font(None, 30)
    
    # Pause button
    pygame.draw.rect(screen, GRAY, pause_rect)
    pause_text = font.render("Pause", True, BLACK)
    screen.blit(pause_text, (pause_rect.x + 20, pause_rect.y + 10))
    
    # Stop button
    pygame.draw.rect(screen, RED, stop_rect)
    stop_text = font.render("Stop", True, BLACK)
    screen.blit(stop_text, (stop_rect.x + 25, stop_rect.y + 10))

def start_screen():
    global game_active, time_start

    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    text = font.render("Car Racing Game", True, WHITE)
    start_button = pygame.Rect(WIDTH//2 - 75, HEIGHT//2, 150, 50)
    
    while not game_active:
        screen.fill(BLACK)
        screen.blit(text, (WIDTH//2 - 150, HEIGHT//3))
        
        pygame.draw.rect(screen, GRAY, start_button)
        start_text = font.render("Start", True, BLACK)
        screen.blit(start_text, (WIDTH//2 - 40, HEIGHT//2 + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_active = True
                    time_start = time.time()
                    return

def game_loop():
    global speed, distance, road_y1, road_y2, car_x, paused, running

    clock = pygame.time.Clock()
    
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_rect.collidepoint(event.pos):
                    paused = not paused  # Toggle pause state
                if stop_rect.collidepoint(event.pos):
                    running = False  # Stop game when "Stop" is clicked

        if not paused:
            # Handle key inputs
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:  # Accelerate
                speed = min(speed + 0.1, max_speed)
            if keys[pygame.K_s]:  # Brake
                speed = max(speed - 0.2, 0)
            if keys[pygame.K_a]:  # Move left
                car_x = max(car_x - 5, 0)
            if keys[pygame.K_d]:  # Move right
                car_x = min(car_x + 5, WIDTH - 50)

            # Scroll background to simulate movement
            road_y1 += speed
            road_y2 += speed

            if road_y1 >= HEIGHT:
                road_y1 = -HEIGHT
            if road_y2 >= HEIGHT:
                road_y2 = -HEIGHT

            # Move distance counter
            distance += int(speed)

        # Draw scrolling road (looping effect)
        screen.blit(road_img, (0, road_y1))
        screen.blit(road_img, (0, road_y2))

        # Draw car
        screen.blit(car_img, (car_x, car_y))

        # Draw UI
        draw_dashboard()
        draw_buttons()

        # Display pause text if game is paused
        if paused:
            font = pygame.font.Font(None, 50)
            pause_text = font.render("PAUSED", True, WHITE)
            screen.blit(pause_text, (WIDTH//2 - 60, HEIGHT//3))

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

# Run the game
start_screen()
game_loop()
