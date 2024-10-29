import pygame
import sys
import tkinter as tk
import customtkinter as ctk
import math
import random
import webbrowser
import numpy as np
import imageio
from weather_game import WeatherPredictionGame
from quiz_game import TriviaQuizGame
from eco_adventure import EcoAdventureGame
from pollution_puzzle import GameState
from savetree import Game
from eco_warrior import EcoWarrior
from food_for_thought import FoodForThoughtGame
from snake import OceanCleanupGame
from Pollution_Fighter import mainfighter
from flappymain import FlappyDoom
from Climate_runner import run_game

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Main Menu")

# Load images for icons
icons = {
    "flappy_doom": pygame.image.load("flappyicon.jpg"),
    "weather": pygame.image.load("weather_icon.jpg"),
    "trivia": pygame.image.load("quiz_icon.jpg"),
    "eco_adventure": pygame.image.load("eco_adventure_icon.png"),
    "pollution": pygame.image.load("puzzle_game_icon.png"),
    "eco_warrior": pygame.image.load("eco_warrior_icon.jpg"),
    "food_thought": pygame.image.load("foodthought_icon.png"),
    "save_tree": pygame.image.load("treesavericon.jpg"),
    "ocean_cleanup": pygame.image.load("snake_icon.jpg"),
    "pollution_fighter": pygame.image.load("pollution_monster.jpg"),
    "climate_runner": pygame.image.load("climate runner.png"),
}

# Load model frames using list comprehension
def load_model_frames():
    return [pygame.image.load(f"model_frame/{i}.png") for i in range(1, 301)]

# Load LinkedIn icon
linkedin_icon = pygame.image.load("linked_icon.png")
linkedin_icon = pygame.transform.scale(linkedin_icon, (50, 50))

# Load mute icons
mute_icon = pygame.image.load("mute.png")
unmute_icon = pygame.image.load("unmute.png")

# Load and set up sounds
intro_sound = pygame.mixer.Sound("intro.mp3")
pygame.mixer.music.load("moonlight.wav")
thunder_sound = pygame.mixer.Sound("thunder.mp3")
rain_sound = pygame.mixer.Sound("raaineffect.mp3")
sound_muted = False

# Fonts
# Fonts
font = pygame.font.Font("balo.otf", 72)
fon1=pygame.font.Font("font.otf", 42)
quote_font = pygame.font.Font("mighty.ttf", 44)  # Increased size and made bold

import pygame
import sys

def fade_in_stay_fade_out(text, position, fade_in_time=255, display_time=3000, fade_out_time=255):
    text_color = (218, 165, 32)
    title_instruction = font.render(text, True, text_color)
    title_instrect = title_instruction.get_rect(midright=position)
    FPS = 60
    # Fade settings
    alpha = 0
    fade_in = True
    fade_out = False
    display_start_time = pygame.time.get_ticks()  # Start time for display
    clock = pygame.time.Clock()

    # Main loop for effects
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fade in
        if fade_in:
            alpha += 5
            if alpha >= fade_in_time:
                alpha = fade_in_time
                fade_in = False  # Stop fading in

        # Check if it has displayed for the required time
        if not fade_in and not fade_out:
            if pygame.time.get_ticks() - display_start_time >= display_time:
                fade_out = True  # Start fading out after staying for the duration

        # Fade out
        if fade_out:
            alpha -= 5
            if alpha <= 0:
                alpha = 0
                break  # Exit the loop after fading out

        # Set the alpha to the text
        title_instruction.set_alpha(alpha)
        screen.blit(title_instruction, title_instrect)
        pygame.display.flip()
        clock.tick(FPS)

# Ensure to initialize Pygame, create a screen, and define `font` before calling this function.

# Snowfall class
class Snowflake:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.size = random.randint(2, 5)
        self.speed = random.uniform(0.5, 1.5)
        self.wind_speed = random.uniform(-0.5, 0.5)

    def fall(self):
        self.y += self.speed
        self.x += self.wind_speed
        if self.y > HEIGHT:
            self.y = random.randint(-20, 0)
            self.x = random.randint(0, WIDTH)

class RainDrop:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.length = random.randint(15, 25)  # Increased length for realism
        self.width = random.uniform(1, 3)  # Varying width
        self.speed = random.uniform(4, 8)  # Slightly varied speed
        # Set the color to a grayish color with some transparency
        gray_value = random.randint(150, 200)  # Control the shade of gray
        self.color = (gray_value, gray_value, gray_value, random.randint(150, 255))  # RGBA

    def fall(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-HEIGHT, 0)
            self.x = random.randint(0, WIDTH)
            self.length = random.randint(15, 25)
            self.width = random.uniform(1, 3)  # Reset width for new drop


