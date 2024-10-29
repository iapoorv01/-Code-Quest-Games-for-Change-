import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window for both PC and phone screen sizes
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Set up the game title
pygame.display.set_caption("Eco-Warrior")

# Set up the game clock
clock = pygame.time.Clock()

# Load images
player_image = pygame.image.load("garbagepicker.png")
trash_images = [pygame.image.load("trash.png"), pygame.image.load("trash2.png"), pygame.image.load("trash3.png")]
polluter_image = pygame.image.load("polluter.png")
power_up_image = pygame.image.load("powerup.png")
background_image = pygame.image.load("background.jpg")
win_image = pygame.image.load("youwin.png")
game_over_image = pygame.image.load("gameover.png")
# Scale images to fit the mobile screen size
player_image = pygame.transform.scale(player_image, (60, 70))
trash_images = [pygame.transform.scale(img, (30, 30)) for img in trash_images]
polluter_image = pygame.transform.scale(polluter_image, (60, 60))
power_up_image = pygame.transform.scale(power_up_image, (40, 40))
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
win_image = pygame.transform.scale(win_image, (screen_width, screen_height))
game_over_image = pygame.transform.scale(game_over_image, (screen_width, screen_height))



# Define sizes for trash and polluters globally
trash_size = trash_images[0].get_width()
polluter_size = polluter_image.get_width()

# Load sounds
collect_sound = pygame.mixer.Sound("enemy.wav")
hit_sound = pygame.mixer.Sound("explode.wav")
powerup_sound = pygame.mixer.Sound("shoot.wav")
button_click_sound = pygame.mixer.Sound("click.mp3")  # Sound for button click
background_music = pygame.mixer.music.load("moonlight.wav")
pygame.mixer.music.play(-1)  # Loop the background music indefinitely

# Set up the player
player_size = player_image.get_width()
player_pos = [screen_width / 2, screen_height / 2]
player_speed = 5
player_health = 3  # Player health
player_score = 0   # Player score

# Set up power-ups
power_up_size = power_up_image.get_width()
power_up_pos = [random.randint(0, screen_width - power_up_size), random.randint(0, screen_height - power_up_size)]
power_up_active = False
power_up_duration = 300  # Duration of power-up effect in frames

# Global variables for game settings
polluter_speed = 2
max_polluters = 3
max_trash = 5
trash_pos = []
trash_collected = []
polluter_pos = []

# Level settings
level_settings = {
    1: {"polluter_speed": 2, "max_polluters": 3, "max_trash": 5},
    2: {"polluter_speed": 3, "max_polluters": 5, "max_trash": 7},
    3: {"polluter_speed": 4, "max_polluters": 7, "max_trash": 9}
}

# Level selection function
def select_level():
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont("Arial", 45)
    title_text = font.render("Select Level", True, (0, 128, 0))
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))

    # Draw level buttons
    button_color = (200, 200, 200)
    hover_color = (150, 150, 150)
    level_buttons = []
    for level in range(1, 4):
        button_rect = pygame.Rect(screen_width // 2 - 50, 200 + 60 * level, 100, 40)
        level_buttons.append((button_rect, level))
        pygame.draw.rect(screen, button_color, button_rect)
        level_text = font.render(f"Level {level}", True, (0, 0, 0))
        screen.blit(level_text, (button_rect.x + 10, button_rect.y + 5))

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
                        button_click_sound.play()
                        return level

        # Change color on hover
        for rect, level in level_buttons:
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, hover_color, rect)
            else:
                pygame.draw.rect(screen, button_color, rect)
            level_text = font.render(f"Level {level}", True, (0, 0, 0))
            screen.blit(level_text, (rect.x + 10, rect.y + 5))

        pygame.display.update()

# Apply level settings
def apply_level_settings(level):
    global polluter_speed, max_polluters, max_trash, trash_pos, trash_collected, polluter_pos
    settings = level_settings[level]
    polluter_speed = settings["polluter_speed"]
    max_polluters = settings["max_polluters"]
    max_trash = settings["max_trash"]

    # Reset trash positions and polluters based on the selected level
    trash_pos = [[random.randint(0, screen_width - trash_size), random.randint(0, screen_height - trash_size)] for _ in range(max_trash)]
    trash_collected = [False] * max_trash

    polluter_pos = [[random.randint(0, screen_width - polluter_size), random.randint(0, screen_height - polluter_size)] for _ in range(max_polluters)]

