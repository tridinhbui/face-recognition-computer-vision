import pygame
import sys
import cv2
import numpy as np
import pickle
import face_recognition

# Pygame and OpenCV setup
pygame.init()
camera_width, camera_height = 640, 480  # Adjust to your webcam's resolution
simulation_width, simulation_height = 800, 600
total_width = camera_width + simulation_width
screen = pygame.display.set_mode(
    (total_width, max(camera_height, simulation_height)))
pygame.display.set_caption('Robot and Camera Simulation')
clock = pygame.time.Clock()  # Clock to manage frame rate

# Load camera and recognition data
video_capture = cv2.VideoCapture(0)
with open('known_face_encodings.pickle', 'rb') as f:
    known_face_encodings = pickle.load(f)
with open('known_face_names.pickle', 'rb') as f:
    known_face_names = pickle.load(f)

# Load and scale images
tri_image = pygame.image.load(
    'buidinhtri/z5390237202615_6a84123bb161b5a651a16ff9ed31adb5.jpg').convert()
bot_image = pygame.image.load(
    'buidinhtri/z5390237202615_6a84123bb161b5a651a16ff9ed31adb5.jpg').convert()
tri_image = pygame.transform.scale(tri_image, (50, 50))
bot_image = pygame.transform.scale(bot_image, (50, 50))

# Initial positions
tri_pos = pygame.math.Vector2(
    simulation_width // 2 + camera_width, camera_height // 2)
bot_pos = pygame.math.Vector2(camera_width + 100, 100)
bot_speed = 5
move_bot = False

# Main loop
running = True

count = 0
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read the next frame from the camera
    ret, frame = video_capture.read()
    if not ret:
        continue  # If frame reading wasn't successful, skip the iteration

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Convert the image to Pygame surface and display it
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    frame = np.rot90(frame)
    frame = np.flipud(frame)
    frame_surface = pygame.surfarray.make_surface(frame)
    screen.blit(frame_surface, (0, 0))

    # Draw the rectangle around each face and check if Tri is detected
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(
            known_face_encodings, face_encoding)
        name = "Stranger"
        box_color = (0, 255, 0)  # Default color for strangers
        

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            if name == "Bui Dinh Tri":
                print("Tri detected", count)
                box_color = (255, 0, 0)  # Color for Tri
                move_bot = True

        # Draw the rectangle around each face
        pygame.draw.rect(screen, box_color, (left, top, right - left, bottom - top), 2)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(name, True, box_color)
        screen.blit(text_surface, (left, top - 30))

    # Update bot position if Tri is detected
    if move_bot:
        print("move bot", count)
        count += 1
        direction = tri_pos - bot_pos
        move_bot = False
        if direction.length() > 0:
            direction = direction.normalize()
            bot_pos += direction * bot_speed
        else:
            move_bot = False  # Stop moving if reached the destination

    # Draw bot and Tri image in the simulation part
    screen.blit(tri_image, tri_pos)
    screen.blit(bot_image, bot_pos)

    pygame.display.flip()  # Update the full display Surface to the screen

    # Print frame rate
    print("FPS:", clock.get_fps())
    clock.tick(30)  # Limit the frame rate to 30 frames per second

video_capture.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