def draw_rain(rain_drops):
    for drop in rain_drops:
        drop.fall()
        pygame.draw.line(screen, drop.color, (drop.x, drop.y), (drop.x, drop.y + drop.length), int(drop.width))



def load_gif_frames(new_width, new_height):
    gif = imageio.get_reader('pixverse-2Fmp4-2Fmedia-2Fweb-2-unscreen.gif')
    frames = []
    for frame in gif:
        frame_array = np.array(frame)[:, :, :3]  # Get RGB only
        rotated_frame = np.rot90(frame_array)
        surface = pygame.Surface((new_height, new_width), pygame.SRCALPHA)
        surface.blit(pygame.surfarray.make_surface(rotated_frame), (0, 0))
        frames.append(pygame.transform.scale(surface, (new_width, new_height)))  # Resize here
    return frames


def load_new_gif_frames(new_width, new_height):
    newgif = imageio.get_reader('dancepolar bear.gif')
    frames = []
    for frame in newgif:
        framenew_array = np.array(frame)[:, :, :3]  # Get RGB only
        rotatednew_frame = np.rot90(framenew_array)
        surface = pygame.Surface((new_height, new_width), pygame.SRCALPHA)
        surface.blit(pygame.surfarray.make_surface(rotatednew_frame), (0, 0))
        frames.append(pygame.transform.scale(surface, (new_width, new_height)))  # Resize here
    return frames
def show_intro():
    gif = imageio.get_reader('intro.gif')
    intro_sound.play(0)

    for frame in gif:
        frame_array = np.array(frame)
        frame_surface = pygame.surfarray.make_surface(frame_array[:, :, :3])
        frame_surface = pygame.transform.scale(frame_surface, (WIDTH - 920, HEIGHT+900))
        frame_surface = pygame.transform.rotate(frame_surface, -90)

        # Calculate the center position
        frame_rect = frame_surface.get_rect()
        frame_rect.center = (WIDTH // 2, HEIGHT // 2)

        # Blit the frame at the center
        screen.blit(frame_surface, frame_rect.topleft)
        pygame.display.flip()
        pygame.time.delay(100)

    intro_sound.stop()

def toggle_sound():
    global sound_muted
    sound_muted = not sound_muted
    if sound_muted:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

# Define the quotes for each game
game_quotes = [
    "Navigate through the skies while avoiding doom and learn about air pollution!",
    "Predict weather patterns to understand climate change and protect our planet!",
    "Test your knowledge on environmental issues and the impact of climate change!",
    "Embark on eco-friendly adventures and discover sustainable practices!",
    "Solve puzzles to address pollution challenges and promote a cleaner Earth!",
    "Join the fight against climate change and become an eco-warrior!",
    "Learn fascinating facts about food sustainability and its impact on the climate!",
    "Protect forests and understand the importance of trees in combating climate change!",
    "Engage in ocean cleanup efforts and see how pollution affects marine life!",
    "Take action against pollution and learn ways to make a positive impact!",
    "Will you pave the way for a sustainable future or drive towards destruction? The journey begins with you!"
]

def render_3d_text(text, position, color, shadow_color=(50, 50, 50)):
    # Create shadow
    shadow_surface = quote_font.render(text, True, shadow_color)
    shadow_rect = shadow_surface.get_rect(center=(position[0] + 2, position[1] + 2))
    screen.blit(shadow_surface, shadow_rect)

    # Create main text
    text_surface = quote_font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)


