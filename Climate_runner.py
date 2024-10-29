import pygame
import random
import sys

def run_game():
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()  # Initialize the mixer module for sound

    # Load and play background music
    pygame.mixer.music.load("climate runner(sound).mp3")  # Replace with your sound file path
    pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
    pygame.mixer.music.play(-1)  # Play the music in a loop (-1 means infinite loop)

    infoObject = pygame.display.Info()
    screen_width = infoObject.current_w
    screen_height = infoObject.current_h
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Runner Game")

    # Define the fade_in_screen function
    def fade_in_screen():
        description_text = [
            "Welcome to Climate Runner!",
            "In a world where luxury often harms the environment,",
            "you choose a different path.",
            "Despite criticism for being 'poor' or 'less than',",
            "you stand firm in your values.",
            "Your choices promote sustainability and health,",
            "proving that true wealth comes from protecting our planet.",
            "Over time, others begin to admire your dedication.",
            "Together, we can create a positive impact!"
        ]

        font = pygame.font.Font("mighty.ttf", 36)

        # Fill screen with black
        screen.fill((0, 0, 0))
        pygame.display.flip()
        pygame.time.delay(500)  # Hold for half a second

        # Fade in effect
        for alpha in range(0, 255, 5):  # Adjust increment for speed
            screen.fill((0, 0, 0))
            surface = pygame.Surface((screen_width, screen_height))
            surface.set_alpha(alpha)
            screen.blit(surface, (0, 0))

            for i, line in enumerate(description_text):
                text_surface = font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 50 + i * 40))
                screen.blit(text_surface, text_rect)

            pygame.display.flip()
            pygame.time.delay(30)  # Delay for smooth transition

        # Hold the screen for 5 seconds after fade-in
        pygame.time.delay(5000)  # Delay for 5 seconds

    # Call the fade-in function before the game starts
    fade_in_screen()

    # Set up player properties
    player_width = 50
    player_height = 50
    player_x = screen_width / 2
    player_y = screen_height / 2 - player_height + 100
    player_speed = 10
    player_currency = 0
    vehicle_price = 100
    is_motor_vehicle = False
    environment_life = 50  # Start with lower environment health
    max_environment_life = 60
    last_environment_tick = pygame.time.get_ticks()
    purchase_screen = False
    can_increase_health = False
    health_increase_time = 2000  # Increase health every 2 seconds
    last_health_increase = pygame.time.get_ticks()
    comment_displayed = False
    winning_screen = False  # To track winning state
    game_over = False  # To track game over state
    show_message = False  # To control message display
    message_displayed_time = 0
    current_vehicle = "bicycle"  # Start with bicycle

    # Load images
    background_image = pygame.image.load("background(climate runner).jpg")  # Replace with your background image path
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    winning_image = pygame.image.load("youwin.png")  # Replace with your winning image path
    losing_image = pygame.image.load("gameover.png")  # Replace with your losing image path
    winning_image = pygame.transform.scale(winning_image, (screen_width, screen_height))
    losing_image = pygame.transform.scale(losing_image, (screen_width, screen_height))

    # Load car images
    car_images = [
        pygame.image.load("car1(climate runner).png"),  # Replace with your first car image path
        pygame.image.load("car2(climate runner).png"),  # Replace with your second car image path
        pygame.image.load("car3(climate runnner).png"),  # Replace with your third car image path
    ]

    # Load bicycle image
    bicycle_image = pygame.image.load("bicycle(climate runner).png")  # Replace with your bicycle image path
    bicycle_image = pygame.transform.scale(bicycle_image, (100, 100))  # Resize bicycle image to fit

    # Load currency image
    currency_image = pygame.image.load("currency(climate runner).png")  # Replace with your currency image path
    currency_image = pygame.transform.scale(currency_image, (60, 60))  # Resize currency image to fit

    # Load obstacle image
    obstacle_image = pygame.image.load("potholes(climate runner).png")  # Replace with your obstacle image path
    obstacle_image = pygame.transform.scale(obstacle_image, (100, 100))  # Resize obstacle image to fit

    # Resize car images to fit
    car_images = [pygame.transform.scale(image, (100, 100)) for image in car_images]

    # Set up fonts
    font = pygame.font.Font("mighty.ttf", 24)
    big_font = pygame.font.SysFont("Arial", 36)

    # Set up colors
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)

    # Set up coins and vehicles
    coin_width = 20
    coin_height = 20
    coin_speed = 4
    coins = []
    vehicles = []
    obstacles = []

    # Function to render multiline text
    def render_multiline_text(text, font, color, max_width):
        lines = []
        words = text.split(' ')
        current_line = ""

        for word in words:
            test_line = current_line + word + ' '
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '
        if current_line:
            lines.append(current_line)

        return lines

    # Game loop
    while True:
        # Draw the background
        screen.blit(background_image, (0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not winning_screen and not game_over:  # Only run the game logic if not in winning or game over state
            # Move the player
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
                player_x += player_speed

            # Generate coins
            if random.random() < 0.05:
                coin_x = random.randint(0, screen_width - coin_width)
                coins.append([coin_x, -coin_height])

            # Generate vehicles
            if random.random() < 0.02:
                vehicle_x = random.randint(0, screen_width - 50)
                vehicle_image = random.choice(car_images)  # Choose a random car image
                vehicles.append([vehicle_x, -50, vehicle_image])  # Store position and image

            # Generate obstacles
            if random.random() < 0.03:
                obstacle_x = random.randint(0, screen_width - 50)
                obstacles.append([obstacle_x, -50])

            # Move and draw coins
            for coin in coins:
                coin[1] += coin_speed
                if coin[1] > screen_height:
                    coins.remove(coin)
                elif (coin[0] <= player_x + player_width and
                      coin[0] + coin_width >= player_x and
                      coin[1] + coin_height >= player_y and
                      coin[1] <= player_y + player_height):
                    player_currency += 10
                    coins.remove(coin)

            # Move and draw vehicles
            for vehicle in vehicles:
                vehicle[1] += 8
                if vehicle[1] > screen_height:
                    vehicles.remove(vehicle)
                elif (vehicle[0] <= player_x + player_width and
                      vehicle[0] + 50 >= player_x and
                      vehicle[1] + 50 >= player_y and
                      vehicle[1] <= player_y + player_height):
                    # Check if the player can purchase the vehicle
                    if player_currency >= vehicle_price:
                        purchase_screen = True
                        can_increase_health = True
                        vehicles.remove(vehicle)  # Remove vehicle after collision
                    else:
                        game_over = True
                        game_over_message = "Game Over! You hit a vehicle without enough currency."
                        break

            # Move and draw obstacles
            for obstacle in obstacles:
                obstacle[1] += 4
                if obstacle[1] > screen_height:
                    obstacles.remove(obstacle)
                elif (obstacle[0] <= player_x + player_width and
                      obstacle[0] + 50 >= player_x and
                      obstacle[1] + 50 >= player_y and
                      obstacle[1] <= player_y + player_height):
                    # Game over if player collides with obstacles
                    game_over = True
                    game_over_message = "Game Over! You hit a pothole."
                    break

            # Draw currency images instead of rectangles
            for coin in coins:
                screen.blit(currency_image, (coin[0], coin[1]))  # Draw currency image

            # Draw vehicles using images
            for vehicle in vehicles:
                screen.blit(vehicle[2], (vehicle[0], vehicle[1]))  # Draw the car image

            # Draw the current vehicle based on player state
            if current_vehicle == "bicycle":
                screen.blit(bicycle_image, (player_x, player_y))  # Draw the bicycle image
            else:
                rotated_car = pygame.transform.rotate(current_vehicle, 180)  # Rotate car image 180 degrees
                screen.blit(rotated_car, (player_x, player_y))  # Draw the rotated car image

            # Display vehicle comments based on currency and position
            for vehicle in vehicles:
                if vehicle[1] + 50 >= player_y:  # Check if vehicle is parallel
                    if player_currency >= vehicle_price:
                        comment_surface = font.render("We should follow him", True, BLACK)
                    else:
                        comment_surface = font.render("Poor guy", True, BLACK)
                    screen.blit(comment_surface, (vehicle[0], vehicle[1] - 30))  # Display comment above the vehicle
                elif is_motor_vehicle:
                    comment_surface = font.render("Hmm!", True, BLACK)
                    screen.blit(comment_surface, (vehicle[0], vehicle[1] - 30))  # Display "Hmm!" for motor vehicles

            # Draw obstacles using images
            for obstacle in obstacles:
                screen.blit(obstacle_image, (obstacle[0], obstacle[1]))  # Draw the obstacle image

            # Display currency and environment life
            currency_text = f"Currency: {player_currency} | Environment Life: {environment_life}"
            text_surface = font.render(currency_text, True, BLACK)
            screen.blit(text_surface, (20, 20))

            # Purchase Decision Screen
            if purchase_screen:
                purchase_surface = big_font.render("Press 'B' to Buy or 'S' to Skip", True, BLACK)
                screen.blit(purchase_surface, (screen_width // 2 - purchase_surface.get_width() // 2, screen_height // 2))

                # Handle input for purchase decision
                keys = pygame.key.get_pressed()
                if keys[pygame.K_b]:  # Buy vehicle
                    if player_currency >= vehicle_price:
                        is_motor_vehicle = True
                        player_currency -= vehicle_price
                        last_environment_tick = pygame.time.get_ticks()
                        last_health_increase = pygame.time.get_ticks()
                        comment_displayed = False
                        current_vehicle = random.choice(car_images)  # Set to a random car image
                        purchase_screen = False
                elif keys[pygame.K_s]:  # Skip purchase
                    purchase_screen = False

            # Handle environment life reduction or increase
            if is_motor_vehicle:
                if pygame.time.get_ticks() - last_environment_tick > 5000:  # Starts decreasing after 5 seconds
                    environment_life -= 1
                    last_environment_tick = pygame.time.get_ticks()

                # Change vehicle comments after buying
                for vehicle in vehicles:
                    comment_surface = font.render("Hmm!", True, BLACK)
                    screen.blit(comment_surface, (vehicle[0], vehicle[1] - 30))
            elif can_increase_health:
                if pygame.time.get_ticks() - last_health_increase >= health_increase_time:
                    if environment_life < max_environment_life:
                        environment_life += 1
                        last_health_increase = pygame.time.get_ticks()

                        # Check for win condition
                        if environment_life >= max_environment_life:
                            winning_screen = True  # Trigger winning screen

        # Handle win or game over screens
        if winning_screen:
            screen.blit(winning_image, (0, 0))  # Display winning image
            if not show_message:
                message_displayed_time = pygame.time.get_ticks()
                show_message = True
            elif show_message and pygame.time.get_ticks() - message_displayed_time >= 2000:  # Wait for 2 seconds
                win_message = (
                    "I want to take a moment to acknowledge the incredible impact you've had. "
                    "Even though you may not always feel the need to change or adapt, "
                    "your consistent efforts have brought about positive change in the world around you. "
                    "Your dedication and the results you achieve speak volumes. "
                    "I truly admire your ability to stay true to yourself while making a difference. "
                    "Thank you for being a force for good."
                )

                # Render multiline text
                lines = render_multiline_text(win_message, big_font, BLACK, screen_width - 40)  # 40 for padding
                for i, line in enumerate(lines):
                    win_surface = big_font.render(line, True, BLACK)
                    screen.blit(win_surface,
                                (screen_width // 2 - win_surface.get_width() // 2, screen_height // 2 - 20 + i * 40))

        elif game_over:
            screen.blit(losing_image, (0, 0))  # Display losing image
            if not show_message:
                message_displayed_time = pygame.time.get_ticks()
                show_message = True
            elif show_message and pygame.time.get_ticks() - message_displayed_time >= 2000:  # Wait for 2 seconds
                over_surface = big_font.render(game_over_message, True, BLACK)
                screen.blit(over_surface, (screen_width // 2 - over_surface.get_width() // 2, screen_height // 2 + 50))

        # Handle exit with ESC key
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # Use ESC to exit
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        pygame.time.delay(30)

if __name__ == "__main__":
    run_game()
