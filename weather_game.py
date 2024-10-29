import pygame
import sys
import random

class WeatherPredictionGame:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Screen dimensions
        self.WIDTH = pygame.display.Info().current_w
        self.HEIGHT = pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Weather Prediction Game")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BUTTON_COLOR = (0, 0, 255)
        self.BUTTON_HOVER_COLOR = (0, 0, 150)

        # Load images
        self.win_image = pygame.transform.scale(pygame.image.load("youwin.png"), (self.WIDTH, self.HEIGHT))
        self.lose_image = pygame.transform.scale(pygame.image.load("gameover.png"), (self.WIDTH, self.HEIGHT))

        # Load sound effects
        self.sounds = {
            "Rainy": pygame.mixer.Sound("rain.mp3"),
            "Sunny": pygame.mixer.Sound("sunny.mp3"),
            "Cloudy": pygame.mixer.Sound("cloudy.mp3"),
            "Stormy": pygame.mixer.Sound("stormy.mp3")
        }
        # Fonts
        self.font = pygame.font.SysFont("Arial", 36)
        self.instruction_font = pygame.font.SysFont("bahnschrift", 28)

        # Clock
        self.clock = pygame.time.Clock()

        # Load backgrounds
        self.backgrounds = {
            "Rainy": pygame.transform.scale(pygame.image.load("rainy.jpg"), (self.WIDTH, self.HEIGHT)),
            "Sunny": pygame.transform.scale(pygame.image.load("sunny.jpg"), (self.WIDTH, self.HEIGHT)),
            "Cloudy": pygame.transform.scale(pygame.image.load("cloudy.jpg"), (self.WIDTH, self.HEIGHT)),
            "Stormy": pygame.transform.scale(pygame.image.load("storm.jpg"), (self.WIDTH, self.HEIGHT))
        }

        self.reset_game()

    def reset_game(self):
        self.weather_conditions = ["Rainy", "Sunny", "Cloudy", "Stormy"]
        self.hints = {
            "Rainy": ["Frontal system", "Low pressure area", "Moist air", "Increased humidity", "Precipitation likelihood", "Cumulonimbus clouds"],
            "Sunny": ["High pressure", "Clear sky", "Dry air", "UV index increase", "No precipitation", "Cumulus clouds"],
            "Cloudy": ["Mid-level clouds", "Overcast", "Stable air", "Possible light rain", "Visibility issues", "Stratus clouds"],
            "Stormy": ["Thunder", "Lightning", "Turbulence", "Severe wind gusts", "Possible hail", "Cumulonimbus clouds"]
        }

        self.current_weather = random.choice(self.weather_conditions)
        self.upcoming_weather = random.choice(self.weather_conditions)
        self.hint = random.choice(self.hints[self.upcoming_weather])
        self.score = 0
        self.incorrect_predictions = 0
        self.prediction = ""
        self.active = False
        self.total_rounds = 5  # Define total rounds
        self.rounds_played = 0  # Track rounds played

        self.play_weather_sound()

        # Input box setup
        self.input_box = pygame.Rect(self.WIDTH // 2 - 139, self.HEIGHT // 2 + 100, 290, 55)

        self.feedback_message = ""
        self.show_feedback = False
        self.feedback_start_time = 0
        self.feedback_duration = 2000  # Show feedback for 2 seconds

    def play_weather_sound(self):
        # Stop all sounds before playing a new one
        for sound in self.sounds.values():
            sound.stop()
        # Play the sound for the current weather
        self.sounds[self.current_weather].play()

    def start_game(self):
        self.game_loop()

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.iconify()  # Minimize the game window
                    if self.active:
                        if event.key == pygame.K_RETURN:
                            if self.prediction.capitalize() == self.upcoming_weather:
                                self.score += 1
                                self.feedback_message = "Correct!"
                            else:
                                self.incorrect_predictions += 1
                                self.feedback_message = f"Incorrect! Correct answer was: {self.upcoming_weather}"

                            self.show_feedback = True
                            self.feedback_start_time = pygame.time.get_ticks()
                            self.prediction = ""
                            self.rounds_played += 1  # Increment rounds played
                        elif event.key == pygame.K_BACKSPACE:
                            self.prediction = self.prediction[:-1]
                        else:
                            self.prediction += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active = True
                    else:
                        self.active = False

            # Draw the background image
            self.screen.blit(self.backgrounds[self.current_weather], (0, 0))
            instruction_rendered = self.instruction_font.render("Showcase your knowledge by predicting the next weather using the hint.", True, self.BLACK)
            self.screen.blit(instruction_rendered, (self.WIDTH // 2 - instruction_rendered.get_width() // 2, 10))

            weather_text = self.font.render("Current Weather: " + self.current_weather, True, self.BLACK)
            self.screen.blit(weather_text, (self.WIDTH // 2 - weather_text.get_width() // 2, self.HEIGHT // 2 - 100))

            if not self.show_feedback:
                hint_text = self.font.render("Hint: " + self.hint, True, self.BLACK)
                self.screen.blit(hint_text, (self.WIDTH // 2 - hint_text.get_width() // 2, self.HEIGHT // 2 - 50))

            score_text = self.font.render(f"Score: {self.score}", True, self.BLACK)
            self.screen.blit(score_text, (self.WIDTH // 2 - score_text.get_width() // 2, self.HEIGHT // 2))

            # Display remaining rounds in top left corner
            remaining_rounds = self.total_rounds - self.rounds_played
            rounds_text = self.font.render(f"Remaining Rounds: {remaining_rounds}", True, self.BLACK)
            self.screen.blit(rounds_text, (10, 10))  # Adjusted position

            # Display possible answers in top left corner
            possible_answers_text = self.font.render("Possible Answers: Rainy, Sunny, Cloudy, Stormy", True, self.BLACK)
            self.screen.blit(possible_answers_text, (10, 50))  # Adjusted position

            if self.show_feedback:
                feedback_text = self.font.render(self.feedback_message, True, self.BLACK)
                self.screen.blit(feedback_text, (self.WIDTH // 2 - feedback_text.get_width() // 2, self.HEIGHT // 2 + 150))

                if pygame.time.get_ticks() - self.feedback_start_time > self.feedback_duration:
                    self.show_feedback = False
                    self.feedback_message = ""
                    self.current_weather = self.upcoming_weather
                    self.play_weather_sound()
                    self.upcoming_weather = random.choice(self.weather_conditions)
                    self.hint = random.choice(self.hints[self.upcoming_weather])

            pygame.draw.rect(self.screen, self.BLACK, self.input_box, 4)
            input_text = self.font.render(self.prediction, True, self.BLACK)
            self.screen.blit(input_text, (self.input_box.x + 5, self.input_box.y + 5))

            # Update the display
            pygame.display.flip()
            self.clock.tick(60)

            # Check win/lose conditions
            if self.score >= 10 or self.incorrect_predictions >= 5 or self.rounds_played >= self.total_rounds:
                self.handle_game_end()

    def handle_game_end(self):
        if self.score >= 10:
            self.screen.blit(self.win_image, (0, 0))
        else:
            self.screen.blit(self.lose_image, (0, 0))
        pygame.display.flip()
        pygame.time.wait(2000)  # Show for 2 seconds

        # Draw Play Again and Back buttons
        while True:
            self.screen.fill(self.WHITE)  # Clear the screen

            play_again_rect = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 2 - 50, 200, 50)
            back_rect = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 2 + 20, 200, 50)

            # Check for mouse hover
            mouse_pos = pygame.mouse.get_pos()
            if play_again_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, self.BUTTON_HOVER_COLOR, play_again_rect)
            else:
                pygame.draw.rect(self.screen, self.BUTTON_COLOR, play_again_rect)

            if back_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, self.BUTTON_HOVER_COLOR, back_rect)
            else:
                pygame.draw.rect(self.screen, self.BUTTON_COLOR, back_rect)

            # Display buttons
            play_again_text = self.font.render("Play Again", True, self.WHITE)
            self.screen.blit(play_again_text, (play_again_rect.x + 20, play_again_rect.y + 10))

            back_text = self.font.render("Back to Menu", True, self.WHITE)
            self.screen.blit(back_text, (back_rect.x + 40, back_rect.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_rect.collidepoint(event.pos):
                        self.reset_game()  # Reset the game state
                        return  # Exit the button loop to restart the game
                    if back_rect.collidepoint(event.pos):
                        return  # Exit the game loop to go back to the main menu

if __name__ == '__main__':
    game_instance = WeatherPredictionGame()
    game_instance.start_game()
