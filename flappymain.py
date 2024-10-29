import pygame as pg
import sys
from bird import *
from pipes import *
from game_objects import *
from settings import *
from fire import *


class FlappyDoom:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.load_assets()
        self.sound = Sound()
        self.score = Score(self)
        self.fire = DoomFire(self)
        self.new_game()

    def load_assets(self):
        # Load bird images
        self.bird_images = [pg.image.load(f'assets/bird/{i}.png').convert_alpha() for i in range(7)]
        bird_image = self.bird_images[0]
        bird_size = bird_image.get_width() * BIRD_SCALE - 500, bird_image.get_height() * BIRD_SCALE - 450
        self.bird_images = [pg.transform.scale(sprite, bird_size) for sprite in self.bird_images]

        # Load background
        self.background_image = pg.image.load('assets/images/bg.jpg').convert_alpha()
        self.background_image = pg.transform.scale(self.background_image, RES)

        # Load ground
        self.ground_image = pg.image.load('assets/images/ground.png').convert()
        self.ground_image = pg.transform.scale(self.ground_image, (WIDTH, GROUND_HEIGHT))

        # Load pipes
        self.top_pipe_image = pg.image.load('assets/images/top_pipe.png').convert_alpha()
        self.top_pipe_image = pg.transform.scale(self.top_pipe_image, (PIPE_WIDTH, PIPE_HEIGHT))
        self.bottom_pipe_image = pg.transform.flip(self.top_pipe_image, False, True)

        # Load tree
        self.tree_image = pg.image.load('assets/images/tree1.png').convert_alpha()
        self.tree_image = pg.transform.scale(self.tree_image, (TREE_WIDTH, TREE_HEIGHT))

        # Load bird mask
        self.mask_images = [pg.image.load(f'assets/bird/{i}.png').convert_alpha() for i in range(7)]
        mask_image = self.mask_images[0]
        mask_size = mask_image.get_width() * BIRD_SCALE - 500, mask_image.get_height() * BIRD_SCALE - 450
        self.mask_images = [pg.transform.scale(birdymask, mask_size) for birdymask in self.mask_images]

    def new_game(self):
        self.all_sprites_group = pg.sprite.Group()
        self.pipe_group = pg.sprite.Group()
        self.bird = Bird(self)
        self.background = Background(self)
        self.ground = Ground(self)
        self.pipe_handler = PipeHandler(self)
        self.trees_positions = [(100, GROUND_Y - TREE_HEIGHT - 20)]  # Fixed position for the tree

    def draw(self):
        self.background.draw()
        self.fire.draw()
        self.all_sprites_group.draw(self.screen)

        # Draw only the bottom pipes
        for pipe in self.pipe_group:
            if isinstance(pipe, BottomPipe):
                self.screen.blit(self.bottom_pipe_image, (pipe.rect.x, pipe.rect.y))

        # Draw the tree, ensuring it doesn't overlap with the bottom pipes
        for tree_x, tree_y in self.trees_positions:
            # Find the lowest position of the bottom pipes, if they exist
            bottom_pipe_x = [pipe.rect.x for pipe in self.pipe_group if isinstance(pipe, BottomPipe)]

            if bottom_pipe_x:  # Check if there are any bottom pipes
                min_bottom_pipe_x = min(bottom_pipe_x)  # Get the lowest y position of the bottom pipes
                tree_x = max(tree_x, min_bottom_pipe_x - 50)  # Adjust tree_y to be above the bottom pipes
            else:
                tree_x = tree_x  # Default to a height if no pipes exist

            self.screen.blit(self.tree_image, (tree_x, tree_y))

        self.ground.draw()
        self.score.draw()

        # Draw hitboxes for debugging
        self.bird.draw_hitbox(self.screen)
        for pipe in self.pipe_group:
            pipe.draw_hitbox(self.screen)

        pg.display.flip()

    def update(self):
        self.background.update()
        self.fire.update()
        self.all_sprites_group.update()
        self.ground.update()
        self.pipe_handler.update()
        self.move_trees()  # Move trees with the ground
        self.clock.tick(FPS)

    def move_trees(self):
        # Move trees to the left to simulate background movement
        for i in range(len(self.trees_positions)):
            tree_x, tree_y = self.trees_positions[i]
            tree_x -= SCROLL_SPEED  # Move tree left
            # Reset position if it goes off-screen (optional)
            if tree_x < -TREE_WIDTH:
                tree_x = WIDTH
            self.trees_positions[i] = (tree_x, tree_y)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            self.bird.check_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


class BottomPipe(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load('assets/images/bottom_pipe.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))  # Scale if needed
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw_hitbox(self, surface):
        pg.draw.rect(surface, (255, 0, 0), self.rect, 2)  # Draw hitbox for debugging


if __name__ == '__main__':
    game = FlappyDoom()
    game.run()