def glow_effect(icon):
    # Create a surface for the glow effect
    glow_surface = pygame.Surface((icon.get_width() + 20, icon.get_height() + 20), pygame.SRCALPHA)

    # Draw a glow effect (using a soft color and transparency)
    for i in range(10, 0, -1):
        # Define the color with decreasing alpha for a fade effect
        color = (255, 215, 0, 100 // i)  # Yellow glow
        pygame.draw.circle(glow_surface, color, (glow_surface.get_width() // 2, glow_surface.get_height() // 2), i * 2)

    return glow_surface


def shine_effect(icon):
    shine_surface = pygame.Surface(icon.get_size(), pygame.SRCALPHA)
    shine_surface.fill((255, 255, 255, 100))
    shine_surface.set_colorkey((255, 255, 255, 0))
    for i in range(30):
        pygame.draw.circle(shine_surface, (255, 255, 255, max(0, 100 - i * 3)),
                           (icon.get_width() // 2, icon.get_height() // 2), 60 - i)
    return shine_surface

def draw_lightning(last_flash_time):
    current_time = pygame.time.get_ticks()
    if current_time - last_flash_time > random.randint(15000, 16000):  # 15-16 seconds
        screen.fill((255, 255, 255))  # White flash
        thunder_sound.play()  # Play thunder sound
        pygame.display.flip()
        pygame.time.delay(100)
        return current_time, True  # Return new last flash time and flag to start rain
    return last_flash_time, False  # Return last flash time and no flag



def main_menu():
    if not sound_muted:
        pygame.mixer.music.play(-1)

    pulse_speed = 0.3
    pulse_size = 0
    pulse_direction = 1
    snowflakes = [Snowflake() for _ in range(100)]
    rain_drops = [RainDrop() for _ in range(100)]  # Create rain drops
    rain_active = False
    rain_start_time = 0

    color_change_offset = 0
    model_frames = load_model_frames()  # Load model frames
    current_frame_index = 0
    scroll_offset = 0
    scroll_speed = 5
    icon_spacing = 300

    # Load the exit icon
    exit_icon = pygame.image.load("exit_icon.jpeg")
    exit_icon_resized = pygame.transform.scale(exit_icon, (30, 30))

    # Positioning for the exit icon
    exit_button_rect = pygame.Rect(WIDTH - 160, HEIGHT - 40, 50, 50)

    last_flash_time = pygame.time.get_ticks()  # Initialize last flash time
    # Load GIF frames
    gif_frames = load_gif_frames(400, 300)
    gif_frame_index = 0
    gif_frame_delay = 100  # Delay between frames in milliseconds
    last_gif_update = pygame.time.get_ticks()

    newgif_frames = load_new_gif_frames(500, 400)
    newgif_frame_index = 0
    newgif_frame_delay = 50  # Delay between frames in milliseconds
    lastnew_gif_update = pygame.time.get_ticks()
    fade_in_stay_fade_out("Scroll down using V", (WIDTH - 40, 400))

    max_scroll_limit = -(len(icons) * icon_spacing) + 500  # Calculate maximum scroll limit

    while True:
        screen.fill((0, 0, 0))

        for flake in snowflakes:
            flake.fall()
            pygame.draw.circle(screen, (255, 255, 255), (flake.x, flake.y), flake.size)

        pulse_size += pulse_speed * pulse_direction
        if pulse_size > 10 or pulse_size < -10:
            pulse_direction *= -1

        color_change_offset += 1
        r = (math.sin(color_change_offset * 0.05) * 127 + 128)
        g = (math.sin(color_change_offset * 0.05 + 2) * 127 + 128)
        b = (math.sin(color_change_offset * 0.05 + 4) * 127 + 128)
        title_color = (int(r), int(g), int(b))

        title_text = font.render("Climate Action Games", True, title_color)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100 + pulse_size))
        screen.blit(title_text, title_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            scroll_offset += scroll_speed
            current_frame_index = (current_frame_index - 1) % len(model_frames)
        if keys[pygame.K_DOWN]:
            scroll_offset -= scroll_speed
            current_frame_index = (current_frame_index + 1) % len(model_frames)

        # Clamp scroll_offset to prevent scrolling too far
        scroll_offset = max(scroll_offset, max_scroll_limit)  # Prevent scrolling up past the first icon
        scroll_offset = min(scroll_offset, 0)  # Prevent scrolling down past the last icon

        current_frame = model_frames[current_frame_index]
        frame_rect = current_frame.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 200))
        screen.blit(current_frame, frame_rect)

        # Icons rendering
        for i, (name, icon) in enumerate(icons.items()):
            icon_resized = pygame.transform.scale(icon, (200, 200))
            x = WIDTH // 2 + 560 if i % 2 == 0 else WIDTH // 4 - 140
            y = (i * icon_spacing) + 600 + scroll_offset
            glow_surface = glow_effect(icon_resized)
            shine_surface = shine_effect(icon_resized)
            screen.blit(icon_resized, (x, y - 30))
            screen.blit(shine_surface, (x, y))
            description = game_quotes[i].split(' ')
            mid_point = len(description) // 2
            line1 = ' '.join(description[:mid_point])
            line2 = ' '.join(description[mid_point:])

            # Render the text for the icon
            render_3d_text(line1, (x + 50, y + 120), (255, 215, 0))  # Yellow text for line 1
            render_3d_text(line2, (x + 50, y + 160), (255, 215, 0))

        mute_button_rect = pygame.Rect(WIDTH - 90, HEIGHT - 40, 80, 40)
        current_icon = unmute_icon if not sound_muted else mute_icon
        icon_resized = pygame.transform.scale(current_icon, (30, 30))
        screen.blit(icon_resized, (mute_button_rect.x + 5, mute_button_rect.y + 5))

        # Draw the exit icon
        screen.blit(exit_icon_resized, (exit_button_rect.x, exit_button_rect.y))

        linkedin_rect = linkedin_icon.get_rect(center=(WIDTH - 30, HEIGHT - 20))
        linkedin_icon_resized = pygame.transform.scale(linkedin_icon, (50, 50))
        screen.blit(linkedin_icon_resized, linkedin_rect)

        # Update thunder effect
        last_flash_time, start_rain = draw_lightning(last_flash_time)

        if start_rain:
            rain_active = True
            rain_start_time = pygame.time.get_ticks()
            rain_sound.play(-1)  # Loop rain sound

        if rain_active:
            draw_rain(rain_drops)
            if pygame.time.get_ticks() - rain_start_time > 6000:  # Rain lasts for 6 seconds
                rain_active = False  # Reset rain state
                rain_sound.stop()  # Stop rain sound after it ends

        # Update GIF frame based on delay
        current_time = pygame.time.get_ticks()
        if current_time - last_gif_update > gif_frame_delay:
            gif_frame_index = (gif_frame_index + 1) % len(gif_frames)
            last_gif_update = current_time

        currentnew_time = pygame.time.get_ticks()
        if currentnew_time - lastnew_gif_update > newgif_frame_delay:
            newgif_frame_index = (newgif_frame_index + 1) % len(newgif_frames)
            lastnew_gif_update = currentnew_time

        # Calculate the Y position for the GIF to be at the bottom of the last icon
        fourth_icon_y = (4 * icon_spacing) + 700 + scroll_offset  # Position for the 4th icon
        gif_y = fourth_icon_y + 100  # Position it 40 pixels below the last icon
        gif_x = WIDTH - gif_frames[0].get_width()  # 20 pixels from the right edge
        gif_rect = gif_frames[gif_frame_index].get_rect(topleft=(gif_x, gif_y))
        screen.blit(gif_frames[gif_frame_index], gif_rect.topleft)

        seventh_icon_y = (7 * icon_spacing) + 670 + scroll_offset
        newgif_y = seventh_icon_y + 150
        newgif_x = WIDTH // 2 - newgif_frames[0].get_width() - 700  # 20 pixels from the right edge
        newgif_rect = newgif_frames[newgif_frame_index].get_rect(topleft=(newgif_x, newgif_y))
        screen.blit(newgif_frames[newgif_frame_index], newgif_rect.topleft)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mute_button_rect.collidepoint(event.pos):
                    toggle_sound()

                if exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

                for i, (name, icon) in enumerate(icons.items()):
                    x = WIDTH // 2 + 600 if i % 2 == 0 else WIDTH // 4 - 200
                    y = (i * icon_spacing) + 600 + scroll_offset
                    icon_rect = pygame.Rect(x, y, 200, 200)

                    if icon_rect.collidepoint(event.pos):
                        if name == "flappy_doom":
                            game = FlappyDoom()
                            game.run()
                        elif name == "weather":
                            game_instance = WeatherPredictionGame()
                            game_instance.start_game()
                        elif name == "trivia":
                            root = tk.Tk()
                            game_instance = TriviaQuizGame(root)
                            root.mainloop()
                        elif name == "eco_adventure":
                            root = ctk.CTk()
                            game_instance = EcoAdventureGame(root)
                            game_instance.run()
                        elif name == "pollution":
                            game_state = GameState(WIDTH,HEIGHT)
                            game_state.run_game(screen)

                        elif name == "eco_warrior":
                            eco_warrior_game = EcoWarrior()
                            level = eco_warrior_game.select_level()
                            eco_warrior_game.apply_level_settings(level)
                            eco_warrior_game.game_loop()
                        elif name == "food_thought":
                            food_game = FoodForThoughtGame(screen)
                            food_game.run()
                        elif name == "save_tree":
                            save_tree_game = Game()
                            save_tree_game.run()
                        elif name == "ocean_cleanup":
                            snake = OceanCleanupGame()
                            snake.run_game()
                        elif name == "pollution_fighter":
                            mainfighter()
                        elif name == "climate_runner" :
                            run_game()

                    if linkedin_rect.collidepoint(event.pos):
                            webbrowser.open(
                            "https://www.linkedin.com/in/iapoorv01?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app")

if __name__ == "__main__":
    show_intro()
    main_menu()



