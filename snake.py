import pygame
import random
import os
import time
import google.generativeai as genai

os.environ["API_KEY"] = "AIzaSyBX4QAOj_iBrEPF9y2QBUNEJK4nsnq7bW0"

# Configure the AI
genai.configure(api_key=os.environ["API_KEY"])
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[]
)

# Define the game class
class OceanCleanupGame:
    def __init__(self, snake_speed=25, mission_time=30, initial_trash_count=5, increase_per_level=3):
        pygame.init()

        # Load sounds
        self.water_sound = pygame.mixer.Sound('underwater-19568.mp3')
        self.collect_sound = pygame.mixer.Sound('click.mp3')
        self.level = 1  # Initialize level

        # Get screen size
        infoObject = pygame.display.Info()
        # Set screen size to full screen
        self.dis_width = pygame.display.Info().current_w
        self.dis_height = pygame.display.Info().current_h# Half of the screen height
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        # Colors
        self.yellow = (255, 255, 102)
        self.green = (0, 255, 0)
        self.red = (213, 50, 80)  # for game over messages

        self.snake_block = 12
        self.snake_speed = snake_speed
        self.mission_time = mission_time  # Mission time in seconds
        self.trash_count = initial_trash_count  # Initial number of trash items
        self.increase_per_level = increase_per_level  # Trash items to add for each new level


        # Load trash images
        self.trash_images = [
            pygame.image.load('trash.png'),
            pygame.image.load('trash2.png'),
            pygame.image.load('trash3.png')
        ]
        # Scale trash images to 20x20 pixels
        self.trash_images = [pygame.transform.scale(img, (50, 50)) for img in self.trash_images]

        # Load fish images
        self.fish_images = [
            pygame.image.load('fishh.png'),
            pygame.image.load('fishes.png')
        ]
        # Scale fish images
        self.fish_images = [pygame.transform.scale(img, (80, 70)) for img in self.fish_images]

        # Initialize fish properties
        self.fish_speed = 8
        self.fish_count = 8  # Number of fish
        self.fish_positions = [(random.randint(0, self.dis_width), random.randint(0, self.dis_height), random.choice(self.fish_images)) for _ in range(self.fish_count)]

        # Load water texture
        self.water_image = pygame.image.load('water.png')
        self.water_image = pygame.transform.scale(self.water_image,
                                                  (self.dis_width, self.dis_height))  # Scale to fit screen
        self.water_y_offset = 0  # Offset for the flowing effect

        # Game Display
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('Ocean Cleanup')

        # Game clock


        # Fonts
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 30)  # Slightly smaller font
        self.quote = self.fetch_quote()
        self.clock = pygame.time.Clock()
    # Display score
    def show_score(self, score):
        value = self.score_font.render("Trash Collected: " + str(score), True, self.yellow)
        self.dis.blit(value, [0, 0])
    #display level
    def show_level(self):
        level_text = self.score_font.render("Level: " + str(self.level), True, self.yellow)
        self.dis.blit(level_text, [self.dis_width - 200, 40])  # Positioning for visibility

    # Display remaining time
    def show_timer(self, remaining_time):
        timer_text = self.score_font.render("Time Left: " + str(remaining_time), True, self.yellow)
        self.dis.blit(timer_text, [self.dis_width - 200, 10])  # Adjusted position

    def show_quote(self):
        quote_surface = self.font_style.render(self.quote, True, self.yellow)
        quote_rect = quote_surface.get_rect(center=(self.dis_width / 2, 20))  # Centered at the top
        self.dis.blit(quote_surface, quote_rect)

    def loading_screen(self):
        loading_start_time = pygame.time.get_ticks()
        loading_duration = 2000  # Display loading screen for 3 seconds

        while True:
            self.dis.fill((0, 0, 0))
            loading_text = self.font_style.render("Loading, please wait...", True, self.yellow)
            self.dis.blit(loading_text, (self.dis_width / 2 - loading_text.get_width() / 2, self.dis_height / 2))
            pygame.display.update()

            # Check if the loading duration has passed
            if pygame.time.get_ticks() - loading_start_time > loading_duration:
                break

            # Allow the event queue to process
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        # i can add any other necessary actions after the loading screen here

    # Small delay to simulate loading

    def fetch_quote(self):
        self.loading_screen()  # Show loading screen
        prompt = (
            "Generate a unique quote which symbolizes reducing water pollution, ensuring it hasn't been generated before even by you(you are giving the same quote again and again)."
        )
        response = chat_session.send_message(prompt)
        quote = self.parse_ai_response(response.text)
        return quote

    def parse_ai_response(self, response):
        quote = response.strip()
        if not quote:
            return "Clean water is essential for life."
        return quote
    # Draw the marine animal (snake)
    def draw_animal(self, animal_list):
        for i, segment in enumerate(animal_list):
            # Ensure the RGB values are valid
            r = max(0, min(255, 0))  # Red component (0)
            g = max(0, min(255, 255 - i * 10))  # Green component, decreases with each segment
            b = max(0, min(255, 0))  # Blue component (0)

            color = (r, g, b)  # Create the color tuple

            # Draw the snake body segments
            pygame.draw.rect(self.dis, color, [segment[0], segment[1], self.snake_block, self.snake_block])

    # Display messages
    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        self.dis.blit(mesg, [self.dis_width / 6, self.dis_height / 3])

    # Draw flowing water background
    def draw_water_background(self):
        # Draw two instances of the water image for seamless effect
        self.dis.blit(self.water_image, (0, self.water_y_offset))
        self.dis.blit(self.water_image, (0, self.water_y_offset - self.dis_height))

        # Update the offset for animation
        self.water_y_offset += 1  # Change this value to adjust speed
        if self.water_y_offset >= self.dis_height:
            self.water_y_offset = 0

    # Generate unique trash positions with associated images
    def generate_trash_positions(self):
        positions = []
        while len(positions) < self.trash_count:
            trash_x = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
            trash_y = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
            if (trash_x, trash_y) not in [pos[0:2] for pos in positions]:  # Ensure unique positions
                # Randomly select a trash image from the list
                trash_image = random.choice(self.trash_images)
                positions.append((trash_x, trash_y, trash_image))  # Store position and image
        return positions
