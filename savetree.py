import sys
import cfg
import math
import random
import pygame
from modules import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(cfg.SCREENSIZE)
        pygame.display.set_caption('SAVE THE NATURAL RESOURCES')

        self.game_images = self.load_images()
        self.game_sounds = self.load_sounds()
        
        pygame.mixer.music.load(cfg.Sounds['moonlight'])
        pygame.mixer.music.play(-1, 0.0)

        self.font = pygame.font.Font(None, 24)

        self.bunny = BunnySprite(image=self.game_images.get('man'), position=(100, 100))
        self.acc_record = [0., 0.]
        self.healthvalue = 194
        self.arrow_sprites_group = pygame.sprite.Group()
        self.badguy_sprites_group = pygame.sprite.Group()

        self.badtimer = 100
        self.badtimer1 = 0

    def load_images(self):
        return {key: pygame.image.load(value) for key, value in cfg.Imagees.items()}

    def load_sounds(self):
        return {key: pygame.mixer.Sound(value) for key, value in cfg.Sounds.items() if key != 'moonlight'}

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.handle_events()
            self.update_game_state()
            self.draw()

            pygame.display.flip()
            clock.tick(cfg.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.game_sounds['shoot'].play()
                self.acc_record[1] += 1
                mouse_pos = pygame.mouse.get_pos()
                angle = math.atan2(mouse_pos[1] - (self.bunny.rotated_position[1] + 32),
                                   mouse_pos[0] - (self.bunny.rotated_position[0] + 26))
                arrow = ArrowSprite(self.game_images.get('arrow'), (angle, self.bunny.rotated_position[0] + 32, self.bunny.rotated_position[1] + 26))
                self.arrow_sprites_group.add(arrow)

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            self.bunny.move(cfg.SCREENSIZE, 'up')
        elif key_pressed[pygame.K_s]:
            self.bunny.move(cfg.SCREENSIZE, 'down')
        elif key_pressed[pygame.K_a]:
            self.bunny.move(cfg.SCREENSIZE, 'left')
        elif key_pressed[pygame.K_d]:
            self.bunny.move(cfg.SCREENSIZE, 'right')

    def update_game_state(self):
        for arrow in self.arrow_sprites_group:
            if arrow.update(cfg.SCREENSIZE):
                self.arrow_sprites_group.remove(arrow)

        if self.badtimer == 0:
            badguy = BadguySprite(self.game_images.get('badguy'), position=(640, random.randint(50, 430)))
            self.badguy_sprites_group.add(badguy)
            self.badtimer = 100 - (self.badtimer1 * 2)
            self.badtimer1 = min(self.badtimer1 + 2, 20)
        self.badtimer -= 1

        for badguy in self.badguy_sprites_group:
            if badguy.update():
                self.game_sounds['hit'].play()
                self.healthvalue -= random.randint(4, 8)
                self.badguy_sprites_group.remove(badguy)

        for arrow in self.arrow_sprites_group:
            for badguy in self.badguy_sprites_group:
                if pygame.sprite.collide_mask(arrow, badguy):
                    self.game_sounds['enemy'].play()
                    self.arrow_sprites_group.remove(arrow)
                    self.badguy_sprites_group.remove(badguy)
                    self.acc_record[0] += 1

        if pygame.time.get_ticks() >= 90000 or self.healthvalue <= 0:
            self.handle_game_over()

    def draw(self):
        self.screen.fill(0)

        for x in range(cfg.SCREENSIZE[0] // self.game_images['grass'].get_width() + 1):
            for y in range(cfg.SCREENSIZE[1] // self.game_images['grass'].get_height() + 1):
                self.screen.blit(self.game_images['grass'], (x * 100, y * 100))
        for i in range(4):
            self.screen.blit(self.game_images['tree'], (0, 30 + 105 * i))

        countdown_text = self.font.render(
            str((90000 - pygame.time.get_ticks()) // 60000) + ":" + str((90000 - pygame.time.get_ticks()) // 1000 % 60).zfill(2), True, (0, 0, 0))
        countdown_rect = countdown_text.get_rect()
        countdown_rect.topright = [635, 5]
        self.screen.blit(countdown_text, countdown_rect)

        self.arrow_sprites_group.draw(self.screen)
        self.badguy_sprites_group.draw(self.screen)
        self.bunny.draw(self.screen, pygame.mouse.get_pos())

        self.screen.blit(self.game_images.get('healthbar'), (5, 5))
        for i in range(self.healthvalue):
            self.screen.blit(self.game_images.get('health'), (i + 8, 8))

    def handle_game_over(self):
        exitcode = self.healthvalue > 0
        final_image = self.game_images.get('youwin') if exitcode else self.game_images.get('gameover')
        self.screen.blit(final_image, (0, 0))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds before closing the game
        pygame.quit()
        sys.exit()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
