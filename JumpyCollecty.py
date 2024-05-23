import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Platformer Jumpy & Collecty @Frido")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
ORANGE = (255, 100, 10)
MOON_GLOW = (235, 245, 255)

# Player properties
player_width, player_height = 15, 20
player_x, player_y = 100, HEIGHT - player_height - 100
player_velocity = 5
jump_power = 12.5
gravity = 0.5
max_jumps = 2
jump_height = (jump_power ** 2) / (2 * gravity)  # Calculate max jump height

# Initialize player variables
velocity_y = 0
jumps_left = max_jumps
on_ground = False

# Obstacle properties
obstacle_width, obstacle_height = 40, 40
obstacles = [
    {"rect": pygame.Rect(400, HEIGHT - obstacle_height - 100, obstacle_width, obstacle_height), "dir": 1, "speed": 1},
    {"rect": pygame.Rect(600, HEIGHT - obstacle_height - 200, obstacle_width, obstacle_height), "dir": -1, "speed": 1},
    {"rect": pygame.Rect(200, HEIGHT - obstacle_height - 150, obstacle_width, obstacle_height), "dir": 1, "speed": 1},
    {"rect": pygame.Rect(700, HEIGHT - obstacle_height - 250, obstacle_width, obstacle_height), "dir": -1, "speed": 1},
    {"rect": pygame.Rect(random.randint(0, WIDTH - obstacle_width), HEIGHT - player_height - obstacle_height - 50, obstacle_width, obstacle_height), "dir": 1, "speed": 2}
]

# Item properties
item_width, item_height = 20, 20
initial_items = [
    pygame.Rect(450, HEIGHT - obstacle_height - 130, item_width, item_height),
    pygame.Rect(650, HEIGHT - obstacle_height - 230, item_width, item_height),
    pygame.Rect(250, HEIGHT - obstacle_height - 180, item_width, item_height),
    pygame.Rect(750, HEIGHT - obstacle_height - 280, item_width, item_height),
    pygame.Rect(350, HEIGHT - obstacle_height - 150, item_width, item_height)
]
items = initial_items.copy()

# Counters for collected items
collected_items = 0
total_collected_items = 0

# Timer
game_time = 60  # Game time in seconds
start_ticks = 0

# High score
high_score = 0

# Main game loop
clock = pygame.time.Clock()
running = True
game_active = False

def handle_player_movement(keys):
    global player_x, player_y, velocity_y, jumps_left, on_ground
    
    if keys[pygame.K_a]:
        player_x -= player_velocity
        # Wrap-around movement
        if player_x < 0:
            player_x = WIDTH - player_width
    
    if keys[pygame.K_d]:
        player_x += player_velocity
        # Wrap-around movement
        if player_x > WIDTH - player_width:
            player_x = 0
    
    # Apply gravity
    player_y += velocity_y
    velocity_y += gravity
    
    # Check if on ground
    on_ground = False
    for obstacle in obstacles:
        if player_x + player_width > obstacle["rect"].x and player_x < obstacle["rect"].x + obstacle["rect"].width:
            if player_y + player_height >= obstacle["rect"].y and player_y + player_height - velocity_y < obstacle["rect"].y:
                player_y = obstacle["rect"].y - player_height
                velocity_y = 0
                on_ground = True
                jumps_left = max_jumps
                player_x += obstacle["dir"] * obstacle["speed"]
    
    if player_y + player_height >= HEIGHT:
        player_y = HEIGHT - player_height
        velocity_y = 0
        on_ground = True
        jumps_left = max_jumps
    
    if keys[pygame.K_w]:
        if jumps_left > 0:
            velocity_y = -jump_power
            jumps_left -= 1

def handle_obstacles():
    for obstacle in obstacles:
        obstacle["rect"].x += obstacle["dir"] * obstacle["speed"]
        if obstacle["rect"].x <= 0 or obstacle["rect"].x + obstacle_width >= WIDTH:
            obstacle["dir"] *= -1

def handle_item_collisions():
    global items, collected_items, total_collected_items
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    new_items = []
    for item in items:
        if player_rect.colliderect(item):
            collected_items += 1
            total_collected_items += 1
        else:
            new_items.append(item)
    items = new_items

    # Respawn items if all collected
    if len(items) == 0:
        items = initial_items.copy()
        change_obstacles()

def change_obstacles():
    for obstacle in obstacles:
        obstacle["rect"].x = random.randint(0, WIDTH - obstacle_width)
        obstacle["rect"].y = random.randint(HEIGHT // 2, HEIGHT - obstacle_height - 10)
        obstacle["speed"] = random.randint(1, 3)
    # Ensure the special obstacle is within jump height
    special_obstacle = obstacles[-1]
    special_obstacle["rect"].y = HEIGHT - player_height - obstacle_height - 50

def draw_button(screen, text, rect, color, font):
    pygame.draw.rect(screen, color, rect)
    screen.blit(font.render(text, True, BLACK), (rect.x + 20, rect.y + 10))

# Main menu
def main_menu():
    global running, game_active, start_ticks, total_collected_items, items, player_x, player_y, velocity_y, jumps_left, on_ground, collected_items

    font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 50)

    start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 75)
    exit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 75)

    while not game_active and running:
        screen.fill(LIGHT_GRAY)

        title_text = font.render("Jumpy & Collecty", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        draw_button(screen, "Start", start_button_rect, ORANGE, button_font)
        draw_button(screen, "Exit", exit_button_rect, DARK_GRAY, button_font)

        # Display high score
        high_score_text = button_font.render(f'High Score: {high_score}', True, BLACK)
        screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    game_active = True
                    start_ticks = pygame.time.get_ticks()  # Reset timer
                    collected_items = 0  # Reset collected items
                    total_collected_items = 0  # Reset total collected items
                    items = initial_items.copy()  # Reset items
                    player_x, player_y = 100, HEIGHT - player_height - 100  # Reset player position
                    velocity_y = 0
                    jumps_left = max_jumps
                    on_ground = False
                elif exit_button_rect.collidepoint(mouse_pos):
                    running = False

        pygame.display.flip()
        clock.tick(60)

# Run the main menu
main_menu()

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_active:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000  
        if seconds >= game_time:
            game_active = False
            high_score = max(high_score, total_collected_items)
            main_menu()
        else:
            keys = pygame.key.get_pressed()
            handle_player_movement(keys)
            handle_obstacles()
            handle_item_collisions()

            screen.fill(LIGHT_GRAY)

            # Draw player
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
            pygame.draw.rect(screen, MOON_GLOW, player_rect)

            # Draw obstacles
            for obstacle in obstacles:
                pygame.draw.rect(screen, DARK_GRAY, obstacle["rect"])

            # Draw items
            for item in items:
                pygame.draw.rect(screen, ORANGE, item)
                
            # Display remaining time and collected items
            font = pygame.font.Font(None, 36)
            time_text = font.render(f'Time Left: {int(game_time - seconds)}', True, BLACK)
            screen.blit(time_text, (10, 10))
            items_collected_text = font.render(f'Collected Items: {collected_items}', True, BLACK)
            screen.blit(items_collected_text, (10, 50))

            pygame.display.flip()

pygame.quit()
sys.exit()



