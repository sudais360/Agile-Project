import pygame

from lives import Lives



class SlidePanel:

    def __init__(self, screen_used, rect_size,
                 colour, text_colour,
                 panel_font, button_font,
                 original_width, original_height,
                 score, questions_cleared,
                 time_elapsed, result):
        super().__init__()

        # attributes

        self.screen_used = screen_used
        self.rect_size = rect_size
        self.colour = colour
        self.text_colour = text_colour
        self.original_width = original_width
        self.original_height = original_height
        self.panel_font = panel_font
        self.button_font = button_font
        self.score = score
        self.questions_cleared = questions_cleared
        self.time_elapsed = time_elapsed
        self.result = result
        self.lives_left = 3
        # player_lives = Lives('gameassets/heart_sprite_sheet_32x32.png', (48, 48), 3)
        # self.lives_left = player_lives.frame_count - player_lives.current_frame
        # self.lives_left = gameplay2.player_lives.frame_count

        # animation attributes
        self.start_pos = original_width + 100
        self.end_pos = original_width - 135
        self.width = rect_size[2]

        # animation logic
        self.pos = self.start_pos
        # check whether panel is in the start position (outside screen frame)
        self.in_start_pos = True

        self.display_value(screen_used, rect_size,
                 colour, text_colour,
                 panel_font, button_font,
                 original_width, original_height,
                 score, questions_cleared,
                 time_elapsed, result)

    def num_lives(self, lives):
        # print(lives)
        self.lives_left = self.lives_left - lives
        print(self.lives_left)

        pygame.display.update()

    def display_value(self, screen_used, rect_size,
                 colour, text_colour,
                 panel_font, button_font,
                 original_width, original_height,
                 score, questions_cleared,
                 time_elapsed, result):
        # print(self.lives_left)

        # layout (button)
        pygame.draw.rect(screen_used, (64, 224, 208), [original_width - 135, 5, 135, 40])
        button_text = self.button_font.render('Show Score', False, (20, 20, 20))
        screen_used.blit(button_text, (original_width - 130, 15))


        # layout (scoreboard background)
        rect_create = pygame.Surface(pygame.Rect(rect_size).size, pygame.SRCALPHA)
        pygame.draw.rect(rect_create, colour, rect_create.get_rect())
        screen_used.blit(rect_create, rect_size)

        # layout (stats text)
        stats_message = self.panel_font.render('Stats', False, text_colour)
        stats_message_rect = stats_message.get_rect(center=(rect_size[0] + rect_size[2]/2, rect_size[1] + 20))
        screen_used.blit(stats_message, stats_message_rect)

        # layout (score)
        score_message = self.panel_font.render(f'Score: {score}', False, text_colour)
        score_message_rect = score_message.get_rect(topleft=(rect_size[0] + 10, rect_size[1] + 50))
        screen_used.blit(score_message, score_message_rect)

        # layout (questions answered)
        clear_count = self.panel_font.render(f'Correct Answers: {questions_cleared}', False, text_colour)
        clear_count_rect = clear_count.get_rect(topleft=(rect_size[0] + 10, rect_size[1] + 80))
        screen_used.blit(clear_count, clear_count_rect)

        # layout (time passed since start of game)
        time = self.panel_font.render(f'Time Elapsed: {time_elapsed} s', False, text_colour)
        time_rect = time.get_rect(topleft=(rect_size[0] + 10, rect_size[1] + 110))
        screen_used.blit(time, time_rect)

        # layout (lives remaining)
        lives = self.panel_font.render(f'Lives: {result}', False, text_colour)
        lives_rect = lives.get_rect(topleft=(rect_size[0] + 10, rect_size[1] + 140))
        screen_used.blit(lives, lives_rect)

        pygame.display.update()





