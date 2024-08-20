import pygame
from character import Character
import subprocess
import sys
def initialize_game():
    pygame.init()
    WIDTH, HEIGHT = 1500, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    world_map = pygame.image.load('map_img/water.png')

    # Create a Character instance
    character = Character('fantasy-chibi-female-sprites-pixel-art/Enchantress/Walk.png', (100, 100), 8, 0, delay=5)

    #character = pygame.transform.flip(pygame.transform.scale(pygame.image.load('map_img/character.png'), (100, 100)),True, False)
    continents = initialize_continents()
    character_pos = [100, 500]
    button = initialize_button(WIDTH, HEIGHT)
    return screen, world_map, character, continents, character_pos, button

def draw_continent_names(screen, continents):
    font = pygame.font.Font('font/Pixeltype.ttf', 36)

    for continent, data in continents.items():
        text_surface = font.render(continent, True, (0, 0, 0))  # Render the continent name in black color
        text_rect = text_surface.get_rect(center=data['rect'].center)  # Center the text in the middle of the continent's rect
        screen.blit(text_surface, text_rect.topleft)

def initialize_continents():
    return {
        'Australia': {
            'image': pygame.transform.scale(pygame.image.load('map_img/australia.png'), (700, 600)),
            'pos': (750, 450),
            'rect': pygame.Rect(1200, 550, 200, 150)
        },
        'Asia': {
            'image': pygame.transform.scale(pygame.image.load('map_img/asia.png'), (2000, 1500)),
            'pos': (0, -300),
            'rect': pygame.Rect(1000, 100, 400, 300)
        },
        'Africa': {
            'image': pygame.transform.scale(pygame.image.load('map_img/africa.png'), (1200, 900)),
            'pos': (400, 300),
            'rect': pygame.Rect(900, 350, 200, 300)
        },
        'Europe': {
            'image': pygame.transform.scale(pygame.image.load('map_img/Europe.png'), (1700, 1500)),
            'pos': (200, -650),
            'rect': pygame.Rect(600, 200, 400, 200)
        },
        'North America': {
            'image': pygame.transform.scale(pygame.image.load('map_img/northamerica.png'), (1700, 1400)),
            'pos': (-550, -700),
            'rect': pygame.Rect(150,100, 400, 400)
        },
        'South America': {
            'image': pygame.transform.scale(pygame.image.load('map_img/southamerica.png'), (1400, 1300)),
            'pos': (-680, -300),
            'rect': pygame.Rect(350,500, 200, 300)
        }
    }

def initialize_button(WIDTH, HEIGHT):
    button_image = pygame.image.load('map_img/button.png')  # Load the button image
    button_image = pygame.transform.scale(button_image, (200, 100))  # Scale the image to 100x50 pixels
    button_pos = button_image.get_rect()  # Get the position and size from the image
    button_pos.bottomright = (WIDTH - 80, HEIGHT )  # Position the button at the bottom right of the screen

    back_button_image = pygame.image.load('map_img/backbutton.png')  # Load the back button image
    back_button_image = pygame.transform.scale(back_button_image, (100, 100))  # Scale the image
    back_button_pos = back_button_image.get_rect()
    back_button_pos.bottomright = (100, 100)  # Position it somewhere suitable

    return button_image, button_pos, back_button_image, back_button_pos

def new_screen():
    screen = pygame.display.set_mode((1500, 800))
    # Add the elements you want in the new screen here
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.flip()

import subprocess
user_id = sys.argv[1]
def gameplay(selected_continent, user_id):
    pygame.quit()
    if selected_continent == "Asia":
        subprocess.run(["python", "asia.py", str(user_id)])
    elif selected_continent == "Africa":
        subprocess.run(["python", "africa.py", str(user_id)])
    elif selected_continent == "South America":
        subprocess.run(["python", "southamerica.py", str(user_id)])
    elif selected_continent == "Europe":
        subprocess.run(["python", "europe.py", str(user_id)])
    elif selected_continent == "North America":
        subprocess.run(["python", "northamerica.py", str(user_id)])
    elif selected_continent == "Africa":
        subprocess.run(["python", "africa.py", str(user_id)])
    elif selected_continent == "Australia":
        subprocess.run(["python", "australia.py", str(user_id)])

def game_loop(screen, world_map, character, continents, character_pos, button, user_id):
    running = True
    target_pos = None
    selected_continent = None
    landed_on_continent = False   # NEW: Flag to check if character has landed on a continent
    character_facing_right = True
    last_flipped_state = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for continent, data in continents.items():
                    if data['rect'].collidepoint(event.pos):
                        center_x = data['rect'].x + data['rect'].width // 4 - character.image.get_width() // 4
                        center_y = data['rect'].y + data['rect'].height // 4 - character.image.get_height() // 4
                        target_pos = (center_x, center_y)
                        selected_continent = continent
                        character.is_moving = True
                        landed_on_continent = False  # Reset the flag
                        break

                        # Check if the button is pressed after landing on a continent
                    if button[1].collidepoint(event.pos) and landed_on_continent:
                        print("Let's Go button clicked!")
                        if selected_continent is not None:
                            gameplay(selected_continent, user_id)
                            return

                    if button[2].get_rect().collidepoint(event.pos):
                        print("Back button clicked!")
                        pygame.quit()
                        subprocess.run(["python", "choice.py", str(user_id)])
                        sys.exit()  # Close the current script
                        return

        # In your game_loop function
        if target_pos:
            # Determine the direction of movement (right or left)
            moving_right = character_pos[0] < target_pos[0]

            # Update orientation
            character_facing_right = moving_right
            if abs(character_pos[0] - target_pos[0]) > 10 or abs(character_pos[1] - target_pos[1]) > 15:
                if character_pos[0] < target_pos[0]:
                    character_pos[0] += 15
                else:
                    character_pos[0] -= 15
                if character_pos[1] < target_pos[1]:
                    character_pos[1] += 15
                else:
                    character_pos[1] -= 15
            else:
                character_pos = list(target_pos)  # snap to target
                print(f'Landed on {selected_continent}...')
                target_pos = None
                character.is_moving = False
                landed_on_continent = True  # Set the flag indicating character has landed

        if character.is_moving:
            character.update()  # Advance the character animation
        else:
            character.image = character.standing_image

        # Flip the image only if the state changes
        if last_flipped_state is None or last_flipped_state != character_facing_right:
            if not character_facing_right:
                character.image = pygame.transform.flip(character.image, True, False)
            last_flipped_state = character_facing_right
        draw(screen, world_map, character, continents, character_pos, button, character_facing_right)

        # Update display
        pygame.display.flip()

    pygame.quit()


def draw(screen, world_map, character, continents, character_pos, button, facing_right):
    screen.blit(world_map, (0, 0))
    for continent, data in continents.items():
        screen.blit(data['image'], data['pos'])

    image_to_draw = character.image
    if not facing_right:
        image_to_draw = pygame.transform.flip(image_to_draw, True, False)

    screen.blit(image_to_draw, character_pos)

    draw_continent_names(screen, continents)

    screen.blit(button[0], button[1].topleft)
    screen.blit(button[2], button[3].topleft)

    # Add a text to the screen
    font = pygame.font.Font('font/Pixeltype.ttf', 80)
    text = font.render("Please choose the Continent", 1, (90, 56, 80))  # color of the text
    screen.blit(text, (500, 0))  # position of the text

def main():
    screen, world_map, character, continents, character_pos, button = initialize_game()
    game_loop(screen, world_map, character, continents, character_pos, button, user_id)

if __name__ == "__main__":
    main()