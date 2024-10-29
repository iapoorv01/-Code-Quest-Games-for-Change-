import pygame
import sys

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
BUDGET_START = 1000
AIR_QUALITY_START = 50

# Colors
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class UrbanGreeneryGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Urban Greenery")
        self.clock = pygame.time.Clock()

        self.city_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.budget = BUDGET_START
        self.air_quality = AIR_QUALITY_START

        self.font = pygame.font.Font(None, 36)

    def draw_grid(self):
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
                if self.city_grid[x][y] == 1:  # Tree
                    pygame.draw.rect(self.screen, GREEN, rect.inflate(-10, -10))

    def draw_info(self):
        budget_text = self.font.render(f"Budget: ${self.budget}", True, BLACK)
        air_quality_text = self.font.render(f"Air Quality: {self.air_quality}", True, BLACK)
        self.screen.blit(budget_text, (10, HEIGHT - 40))
        self.screen.blit(air_quality_text, (10, HEIGHT - 80))

    def plant_tree(self, x, y):
        if self.budget >= 100:
            self.city_grid[x][y] = 1  # 1 represents a tree
            self.budget -= 100
            self.air_quality += 2  # Improve air quality

    def run(self):
        while True:
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_info()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                        self.plant_tree(grid_x, grid_y)

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = UrbanGreeneryGame()
    game.run()