#main game loop
    def run_game(self):
        game_over = False
        game_close = False

        x1 = self.dis_width / 2
        y1 = self.dis_height / 2

        x1_change = 0
        y1_change = 0

        animal_List = []
        length_of_animal = 1

        # Generate initial trash positions
        trash_positions = self.generate_trash_positions()

        start_ticks = pygame.time.get_ticks()  # Start timer

        while not game_over:

            while game_close:
                self.dis.fill((0, 0, 0))  # Clear the screen
                self.message("You Lost! Press C-Play Again or Q-Quit", self.red)
                self.show_score(length_of_animal - 1)

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                        game_close = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            self.run_game()  # Restart the game

            # Calculate remaining time
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            remaining_time = self.mission_time - int(seconds)

            if remaining_time <= 0:
                game_close = True  # End game when time runs out

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -self.snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = self.snake_block
                        x1_change = 0

            if x1 >= self.dis_width or x1 < 0 or y1 >= self.dis_height or y1 < 0:
                game_close = True
            x1 += x1_change
            y1 += y1_change

            # Draw flowing water background
            self.draw_water_background()

            # Play water sound continuously (optional)
            self.water_sound.play(-1)  # Loop the water sound

            # Draw trash
            for trash_x, trash_y, trash_image in trash_positions:
                self.dis.blit(trash_image, (trash_x, trash_y))  # Draw trash

            # Update and draw fish positions
            for i in range(len(self.fish_positions)):
                fish_x, fish_y, fish_image = self.fish_positions[i]
                fish_x += self.fish_speed  # Move fish to the right

                # Reset fish position if it moves off screen
                if fish_x > self.dis_width:
                    fish_x = 0
                    fish_y = random.randint(0, self.dis_height)  # Randomize y position
                    fish_image = random.choice(self.fish_images)  # Choose a new fish image

                self.fish_positions[i] = (fish_x, fish_y, fish_image)
                self.dis.blit(fish_image, (fish_x, fish_y))  # Draw fish

            # Check for collision with fish
            snake_head_rect = pygame.Rect(x1, y1, self.snake_block, self.snake_block)
            for fish_x, fish_y, fish_image in self.fish_positions:
                fish_rect = pygame.Rect(fish_x, fish_y, fish_image.get_width(), fish_image.get_height())
                if snake_head_rect.colliderect(fish_rect):  # Check for collision
                    game_close = True  # Game over if snake collides with fish

            animal_Head = [x1, y1]
            animal_List.append(animal_Head)
            if len(animal_List) > length_of_animal:
                del animal_List[0]

            for x in animal_List[:-1]:
                if x == animal_Head:
                    game_close = True

            # Check for trash collection using bounding boxes
            for trash_x, trash_y, trash_image in trash_positions:
                trash_rect = pygame.Rect(trash_x, trash_y, trash_image.get_width(), trash_image.get_height())
                if snake_head_rect.colliderect(trash_rect):  # Check for collision
                    trash_positions.remove((trash_x, trash_y, trash_image))
                    length_of_animal += 1  # Increase snake length
                    self.collect_sound.play()  # Play collection sound

            # Check if all trash collected
            if not trash_positions:
                # Increase the trash count for the next level
                self.trash_count += self.increase_per_level
                self.level += 1  # Increase the level number
                # Generate new trash positions for the next level
                trash_positions = self.generate_trash_positions()
                start_ticks = pygame.time.get_ticks()  # Reset timer for the new level

            self.draw_animal(animal_List)
            self.show_quote()
            self.show_score(length_of_animal - 1)
            self.show_timer(remaining_time)  # Display the remaining time
            self.show_level()
            pygame.display.update()

            self.clock.tick(self.snake_speed)

        pygame.quit()


# If you want to call it directly from this file
if __name__ == "__main__":
    game = OceanCleanupGame()
    game.run_game()
