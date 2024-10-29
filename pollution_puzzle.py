import pygame
import random

class GameState:
    def __init__(self, width, height):
        self.puzzle_type = 0
        self.energy = 100
        self.level_progress = 0
        self.recyclables = []
        self.non_recyclables = []
        self.recycling_bin = None
        self.trash_bin = None
        self.score = 0
        self.game_over = False
        self.win = False
        self.lose = False
        self.WIDTH = width
        self.HEIGHT = height
        self.winning_score = 10  # Set a specific winning score

        # Center the bins based on the current width and height
        self.recycling_bin = pygame.Rect((self.WIDTH - 100) // 2, (self.HEIGHT - 100) // 2 - 50, 100, 100)
        self.trash_bin = pygame.Rect((self.WIDTH - 100) // 2, (self.HEIGHT - 100) // 2 + 50, 100, 100)

    def update(self):
        if self.check_game_end():
            self.game_over = True

    def check_game_end(self):
        if self.score >= self.winning_score:  # Check if the score reaches the winning score
            self.win = True
            return True

        if self.energy <= 0:
            self.lose = True
            return True
        return False

    def handle_object_placement(self, obj):
        if obj in self.recyclables:
            if self.recycling_bin.collidepoint(obj.center):
                self.score += 1
                self.recyclables.remove(obj)
            else:
                self.score -= 1
                self.energy -= 5
                self.recyclables.remove(obj)
        elif obj in self.non_recyclables:
            if self.trash_bin.collidepoint(obj.center):
                self.score += 1
                self.non_recyclables.remove(obj)
            else:
                self.score -= 1
                self.energy -= 5
                self.non_recyclables.remove(obj)

    def run_game(self, screen):
        # Load and scale the background image
        background_image = pygame.image.load("puzzleresources/background.jpg")
        background_image = pygame.transform.scale(background_image, (self.WIDTH, self.HEIGHT))

        recyclable_images = [
            pygame.image.load("puzzleresources/recycle1.png"),
            pygame.image.load("puzzleresources/recycle2.png"),
            pygame.image.load("puzzleresources/recycle3.png")
        ]
        non_recyclable_images = [
            pygame.image.load("puzzleresources/Screenshot 2024-09-10 002602.png"),
            pygame.image.load("puzzleresources/Screenshot 2024-09-10 002502.png"),
            pygame.image.load("puzzleresources/Screenshot 2024-09-10 002544.png")
        ]
        recycling_bin_image = pygame.image.load("puzzleresources/bluedustbin.png")
        trash_bin_image = pygame.image.load("puzzleresources/reddustbin.png")

        # Place objects
        for _ in range(10):
            recyclable = pygame.Rect(0, 0, 50, 50)
            recyclable.x = random.randint(0, self.WIDTH - recyclable.width)
            recyclable.y = random.randint(0, self.HEIGHT - recyclable.height)
            self.recyclables.append(recyclable)

            non_recyclable = pygame.Rect(0, 0, 50, 50)
            non_recyclable.x = random.randint(0, self.WIDTH - non_recyclable.width)
            non_recyclable.y = random.randint(0, self.HEIGHT - non_recyclable.height)
            self.non_recyclables.append(non_recyclable)

        font = pygame.font.SysFont(None, 36)
        instruction_font = pygame.font.SysFont(None, 48)  # Larger font for instructions
        instruction_text = "Drag recyclables to the recycling bin and trash to the trash bin."
        selected_object = None

        while not self.game_over:
            # Fill the screen with the scaled background image
            screen.blit(background_image, (0, 0))

            # Render and position the instruction text
            instruction_surface = instruction_font.render(instruction_text, True, (0, 0, 0))
            instruction_rect = instruction_surface.get_rect(center=(self.WIDTH // 2, 20))  # Top center position
            screen.blit(instruction_surface, instruction_rect.topleft)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for recyclable in self.recyclables:
                        if recyclable.collidepoint(mouse_pos):
                            selected_object = recyclable
                    for non_recyclable in self.non_recyclables:
                        if non_recyclable.collidepoint(mouse_pos):
                            selected_object = non_recyclable
                elif event.type == pygame.MOUSEBUTTONUP:
                    if selected_object:
                        self.handle_object_placement(selected_object)
                        selected_object = None
                elif event.type == pygame.MOUSEMOTION:
                    if selected_object:
                        selected_object.x, selected_object.y = pygame.mouse.get_pos()

            # Draw bins in center
            screen.blit(recycling_bin_image, self.recycling_bin.topleft)
            screen.blit(trash_bin_image, self.trash_bin.topleft)

            for idx, recyclable in enumerate(self.recyclables):
                screen.blit(recyclable_images[idx % len(recyclable_images)], recyclable.topleft)
            for idx, non_recyclable in enumerate(self.non_recyclables):
                screen.blit(non_recyclable_images[idx % len(non_recyclable_images)], non_recyclable.topleft)

            score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
            energy_text = font.render(f"Energy: {self.energy}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))  # Position at (10, 10) for top-left corner
            screen.blit(energy_text, (10, 40))  # Position at (10, 40) for below the score

            self.update()

            pygame.display.flip()

        # Handle game over screen
        self.display_game_over(screen, font)

    def display_game_over(self, screen, font):
        message = "You Win! Fantastic job sorting the items correctly! Your efforts are making a positive impact on the environment! Keep up the great work!" if self.win else "You Lose! Don't worry! Mistakes are part of the learning process.Keep studying which items are renewable and non-renewable, and you'll master the puzzle next time!"
        while self.game_over:
            screen.fill((255, 255, 255))
            game_over_text = font.render(message, True, (0, 0, 0))
            restart_text = font.render("Press R to restart or M to return to menu", True, (0, 0, 0))
            screen.blit(game_over_text, (self.WIDTH // 2 - game_over_text.get_width() // 2, self.HEIGHT // 2 - 20))
            screen.blit(restart_text, (self.WIDTH // 2 - restart_text.get_width() // 2, self.HEIGHT // 2 + 20))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.run_game(screen)  # Restart the game
                    elif event.key == pygame.K_m:
                        self.game_over = False  # Exit to menu

    def reset_game(self):
        self.__init__(self.WIDTH, self.HEIGHT)  # Reset game state

if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # Set the window title

    game_state = GameState(WIDTH, HEIGHT)  # Create an instance of GameState
    game_state.run_game(screen)  # Run the game
    pygame.quit()  # Quit Pygame
