
import pygame
import sys
from sys import exit
import subprocess
from random import randint, choice

from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb

EDGE_OFFSET = 100

class Question:
    def __init__(self, question, options, correct_option_index):
        self.question = question
        self.options = options
        self.correct_option_index = correct_option_index


    # def display(self, screen):
    #     question_surface = test_font.render(self.question, False, (111, 196, 169))
    #     question_rect = question_surface.get_rect(center=(WIN_WIDTH / 2, 100))
    #     screen.blit(question_surface, question_rect)
    #
    #     self.option_rects = []  # List to store the rects of the options
    #
    #     for index, option in enumerate(self.options):
    #         option_surface = test_font.render(option, False, (111, 196, 169))
    #         option_rect = option_surface.get_rect(center=(WIN_WIDTH / 2, 200 + index * 50))
    #         screen.blit(option_surface, option_rect)
    #
    #         self.option_rects.append(option_rect)

    def display(self, screen):
        max_width = 0.95 * WIN_WIDTH  # Adjust to the preferred width

        # Scale the question font size
        scaled_question_font = get_scaled_font(test_font, self.question, max_width)
        question_surface = scaled_question_font.render(self.question, False, (111, 196, 169))
        question_rect = question_surface.get_rect(center=(WIN_WIDTH / 2, 100))
        screen.blit(question_surface, question_rect)

        self.option_rects = []  # List to store the rects of the options

        for index, option in enumerate(self.options):
            # Scale the options font size
            scaled_option_font = get_scaled_font(test_font, option, max_width)
            option_surface = scaled_option_font.render(option, False, (111, 196, 169))
            option_rect = option_surface.get_rect(center=(WIN_WIDTH / 2, 200 + index * 50))
            screen.blit(option_surface, option_rect)
            self.option_rects.append(option_rect)

    def check_answer(self, user_choice_index):
        return user_choice_index == self.correct_option_index


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # Centering target as before.
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Adjust the offset when the target is within the world's boundaries.
        if EDGE_OFFSET < target.rect.centerx < self.width - EDGE_OFFSET:
            # If the player is on the right half + offset of the screen, move the camera to the right.
            if target.rect.centerx > WIN_WIDTH / 2 + EDGE_OFFSET:
                x -= target.rect.centerx - (WIN_WIDTH / 2 + EDGE_OFFSET)

            # If the player is on the left half - offset of the screen, move the camera to the left.
            elif target.rect.centerx < WIN_WIDTH / 2 - EDGE_OFFSET:
                x += (WIN_WIDTH / 2 - EDGE_OFFSET) - target.rect.centerx

        # Clamp the camera so it doesn't show outside the level.
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIN_WIDTH), x)  # right
        y = max(-(self.height - WIN_HEIGHT), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(
            'fantasy-chibi-female-sprites-pixel-art/Enchantress/run-cut/run1.png').convert_alpha()
        player_walk_2 = pygame.image.load(
            'fantasy-chibi-female-sprites-pixel-art/Enchantress/run-cut/run2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_idle = [
            pygame.image.load('fantasy-chibi-female-sprites-pixel-art/Enchantress/idle-cut/idle2.png').convert_alpha(),
            pygame.image.load(
                'fantasy-chibi-female-sprites-pixel-art/Enchantress/idle-cut/idle2.png').convert_alpha()]  # Add idle frames
        self.player_index = 0
        self.player_jump = pygame.image.load(
            'fantasy-chibi-female-sprites-pixel-art/Enchantress/jump-cut/jump6.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
        self.moving = False  # Track if the player is moving
        self.lives = 3

    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

        if keys[pygame.K_RIGHT] and self.rect.right < WORLD_WIDTH:  # Check for right boundary
            self.rect.x += 5
            self.moving = True
        elif keys[pygame.K_LEFT] and self.rect.left > 0:  # Check for left boundary
            self.rect.x -= 5
            self.moving = True
        else:
            self.moving = False

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        elif self.moving:  # if player is moving, show walk animation
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
        else:  # if player is idle, show idle animation
            self.player_index += 0.1
            if self.player_index >= len(self.player_idle): self.player_index = 0
            self.image = self.player_idle[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load the animation frames for the obstacle/snail
        snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
        snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
        self.frames = [snail_1, snail_2]

        # Animation control
        self.animation_index = 0
        self.image = self.frames[self.animation_index]

        # Position the obstacle character randomly on the x-axis (or specify a fixed position if desired)
        y_pos = 300  # Assuming it stands on the ground
        self.rect = self.image.get_rect(midbottom=(randint(700, 900), y_pos))
        self.lives = 5

    def animate(self):
        # Update the animation index and loop back to 0 if it reaches the end
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animate()

class Obstacle2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load the animation frames for the obstacle/snail
        snail_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
        snail_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
        self.frames = [snail_1, snail_2]

        # Animation control
        self.animation_index = 0
        self.image = self.frames[self.animation_index]

        # Position the obstacle character randomly on the x-axis (or specify a fixed position if desired)
        y_pos = 300  # Assuming it stands on the ground
        self.rect = self.image.get_rect(midbottom=(randint(300, 500), y_pos))
        self.lives = 5

    def animate(self):
        # Update the animation index and loop back to 0 if it reaches the end
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animate()

class Obstacle3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load the animation frames for the obstacle/snail
        knight_1 = pygame.image.load('fantasy-chibi-female-sprites-pixel-art/Knight/idle-cut/tile000.png').convert_alpha()
        knight_2 = pygame.image.load('fantasy-chibi-female-sprites-pixel-art/Knight/idle-cut/tile001.png').convert_alpha()
        knight_3 = pygame.image.load('fantasy-chibi-female-sprites-pixel-art/Knight/idle-cut/tile002.png').convert_alpha()
        knight_4 = pygame.image.load('fantasy-chibi-female-sprites-pixel-art/Knight/idle-cut/tile003.png').convert_alpha()
        knight_5 = pygame.image.load('fantasy-chibi-female-sprites-pixel-art/Knight/idle-cut/tile004.png').convert_alpha()
        knight_6 = pygame.image.load('fantasy-chibi-female-sprites-pixel-art/Knight/idle-cut/tile005.png').convert_alpha()
        self.frames = [knight_1, knight_2, knight_3, knight_4, knight_5, knight_6]

        # Animation control
        self.animation_index = 0
        self.image = self.frames[self.animation_index]

        # Position the obstacle character randomly on the x-axis (or specify a fixed position if desired)
        y_pos = 300  # Assuming it stands on the ground
        self.rect = self.image.get_rect(midbottom=(randint(1000, 1200), y_pos))
        self.lives = 5

    def animate(self):
        # Update the animation index and loop back to 0 if it reaches the end
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animate()

def display_score(time_left):

    min = time_left // 60
    sec = time_left % 60
    time_string = f"{min:02}:{sec:02}"
    score_surf = test_font.render(f'Time left: {time_string}', False, (64, 64, 64))

    # score_surf = test_font.render(f'Score: {score_amt}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    # return score_amt

def time_elapsed():
    time_elapsed = int(pygame.time.get_ticks() / 1000)
    return time_elapsed

def get_random_questions(cursor, count=5):
    query = f"SELECT question, option1, option2, option3, correct_option FROM south_america ORDER BY RAND() LIMIT {count};"
    cursor.execute(query)
    results = cursor.fetchall()

    questions = []
    for result in results:
        question_text, option1, option2, option3, correct_option = result
        questions.append(Question(question_text, [option1, option2, option3], correct_option - 1))
    return questions


def collision_sprite():
    global score

    collided_obstacles = pygame.sprite.spritecollide(player.sprite, obstacle_group, True)

    if not collided_obstacles:  # Return True if no collisions
        return True

    if collided_obstacles:
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

        # Get a random question
        questions = get_random_questions(cur)
        cur.close()
        db.close()

        # Loop over all questions
        for question in questions:
            waiting_for_answer = True
            time_left = 120
            start_ticks = pygame.time.get_ticks()
            prev_second = 0

            while waiting_for_answer and time_left > 0:
                screen.fill((94, 129, 162))
                screen.blit(player.sprite.image, (50, WIN_HEIGHT / 2 - player.sprite.rect.height))
                screen.blit(collided_obstacles[0].image,
                            (WIN_WIDTH - 150, WIN_HEIGHT / 2 - collided_obstacles[0].rect.height))

                player_image_bottom = WIN_HEIGHT / 2 + 50
                obstacle_image_bottom = WIN_HEIGHT / 2 + 50

                # Rendering and positioning player lives
                player_lives_surface = test_font.render(f"hp:{player.sprite.lives}/3", True, (255, 255, 255))
                player_lives_rect = player_lives_surface.get_rect(topleft=(50, player_image_bottom + 10))
                screen.blit(player_lives_surface, player_lives_rect)

                # Rendering and positioning obstacle lives
                obstacle_lives_surface = test_font.render(f"hp:{collided_obstacles[0].lives}/5", True, (255, 255, 255))
                obstacle_lives_rect = obstacle_lives_surface.get_rect(
                    topleft=(WIN_WIDTH - 150, obstacle_image_bottom + 10))
                screen.blit(obstacle_lives_surface, obstacle_lives_rect)

                seconds_gone = (pygame.time.get_ticks() - start_ticks) // 1000
                if seconds_gone != prev_second:
                    time_left -= 1
                    prev_second = seconds_gone

                display_score(time_left)
                question.display(screen)
                pygame.display.update()
                clock.tick(30)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        for idx, rect in enumerate(question.option_rects):
                            if rect.collidepoint(x, y):  # Check if the click was within this option's rectangle
                                correct_answer = question.check_answer(idx)
                                # Exit the loop once an answer is chosen
                                waiting_for_answer = False

                                # Check if the answer is correct
                                if correct_answer:
                                    BASE_SCORE = 5
                                    ALPHA = 0.5
                                    score_increment = BASE_SCORE + ALPHA * time_left
                                    score += score_increment
                                    print("Answer is correct!")
                                    collided_obstacles[0].lives -= 1  # Decrease the obstacle's lives
                                    break
                                else:
                                    print("Answer is incorrect!")
                                    player.sprite.lives -= 1  # Decrease the player's lives
                                    if player.sprite.lives <= 0 or collided_obstacles[0].lives <= 0:
                                        return False  # End the game
                                    else:
                                        break

            if time_left <= 0:
                return False

        return True


user_id = sys.argv[1]
def update_score_in_db(user_id, score):
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

    # Update the score
    query = "UPDATE registration SET score = %s WHERE id = %s"
    cur.execute(query, (score, user_id))

    db.close()

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

in_story_mode = True  # Initially, the story will be shown
show_instructions = False  # Initially, the instructions will not be shown
game_active = False
game_over = False
story_timer = 0  # Initialize a timer for the story text
story_index = 0  # Initialize an index for which line of the story to display
char_index = 0  # Initialize an index for which character to display

def get_scaled_font(original_font, text, max_width):
    # font_size = original_font.get_height()
    font_size = max(original_font.get_height(), 50)
    text_width, _ = original_font.size(text)

    while text_width > max_width:
        font_size -= 1
        smaller_font = pygame.font.Font('font/Pixeltype.ttf', font_size)
        text_width, _ = smaller_font.size(text)

    return pygame.font.Font('font/Pixeltype.ttf', font_size)

def display_instructions(screen, font):
    WIN_WIDTH, WIN_HEIGHT = screen.get_size()
    max_width = 0.95 * WIN_WIDTH  # Adjust this if you want to utilize more or less width for instructions

    instructions = [
        "How to Play:",
        "1. Use the arrow keys to move left and right.",
        "2. If you collide with an obstacle, you'll be presented with a question.",
        "3. Select the correct answer by clicking on one of the three options.",
        "4. An incorrect answer will result in the loss of a life",
        "5. Your score is based on how fast you answer.",
        "Press space to continue..."
    ]

    for index, line in enumerate(instructions):
        scaled_font = get_scaled_font(font, line, max_width)
        text_surface = scaled_font.render(line, False, (111, 196, 169))
        text_rect = text_surface.get_rect(center=(WIN_WIDTH / 2, 50 + index * 40))
        screen.blit(text_surface, text_rect)


def display_game_over(screen, font, score):
    # Screen background
    screen.fill((94, 129, 162))

    # Game Over Text
    game_over_text = font.render('Game Over', False, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WIN_WIDTH / 2 + 150, WIN_HEIGHT / 2 - 100))
    screen.blit(game_over_text, game_over_rect)

    # Score
    score_text = font.render(f'Your Score: {score}', False, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIN_WIDTH / 2 + 150, WIN_HEIGHT / 2))
    screen.blit(score_text, score_rect)

    # Instructions to restart or quit
    instructions_text1 = font.render('Press R to Restart,', False, (255, 255, 255))
    instructions_rect1 = instructions_text1.get_rect(center=(WIN_WIDTH / 2 + 150, WIN_HEIGHT / 2 + 50))
    instructions_text2 = font.render('Q to Quit', False, (255, 255, 255))
    instructions_rect2 = instructions_text2.get_rect(center=(WIN_WIDTH / 2 + 150, WIN_HEIGHT / 2 + 100))

    screen.blit(instructions_text1, instructions_rect1)
    screen.blit(instructions_text2, instructions_rect2)



def display_story(screen, font):
    global story_timer, story_index, char_index  # Declare as global to modify

    screen.fill((0, 0, 0))  # Fill the screen with black to clear previous text

    story_lines = [
        "Welcome to the Grand Odyssey of South America!",
        "A land of ancient civilizations,",
        "lush rainforests, and vibrant cultures.",
        "Dare to embark on this expedition?",
        "Journey through South America's wonders,",
        "from awe-inspiring landmarks",
        "to the challenges of its mysteries.",
        "Claim your place as a true Conquistador.",
        "From the Andes' peaks",
        "to Rio de Janeiro's rhythms,",
        "your wisdom guides your path.",
        "Ready to explore this diverse continent?",
        "Press space to start your South American saga!"
    ]

    # Increment the timer by the time since the last frame
    story_timer += clock.get_time()

    if story_timer > 40:  # 100 milliseconds have passed
        char_index += 1  # Move on to the next character
        story_timer = 0  # Reset the timer

    # If we've displayed all characters of the current line
    if char_index > len(story_lines[story_index]):
        story_index += 1  # Move on to the next line
        char_index = 0  # Reset the character index

    # If we've displayed all lines, reset
    if story_index == len(story_lines):
        story_index = 0

    # Render and display the portion of the text we want to show
    max_width = 0.95 * WIN_WIDTH  # Adjust this if you want to utilize more or less width for story lines

    for index in range(story_index + 1):
        line = story_lines[index]
        if index == story_index:
            line = line[:char_index]  # Only take the portion of the line up to char_index

        # Use scaled font for rendering each line
        scaled_font = get_scaled_font(font, line, max_width)
        text_surface = scaled_font.render(line, False, (255, 255, 255))

        text_rect = text_surface.get_rect(center=(WIN_WIDTH / 2, 30 + index * 30))
        screen.blit(text_surface, text_rect)


pygame.init()
WIN_WIDTH, WIN_HEIGHT = 800, 400
WORLD_WIDTH, WORLD_HEIGHT = 800*2, 400
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)
pygame.display.set_caption('Geography Quiz Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_countdown = False
start_time_1 = int(pygame.time.get_ticks() / 1000)
score = 0
# bg_music = pygame.mixer.Sound('audio/music.wav')
# bg_music.play(loops=-1)

# SlidePanel specific attributes
panel_x, panel_y, panel_width, panel_height = WIN_WIDTH - (WIN_WIDTH/4 - 10), 50, WIN_WIDTH/4 - 10, WIN_HEIGHT/1.9
panelSize = (panel_x, panel_y, panel_width, panel_height)
panelColour = (153, 153, 255, 255)
textColour = (255, 255, 255)
font_p = pygame.font.Font('font/Pixeltype.ttf', 25)
font_b = pygame.font.Font('font/Pixeltype.ttf', 35)
correct_answers = 0
time_passed = '00:00'
# lives = 3

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()
obstacle_group.add(Obstacle1())
obstacle_group.add(Obstacle2())
obstacle_group.add(Obstacle3())

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Get the width and height of your sky and ground images.
sky_width = sky_surface.get_width()
sky_height = sky_surface.get_height()
ground_width = ground_surface.get_width()
ground_height = ground_surface.get_height()


player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('Welcome', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press space start', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active and not game_over:
                    if in_story_mode:
                        in_story_mode = False  # End the story mode
                        show_instructions = True  # Show the instructions next
                    elif show_instructions:
                        show_instructions = False  # End the instructions
                        game_active = True  # Start the game
            if game_over:
                if event.key == pygame.K_r:
                    pygame.quit()
                    subprocess.run(["python", "southamerica.py", str(user_id)])
                    exit()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    subprocess.run(["python", "geomap.py", str(user_id)])
                    exit()

    if in_story_mode:
        display_story(screen, test_font)

    elif show_instructions:
        screen.fill((0, 0, 0))  # Fill the screen with black (or any other color)
        display_instructions(screen, test_font)  # This function needs to be defined to display instructions

    elif in_story_mode:
        screen.fill((0, 0, 0))  # Fill the screen with black (or any other color)
        display_story(screen, test_font)  # This function needs to be defined to display the story


    elif game_active:

        # Blit the sky images as many times as needed to cover the entire world width.
        for x in range(0, WORLD_WIDTH, sky_width):
            screen.blit(sky_surface, (x + camera.camera.x, 0))

        # Blit the ground images as many times as needed to cover the entire world width.
        for x in range(0, WORLD_WIDTH, ground_width):
            screen.blit(ground_surface, (x + camera.camera.x, 300))

        # score = display_score()

        for sprite in player:
            screen.blit(sprite.image, camera.apply(sprite))
        player.update()
        camera.update(player.sprite)

        for sprite in obstacle_group:
            screen.blit(sprite.image, camera.apply(sprite))
        obstacle_group.update()

        # display live and score
        player_lives = pygame.image.load('gameassets/Pixel Heart Animation 32x32.gif').convert_alpha()
        player_lives_rect = player_lives.get_rect(topleft=(10, 10))

        player_lives_count = test_font.render(f'X{player.sprite.lives}', False, (0, 0, 0))
        player_lives_count_rect = player_lives_count.get_rect(topleft=(player_lives_rect.right + 5, 10))

        score_display = test_font.render(f'Score: {score}', False, (0, 0, 0))
        score_display_rect = score_display.get_rect(midtop=(WIN_WIDTH / 2, 10))

        screen.blit(player_lives, player_lives_rect)
        screen.blit(player_lives_count, player_lives_count_rect)
        screen.blit(score_display, score_display_rect)
        pygame.display.update()

        game_active = collision_sprite()

        # Check if there are no more obstacles
        if not len(obstacle_group):
            game_active = False

        camera.update(player.sprite)


    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        if not game_active:
            game_over = True
        if game_over:
            display_game_over(screen, test_font, score)

        update_score_in_db(user_id, score)

        start_y_position = 75  # adjust this value for where you want the list to start

        # Draw title
        title_text = "Top 10 players"
        title_render = test_font.render(title_text, False, (255, 0, 0))  # white color for title
        title_position = (75, start_y_position - 40)  # position title 40 pixels above the first score
        screen.blit(title_render, title_position)

        top_10_scores = get_top_10_scores()

        # Calculate border dimensions
        border_margin = 10  # space between the text and the border
        border_x = 50  # a bit left from the start of the text
        border_y = start_y_position - 50  # above the title
        border_width = max(title_render.get_width(),
                           300) + 2 * border_margin  # maximum of title width or 300 for scores, plus margins
        border_height = len(
            top_10_scores) * 30 + title_render.get_height() + 2 * border_margin  # for 10 scores, the title and margins

        # Draw border
        pygame.draw.rect(screen, (255, 255, 255), (border_x, border_y, border_width, border_height),
                         2)  # 2 is the border thickness

        # Display scores inside the border
        for idx, (username, user_score) in enumerate(top_10_scores):
            score_line = f"{idx + 1}. {username}: {user_score}"
            score_render = test_font.render(score_line, False, (255, 255, 255))  # white color for scores
            screen.blit(score_render, (100, start_y_position + idx * 30))

    pygame.display.update()
    clock.tick(60)
