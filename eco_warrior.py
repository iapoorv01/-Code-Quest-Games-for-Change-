import pygame
import sys
import random
import os


class EcoWarrior:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the game window
        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Eco-Warrior")
        self.clock = pygame.time.Clock()

        # Load images and sounds
        self.load_resources()

        # Game settings
        self.player_pos = [self.screen_width / 2, self.screen_height / 2]
        self.player_speed = 5
        self.player_health = 3
        self.player_score = 0
        self.power_up_active = False
        self.power_up_duration = 300  # Duration in frames

        self.selected_level = None
        self.apply_level_settings(1)  # Default to level 1

    def load_resources(self):
        # Load images
        base_path = "resources/images/"
        self.player_image = pygame.image.load(os.path.join(base_path, "garbagepicker.png"))
        self.trash_images = [
            pygame.image.load(os.path.join(base_path, "trash.png")),
            pygame.image.load(os.path.join(base_path, "trash2.png")),
            pygame.image.load(os.path.join(base_path, "trash3.png"))
        ]
        self.polluter_image = pygame.image.load(os.path.join(base_path, "polluter.png"))
        self.power_up_image = pygame.image.load(os.path.join(base_path, "powerup.png"))
        self.background_image = pygame.image.load(os.path.join(base_path, "bg.jpg"))
        self.win_image = pygame.image.load(os.path.join(base_path, "youwin.png"))
        self.game_over_image = pygame.image.load(os.path.join(base_path, "gameover.png"))

        # Scale images
        self.player_image = pygame.transform.scale(self.player_image, (60, 70))
        self.trash_images = [pygame.transform.scale(img, (30, 30)) for img in self.trash_images]
        self.polluter_image = pygame.transform.scale(self.polluter_image, (60, 60))
        self.power_up_image = pygame.transform.scale(self.power_up_image, (40, 40))
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        self.win_image = pygame.transform.scale(self.win_image, (self.screen_width, self.screen_height))
        self.game_over_image = pygame.transform.scale(self.game_over_image, (self.screen_width, self.screen_height))

        # Load sounds
        self.collect_sound = pygame.mixer.Sound(os.path.join("resources/audio", "enemy.wav"))
        self.hit_sound = pygame.mixer.Sound(os.path.join("resources/audio", "explode.wav"))
        self.powerup_sound = pygame.mixer.Sound(os.path.join("resources/audio", "shoot.wav"))
        self.button_click_sound = pygame.mixer.Sound(os.path.join("resources/audio", "click.mp3"))
        pygame.mixer.music.load(os.path.join("resources/audio", "moonlight.wav"))
        pygame.mixer.music.play(-1)

    def apply_level_settings(self, level):
        # Define level settings
        level_settings = {
            1: {"polluter_speed": 2, "max_polluters": 3, "max_trash": 5},
            2: {"polluter_speed": 3, "max_polluters": 5, "max_trash": 7},
            3: {"polluter_speed": 4, "max_polluters": 7, "max_trash": 9}
        }
        settings = level_settings[level]
        self.polluter_speed = settings["polluter_speed"]
        self.max_polluters = settings["max_polluters"]
        self.max_trash = settings["max_trash"]

        # Reset trash and polluters
        self.trash_pos = [[random.randint(0, self.screen_width - 30), random.randint(0, self.screen_height - 30)] for _ in range(self.max_trash)]
        self.trash_collected = [False] * self.max_trash
        self.polluter_pos = [[random.randint(0, self.screen_width - 60), random.randint(0, self.screen_height - 60)] for _ in range(self.max_polluters)]

    def select_level(self):
        self.screen.fill((255, 255, 255))
        font = pygame.font.SysFont("Arial", 45)
        title_text = font.render("Select Level", True, (0, 128, 0))
        self.screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))

        # Draw level buttons
        button_color = (200, 200, 200)
        hover_color = (150, 150, 150)
        level_buttons = []
        for level in range(1, 4):
            button_rect = pygame.Rect(self.screen_width // 2 - 50, 200 + 60 * level, 100, 40)
            level_buttons.append((button_rect, level))
            pygame.draw.rect(self.screen, button_color, button_rect)
            level_text = font.render(f"Level {level}", True, (0, 0, 0))
            self.screen.blit(level_text, (button_rect.x + 10, button_rect.y + 5))

        pygame.display.flip()

        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, level in level_buttons:
                        if rect.collidepoint(mouse_pos):
                            self.button_click_sound.play()
                            self.selected_level = level
                            return level

            # Change color on hover
            for rect, level in level_buttons:
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, hover_color, rect)
                else:
                    pygame.draw.rect(self.screen, button_color, rect)
                level_text = font.render(f"Level {level}", True, (0, 0, 0))
                self.screen.blit(level_text, (rect.x + 10, rect.y + 5))

            pygame.display.update()

    def game_loop(self):
        while True:
            self.handle_events()
            self.update_game_state()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update_game_state(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player_pos[1] -= self.player_speed
        if keys[pygame.K_DOWN]:
            self.player_pos[1] += self.player_speed
        if keys[pygame.K_LEFT]:
            self.player_pos[0] -= self.player_speed
        if keys[pygame.K_RIGHT]:
            self.player_pos[0] += self.player_speed

        # Boundary checks
        self.player_pos[0] = max(0, min(self.player_pos[0], self.screen_width - self.player_image.get_width()))
        self.player_pos[1] = max(0, min(self.player_pos[1], self.screen_height - self.player_image.get_height()))

        # Move polluters and check for collisions
        for i in range(len(self.polluter_pos)):
            self.polluter_pos[i][0] += self.polluter_speed
            if self.polluter_pos[i][0] > self.screen_width:
                self.polluter_pos[i][0] = 0

            # Check collision with polluters
            if (self.player_pos[0] < self.polluter_pos[i][0] + 60 and
                    self.player_pos[0] + 60 > self.polluter_pos[i][0] and
                    self.player_pos[1] < self.polluter_pos[i][1] + 60 and
                    self.player_pos[1] + 70 > self.polluter_pos[i][1]):
                self.player_health -= 1
                self.hit_sound.play()
                if self.player_health <= 0:
                    self.game_over()

        # Check for collisions with trash
        for i in range(len(self.trash_pos)):
            if (self.player_pos[0] < self.trash_pos[i][0] + 30 and
                    self.player_pos[0] + 60 > self.trash_pos[i][0] and
                    self.player_pos[1] < self.trash_pos[i][1] + 30 and
                    self.player_pos[1] + 70 > self.trash_pos[i][1]):
                if not self.trash_collected[i]:
                    self.trash_collected[i] = True
                    self.player_score += 1
                    self.collect_sound.play()

        # Check if all trash has been collected
        if all(self.trash_collected):
            self.win()

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.player_image, (self.player_pos[0], self.player_pos[1]))

        for i in range(len(self.trash_pos)):
            if not self.trash_collected[i]:
                self.screen.blit(self.trash_images[i % len(self.trash_images)],
                                 (self.trash_pos[i][0], self.trash_pos[i][1]))

        for polluter in self.polluter_pos:
            self.screen.blit(self.polluter_image, (polluter[0], polluter[1]))

        # Draw score and health
        font = pygame.font.SysFont("Arial", 30)
        score_text = font.render(f"Score: {self.player_score}", True, (255, 255, 255))
        health_text = font.render(f"Health: {self.player_health}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(health_text, (10, 40))

        pygame.display.flip()

    def win(self):
        self.show_end_screen(self.win_image, "You Win!")

    def game_over(self):
        self.show_end_screen(self.game_over_image, "Game Over!")

    def show_end_screen(self, image, message):
        self.screen.blit(image, (0, 0))
        font = pygame.font.SysFont("Arial", 30)
        message_text = font.render(message, True, (255, 255, 255))
        self.screen.blit(message_text, (self.screen_width // 2 - message_text.get_width() // 2, 50))

        # Draw Play Again and Back to Menu buttons
        play_again_rect = pygame.Rect(self.screen_width // 2 - 80, 400, 150, 40)
        back_to_menu_rect = pygame.Rect(self.screen_width // 2 - 80, 460, 150, 40)

        pygame.draw.rect(self.screen, (200, 200, 200), play_again_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), back_to_menu_rect)

        play_again_text = font.render("Play Again", True, (0, 0, 0))
        back_to_menu_text = font.render("Back to Menu", True, (0, 0, 0))
        self.screen.blit(play_again_text, (play_again_rect.x + 10, play_again_rect.y + 5))
        self.screen.blit(back_to_menu_text, (back_to_menu_rect.x + 10, back_to_menu_rect.y + 5))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_rect.collidepoint(event.pos):
                        self.button_click_sound.play()
                        self.play_again()
                        return  # Exit the loop
                    elif back_to_menu_rect.collidepoint(event.pos):
                        self.button_click_sound.play()
                        self.back_to_menu()
                        return  # Exit the loop

    def play_again(self):
        self.player_health = 3
        self.player_score = 0
        self.apply_level_settings(self.selected_level)
        self.game_loop()  # Restart the game loop

    def back_to_menu(self):
        # Handle returning to the main menu, if implemented.
        return # Or whatever logic you have to go back to the menu.


# Or implement a way to navigate back to the main menu if you have one.


# Modify this to return to the main menu in your main menu code

if __name__ == "__main__":
    game = EcoWarrior()
    level = game.select_level()
    game.apply_level_settings(level)
    game.game_loop()
