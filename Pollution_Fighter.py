import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("pollution_character.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (80, 80))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.health = 100
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def draw_mask(self, surface):
        mask_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        for x in range(self.image.get_width()):
            for y in range(self.image.get_height()):
                if self.mask.get_at((x, y)):
                    mask_surface.set_at((x, y), (255, 0, 0, 128))  # Semi-transparent red
        surface.blit(mask_surface, self.rect.topleft)

# Pollution Monster class
class PollutionMonster(pygame.sprite.Sprite):
    def __init__(self, level, player_rect):
        super().__init__()
        self.level = level
        self.image = pygame.image.load("pollution_msmall.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.spawn_away_from_player(player_rect)
        self.health = 50 + level * 10
        self.speed = 2 + level
        self.distance_threshold = 1000

    def spawn_away_from_player(self, player_rect):
        while True:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
            if not self.rect.colliderect(player_rect):
                break

    def update(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > self.distance_threshold:
            if dx < 0:
                self.rect.x -= self.speed
            if dx > 0:
                self.rect.x += self.speed
            if dy < 0:
                self.rect.y -= self.speed
            if dy > 0:
                self.rect.y += self.speed

        if random.randint(0, 60 - self.level * 5) == 0:
            projectile = PollutionProjectile(self.rect.centerx, self.rect.centery, player.rect.center)
            return projectile
        return None

class BigMonster(PollutionMonster):
    def __init__(self, level, player_rect):
        super().__init__(level, player_rect)
        self.image = pygame.image.load("pollution_monster.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.spawn_away_from_player(player_rect)
        self.health = 150 + level * 20
        self.speed = 1 + level // 2

# Projectile class for the player's attack
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        self.image = pygame.image.load("waterbullets.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dx = (target[0] - x) / 20
        self.dy = (target[1] - y) / 20

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if (self.rect.bottom < 0 or
                self.rect.left < 0 or
                self.rect.right > SCREEN_WIDTH or
                self.rect.top > SCREEN_HEIGHT):
            self.kill()

# Pollution Projectile class for the monster's attack
class PollutionProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        self.image = pygame.image.load("pollution_bullets.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dx = (target[0] - x) / 20
        self.dy = (target[1] - y) / 20

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if (self.rect.bottom < 0 or
                self.rect.left < 0 or
                self.rect.right > SCREEN_WIDTH or
                self.rect.top > SCREEN_HEIGHT):
            self.kill()

def fade_in(screen, font, duration=5000):
    """Fades in from a black screen and displays the description text."""
    black_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    black_surface.fill((0, 0, 0))
    font = pygame.font.Font("mighty.ttf", 36)
    description_text = [
        "Welcome to Pollution Fighter!",
        "An action-packed adventure where you battle",
        "against pollution monsters to save the environment!",
        "Navigate through challenging levels, defeat enemies,",
        "and protect your health while unleashing your attacks.",
        "Can you conquer all the levels and emerge victorious?",
        "Let the fight against pollution begin!",
    ]

    line_spacing = 20  # Space between lines
    total_height = len(description_text) * (font.get_height() + line_spacing) - line_spacing

    for alpha in range(0, 256, 5):
        black_surface.set_alpha(alpha)
        screen.blit(black_surface, (0, 0))

        # Calculate starting y position to center the text block
        start_y = (SCREEN_HEIGHT - total_height) // 2

        for i, line in enumerate(description_text):
            text_surface = font.render(line, True, (255, 255, 255))  # White text
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * (font.get_height() + line_spacing)))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        pygame.time.delay(duration // 51)

# Main game function
def mainfighter():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Pollution Fighter")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 36,True)

    # Load images for win/lose screens
    win_image = pygame.image.load("youwin.png").convert()
    win_image = pygame.transform.scale(win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    lose_image = pygame.image.load("gameover.png").convert()
    lose_image = pygame.transform.scale(lose_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load background image
    background_image = pygame.image.load("pollytion_background.jpg").convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load firing sound
    fire_sound = pygame.mixer.Sound("click.mp3")  # Replace with your sound file

    win_message = "Congratulations! You defeated all the monsters!"
    lose_message = "Game Over! You ran out of health."

    all_sprites = pygame.sprite.Group()
    monsters = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    level = 1
    monster = PollutionMonster(level, player.rect)
    all_sprites.add(monster)
    monsters.add(monster)

    projectiles = pygame.sprite.Group()
    monster_projectiles = pygame.sprite.Group()

    level_won = False
    level_won_timer = 0

    running = True
    game_over = False
    game_won = False
    recently_hit = False

    # Fade-in effect
    fade_in(screen, font)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    projectile = Projectile(player.rect.centerx, player.rect.centery, (mouse_x, mouse_y))
                    all_sprites.add(projectile)
                    projectiles.add(projectile)
                    fire_sound.play()  # Play the firing sound
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Escape key to exit
                    running = False
                if event.key == pygame.K_SPACE and pygame.key.get_mods() & pygame.KMOD_ALT:  # Alt + Space
                    pygame.display.iconify()  # Minimize the window

        if not game_over:
            projectiles.update()
            monster_projectiles.update()

            for monster in monsters:
                new_projectile = monster.update(player)
                if new_projectile:
                    all_sprites.add(new_projectile)
                    monster_projectiles.add(new_projectile)

            player.update()

            hits = pygame.sprite.groupcollide(projectiles, monsters, False, False)
            for projectile, hit_monsters in hits.items():
                for monster in hit_monsters:
                    monster.health -= 10
                    projectile.kill()
                    if monster.health <= 0:
                        monster.kill()
                        if level == 5:
                            level_won = True
                            level_won_timer = pygame.time.get_ticks()
                            game_won = True
                        else:
                            level += 1
                            player.health = 100
                            if level == 5:
                                big_monster = BigMonster(level, player.rect)
                                all_sprites.add(big_monster)
                                monsters.add(big_monster)
                                for _ in range(2):
                                    small_monster = PollutionMonster(level, player.rect)
                                    all_sprites.add(small_monster)
                                    monsters.add(small_monster)
                            else:
                                monster = PollutionMonster(level, player.rect)
                                all_sprites.add(monster)
                                monsters.add(monster)

            hits = pygame.sprite.spritecollide(player, monsters, False,
                                               collided=lambda x, y: pygame.sprite.collide_mask(x, y))
            if hits and not recently_hit:
                player.health -= 10
                recently_hit = True
                if player.health <= 0:
                    game_over = True
            else:
                recently_hit = False

            hits = pygame.sprite.spritecollide(player, monster_projectiles, True)
            if hits:
                player.health -= 5
                if player.health <= 0:
                    game_over = True

            # Drawing
            screen.blit(background_image, (0, 0))
            all_sprites.draw(screen)
            player.draw_mask(screen)

            player_health_text = font.render(f'Player Health: {player.health}', True, BLACK)
            screen.blit(player_health_text, (10, 10))

            if monsters:
                monster_health_text = font.render(f'Monster Health: {monsters.sprites()[0].health}', True, BLACK)
                screen.blit(monster_health_text, (10, 40))

            level_text = font.render(f'Level: {level}', True, BLACK)
            screen.blit(level_text, (10, 70))

            if level_won:
                current_time = pygame.time.get_ticks()
                if current_time - level_won_timer < 2000:
                    win_text = font.render('Level Completed!', True, BLACK)
                    screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2))
                    if current_time - level_won_timer >= 2000:
                        game_over = True

        else:
            if game_won:
                screen.blit(win_image, (0, 0))
                win_message_text = font.render(win_message, True, BLACK)
                screen.blit(win_message_text,
                            (SCREEN_WIDTH // 2 - win_message_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
            else:
                screen.blit(lose_image, (0, 0))
                lose_message_text = font.render(lose_message, True, BLACK)
                screen.blit(lose_message_text,
                            (SCREEN_WIDTH // 2 - lose_message_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(60)

# Start the game
if __name__ == "__main__":
    mainfighter()
    pygame.quit()
