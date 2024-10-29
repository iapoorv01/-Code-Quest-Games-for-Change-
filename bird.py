import pygame as pg
from collections import deque
from settings import *

class Bird(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.all_sprites_group)
        self.game = game
        self.images = deque(game.bird_images)
        self.image = self.images[0]
        self.mask_images = deque(game.mask_images)  # Store mask images in a deque
        self.mask = pg.mask.from_surface(self.mask_images[0])  # Use the initial mask image
        self.rect = self.image.get_rect()
        self.rect.center = BIRD_POS

        self.animation_event = pg.USEREVENT + 0
        pg.time.set_timer(self.animation_event, BIRD_ANIMATION_TIME)

        self.falling_velocity = 0
        self.first_jump = False

    def check_collision(self):
        hit = pg.sprite.spritecollide(self, self.game.pipe_group, dokill=False,
                                       collided=pg.sprite.collide_mask)
        if hit or self.rect.bottom > GROUND_Y or self.rect.top < -self.image.get_height():
            self.game.sound.hit_sound.play()
            pg.time.wait(1000)
            self.game.new_game()

    def jump(self):
        self.game.sound.wing_sound.play()
        self.first_jump = True
        self.falling_velocity = BIRD_JUMP_VALUE

    def use_gravity(self):
        if self.first_jump:
            self.falling_velocity += GRAVITY
            self.rect.y += self.falling_velocity + 0.5 * GRAVITY

    def update(self):
        self.check_collision()
        self.use_gravity()

    def animate(self):
        self.images.rotate(-1)  # Rotate bird images
        self.image = self.images[0]  # Update current image
        self.mask = pg.mask.from_surface(self.mask_images[0])  # Update the mask

    def check_event(self, event):
        if event.type == self.animation_event:
            self.animate()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.jump()

    def draw_hitbox(self, surface):
        # Draw the original image first
        surface.blit(self.image, self.rect.topleft)

        # Create a mask surface with the same size as the bird's image
        mask_surface = pg.Surface(self.image.get_size(), pg.SRCALPHA)
        mask_surface.fill((0, 0, 0, 0))  # Fully transparent

        # Draw the mask pixels on the mask surface
        for x in range(self.mask.get_size()[0]):
            for y in range(self.mask.get_size()[1]):
                if self.mask.get_at((x, y)):
                    mask_surface.set_at((x, y), (0, 0, 0,0))  # Semi-transparent green

        # Blit the mask on top of the bird's image
        surface.blit(mask_surface, self.rect.topleft)
