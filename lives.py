import pygame

test = 2
class Lives(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, scale, frame_count):
        super().__init__()
        self.frame_count = frame_count
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frames = self.load_frames(sprite_sheet, scale)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.height = self.image.get_height()
        self.lives_lost = False
        self.game_over = False

    def load_frames(self, sprite_sheet, scale):
        sprite_width = sprite_sheet.get_width() // self.frame_count
        sprite_height = sprite_sheet.get_height()
        frames = []
        for frame in range(self.frame_count):
            frame_surface = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA, 32)
            frame_surface.blit(sprite_sheet, (0, 0), (frame * sprite_width, 0, sprite_width, sprite_height))
            frames.append(pygame.transform.scale(frame_surface, (scale[0], scale[1])))
        return frames

    def update(self):
        if self.current_frame > 2:
            self.game_over = True
        else:
            if self.lives_lost:
                self.current_frame += 1
                self.lives_lost = False

        self.image = self.frames[self.current_frame]
