import pygame
import sys
import subprocess


# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
NEW_BUTTON_WIDTH, NEW_BUTTON_HEIGHT = 180, 100  # New dimensions for the buttons
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Single Player vs Multiplayer')

# Create Fonts and Texts
font1 = pygame.font.Font('font/Pixeltype.ttf', 80)
font = pygame.font.Font('font/Pixeltype.ttf', 36)
text_single = font.render('Single Player', True, BLACK)
text_multi = font.render('Multiplayer', True, BLACK)
text_title = font1.render('Choose Your Mode to Play', True, WHITE)  # Title text
text_highscore = font.render('Highscore', True, BLACK)

# Load and Resize Background and Button Images
background_image = pygame.image.load('login_img/plainbg.png')
single_button_image = pygame.image.load('gameassets/button1.png')
single_button_image = pygame.transform.scale(single_button_image, (NEW_BUTTON_WIDTH, NEW_BUTTON_HEIGHT))
multi_button_image = pygame.image.load('gameassets/button1.png')
multi_button_image = pygame.transform.scale(multi_button_image, (NEW_BUTTON_WIDTH, NEW_BUTTON_HEIGHT))

# Calculate text position on the buttons
text_single_x = 100 + (NEW_BUTTON_WIDTH - text_single.get_width()) // 2
text_single_y = 200 + (NEW_BUTTON_HEIGHT - text_single.get_height()) // 2
text_multi_x = 500 + (NEW_BUTTON_WIDTH - text_multi.get_width()) // 2
text_multi_y = 200 + (NEW_BUTTON_HEIGHT - text_multi.get_height()) // 2

# Initialize the Back Button
back_button_image = pygame.image.load('map_img/backbutton.png')
back_button_image = pygame.transform.scale(back_button_image, (100, 100))
back_button_pos = back_button_image.get_rect()

single_image = pygame.image.load('gameassets/single.png')
single_image = pygame.transform.scale(single_image, (NEW_BUTTON_WIDTH, NEW_BUTTON_HEIGHT))  # Scale it if needed
single_image.convert_alpha()  # Convert to a format suitable for quick blitting
single_image.set_colorkey((255, 255, 255))  # Remove white background

multi_image = pygame.image.load('gameassets/multiplayer.png')
multi_image  = pygame.transform.scale(multi_image , (250,150))  # Scale it if needed


highscore_button_image = pygame.image.load('gameassets/button1.png')  # New highscore button
highscore_button_image = pygame.transform.scale(highscore_button_image, (180,100))

# Calculate text position on the highscore button
text_highscore_x = 300 + (180 - text_highscore.get_width()) // 2
text_highscore_y = 400 + (100 - text_highscore.get_height()) // 2  # New y position

highscore_image = pygame.image.load('login_img/high-score.png')  # New highscore button
highscore_image = pygame.transform.scale(highscore_image, (180,100))
 # Position it somewhere suitable
user_id = sys.argv[1]
# Main Loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if single_rect.collidepoint(x, y):
                pygame.quit()
                subprocess.run(["python", "geomap.py",str(user_id)])
                exit()
            elif multi_rect.collidepoint(x, y):
                pygame.quit()
                subprocess.run(["python", "multiplayer.py",str(user_id)])
                exit()
            elif back_button_pos.collidepoint(x, y):
                pygame.quit()
                subprocess.run(["python", "userlogin.py",str(user_id)])
                exit()
            elif highscore_rect.collidepoint(x, y):
                pygame.quit()
                subprocess.run(["python", "highscore.py", str(user_id)])
                exit()
    # Draw Background Image
    screen.blit(background_image, [0, 0])
    screen.blit(text_title, (100, 120))  # Will put the text 50 pixels from the left edge of the screen

    # Draw Buttons
    single_rect = screen.blit(single_button_image, [100, 200])
    multi_rect = screen.blit(multi_button_image, [500, 200])
    back_button_pos.bottomright = (100, 100)
    single_image1 = screen.blit(single_image, [100, 310])
    multi_image1 = screen.blit(multi_image , [500, 310])
    highscore_rect = screen.blit(highscore_button_image, [300, 400])
    highscore_image1 = screen.blit(highscore_image, [300, 500])

    # Draw Texts on Buttons
    screen.blit(text_single, (text_single_x, text_single_y))
    screen.blit(text_multi, (text_multi_x, text_multi_y))
    back_rect = screen.blit(back_button_image, [10, 30])
    screen.blit(text_highscore, (text_highscore_x, text_highscore_y))
    # Refresh screen
    pygame.display.flip()