# Main game loop
def game_loop():
    global player_pos, player_speed, player_health, player_score, power_up_active, powerup_timer

    # Create a faded background surface
    faded_background = pygame.Surface((screen_width, screen_height))
    faded_background.blit(background_image, (0, 0))
    faded_background.set_alpha(150)  # Set transparency

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get the pressed keys
        keys = pygame.key.get_pressed()

        # Move the player
        if keys[pygame.K_UP]:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN]:
            player_pos[1] += player_speed
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed

        # Boundary check for the player
        player_pos[0] = max(0, min(player_pos[0], screen_width - player_size))
        player_pos[1] = max(0, min(player_pos[1], screen_height - player_size))

        # Move the polluters
        for i in range(len(polluter_pos)):
            polluter_pos[i][0] += polluter_speed
            if polluter_pos[i][0] > screen_width:
                polluter_pos[i][0] = 0

        # Check for collisions with trash
        for i in range(len(trash_pos)):
            if (player_pos[0] < trash_pos[i][0] + trash_size and
                player_pos[0] + player_size > trash_pos[i][0] and
                player_pos[1] < trash_pos[i][1] + trash_size and
                player_pos[1] + player_size > trash_pos[i][1]):
                if not trash_collected[i]:
                    trash_collected[i] = True
                    player_score += 1
                    collect_sound.play()

        # Check for collisions with polluters
        for i in range(len(polluter_pos)):
            if (player_pos[0] < polluter_pos[i][0] + polluter_size and
                player_pos[0] + player_size > polluter_pos[i][0] and
                player_pos[1] < polluter_pos[i][1] + polluter_size and
                player_pos[1] + player_size > polluter_pos[i][1]):
                player_health -= 1
                hit_sound.play()
                if player_health <= 0:
                    screen.blit(game_over_image, (0, 0))  # Show game over image
                    pygame.display.flip()
                    pygame.time.wait(3000)  #WAit for 3 sec before quitting
                    pygame.quit()
                    sys.exit()

        # Check if all trash has been collected
        if all(trash_collected):
            screen.blit(win_image, (0, 0))  # Show game over image
            pygame.display.flip()
            pygame.time.wait(3000)  #
            pygame.quit()
            sys.exit()

        # Check if player collected power-up
        if (player_pos[0] < power_up_pos[0] + power_up_size and
            player_pos[0] + player_size > power_up_pos[0] and
            player_pos[1] < power_up_pos[1] + power_up_size and
            player_pos[1] + player_size > power_up_pos[1]):
            power_up_active = True
            powerup_timer = pygame.time.get_ticks()
            powerup_sound.play()
            player_speed = 8  # Increase speed as a power-up effect

        # Manage power-up duration
        if power_up_active:
            if pygame.time.get_ticks() - powerup_timer > power_up_duration:
                power_up_active = False
                player_speed = 5  # Reset speed

        # Draw everything
        screen.blit(faded_background, (0, 0))  # Draw the faded background
        screen.blit(player_image, (player_pos[0], player_pos[1]))
        for i in range(len(trash_pos)):
            if not trash_collected[i]:
                screen.blit(trash_images[i % len(trash_images)], (trash_pos[i][0], trash_pos[i][1]))  # Cycle through trash images
        for i in range(len(polluter_pos)):
            screen.blit(polluter_image, (polluter_pos[i][0], polluter_pos[i][1]))
        if not power_up_active:
            screen.blit(power_up_image, (power_up_pos[0], power_up_pos[1]))

        # Draw health and score with white color for visibility
        font = pygame.font.SysFont("Arial", 30)
        score_text = font.render(f"Score: {player_score}", True, (255, 255, 255))  # White color
        health_text = font.render(f"Health: {player_health}", True, (255, 255, 255))  # White color
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 40))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    # Run level selection
    selected_level = select_level()
    apply_level_settings(selected_level)
    game_loop()