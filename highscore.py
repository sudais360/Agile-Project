import pygame
import sys
import MySQLdb
import os

import subprocess
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("High Scores")

# Load fonts and images
MAIN_FONT = pygame.font.Font("font/Pixeltype.ttf", 45)
TITLE_FONT = pygame.font.Font("font/Pixeltype.ttf", 50)
BACKGROUND_IMG = pygame.image.load("login_img/plainbg.png")  # Replace with the path to your background image


def get_top_10_scores():
    # Connect to the database
    db = MySQLdb.connect(
        host=os.getenv("HOST"),
        user=os.getenv("DB_USERNAME"),
        passwd=os.getenv("PASSWORD"),
        db=os.getenv("DATABASE"),
        autocommit=True,
        ssl_mode="VERIFY_IDENTITY",
        ssl={
            "ca": os.getenv("SSL_CERT")
        }
    )
    cur = db.cursor()

    # Fetch the top 10 scores
    query = "SELECT username, score FROM registration ORDER BY score DESC LIMIT 10"
    cur.execute(query)
    scores = cur.fetchall()

    db.close()
    return scores

BACK_BUTTON_IMG = pygame.image.load('map_img/backbutton.png')  # Replace with the path to your back button image
BACK_BUTTON_IMG = pygame.transform.scale(BACK_BUTTON_IMG, (100, 100))  # Scale the image to a suitable size


def draw_high_scores(scores):
    # Draw background
    SCREEN.blit(BACKGROUND_IMG, (0, 0))

    # Draw title
    title_surface = TITLE_FONT.render("High Scores", True, (255, 255, 255))
    SCREEN.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 50))


    # Draw high scores
    for index, (username, score) in enumerate(scores):
        text_surface = MAIN_FONT.render(f"{index + 1}. {username}: {score}", True, (255, 255, 255))
        SCREEN.blit(text_surface, (100, 150 + index * 40))

    back_button_rect = SCREEN.blit(BACK_BUTTON_IMG, (10, 10))
    return back_button_rect

user_id = sys.argv[1]
# Main Loop
# Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fetch the high scores from the database and draw everything
    high_scores = get_top_10_scores()
    back_button_rect = draw_high_scores(high_scores)  # Capture the back_button_rect here

    for event in pygame.event.get():  # Add another event loop here to handle the button click
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if back_button_rect.collidepoint(x, y):  # Check if the back button was clicked
                pygame.quit()
                subprocess.run(["python", "choice.py", str(user_id)])
                exit()

    pygame.display.update()

