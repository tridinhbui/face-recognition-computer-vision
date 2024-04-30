import pygame
import sys

# Pygame setup
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Robot Simulation')

# Load images
tri_image = pygame.image.load('buidinhtri/z5390237202615_6a84123bb161b5a651a16ff9ed31adb5.jpg')  # Replace with Tri's image path
bot_image = pygame.image.load('buidinhtri/z5390237202615_6a84123bb161b5a651a16ff9ed31adb5.jpg')  # Replace with the bot's image path

# Scale images
tri_image = pygame.transform.scale(tri_image, (50, 50))
bot_image = pygame.transform.scale(bot_image, (50, 50))

# Initial positions
tri_pos = pygame.math.Vector2(width // 2, height // 2)
bot_pos = pygame.math.Vector2(100, 100)
# Start the face recognition script
import subprocess
subprocess.Popen(['/opt/homebrew/bin/python3', 'tri_recognition.py'])

# Movement simulation
bot_speed = 1

# Simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Read from the signal file
    try:
        with open('signal.txt', 'r') as signal_file:
            signal = signal_file.read().strip()
            move_bot = signal == 'detected'
    except FileNotFoundError:
        pass  # If the file isn't found, don't move the bot

    if move_bot:
        bot_pos += (tri_pos - bot_pos).normalize() * bot_speed
        move_bot = False  # Reset move_bot after movement

    # Draw everything
    screen.fill((255, 255, 255))
    screen.blit(tri_image, tri_pos)
    screen.blit(bot_image, bot_pos)

    pygame.display.flip()
    pygame.time.Clock().tick(60)  # 60 FPS

pygame.quit()
sys.exit()