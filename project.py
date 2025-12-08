import pygame
import sys
import random

pygame.init()
W, H = 800, 450
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# Colors
BG = (30, 37, 94)
HILLS = (62, 78, 139)
GROUND = (96, 116, 224)
PLAYER = (250, 236, 70)
OBSTACLE = (245, 90, 71)

offset = 0

# Player setup
player_size = 40
player_x = 100
player_y = 360
player_vel_y = 0
gravity = 1
jump_power = -20
on_ground = True

# Obstacles
obstacles = []
obs_width = 30
obs_gap_min = 200
obs_gap_max = 350
obs_timer = 0
obs_spawn_interval = 70  # frames

game_over = False
font = pygame.font.SysFont(None, 56)

def reset_game():
    global player_y, player_vel_y, on_ground, obstacles, offset, obs_timer, game_over
    player_y = 360
    player_vel_y = 0
    on_ground = True
    obstacles = []
    offset = 0
    obs_timer = 0
    game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                if (event.key == pygame.K_SPACE if event.type == pygame.KEYDOWN else True) and on_ground:
                    player_vel_y = jump_power
                    on_ground = False
            else:
                reset_game()

    if not game_over:
        screen.fill(BG)
        offset += 2

        # Hills (polygon) - scrolling
        hill_points = [
            ((0 - offset) % W, 350),
            ((200 - offset) % W, 300),
            ((400 - offset) % W, 350),
            ((600 - offset) % W, 320),
            ((800 - offset) % W, 370),
            (W, H),
            (0, H)
        ]
        pygame.draw.polygon(screen, HILLS, hill_points)

        # Ground
        pygame.draw.rect(screen, GROUND, (0, 400, W, 50))

        # Spawn obstacles
        obs_timer += 1
        if obs_timer >= obs_spawn_interval:
            obs_timer = 0
            obs_x = W + random.randint(0, 50)
            obs_h = random.randint(50, 60)
            obstacles.append([obs_x, 400 - obs_h, obs_width, obs_h])

        # Move and draw obstacles
        for obs in obstacles:
            obs[0] -= 4
        obstacles = [o for o in obstacles if o[0] + o[2] > 0]
        for obs in obstacles:
            pygame.draw.rect(screen, OBSTACLE, obs)

        # Player physics
        player_vel_y += gravity
        player_y += player_vel_y

        # Ground collision
        if player_y + player_size >= 400:
            player_y = 400 - player_size
            player_vel_y = 0
            on_ground = True

        # Draw player
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        pygame.draw.rect(screen, PLAYER, player_rect)

        # Collision detection
        for obs in obstacles:
            obs_rect = pygame.Rect(obs[0], obs[1], obs[2], obs[3])
            if player_rect.colliderect(obs_rect):
                game_over = True

        pygame.display.flip()
        clock.tick(60)

    else:
        # Game over screen
        txt = font.render("Game Over! Press any key to restart.", True, (255, 255, 255))
        screen.fill(BG)
        screen.blit(txt, (W // 2 - txt.get_width() // 2, H // 2 - 40))
        pygame.display.flip()
        clock.tick(30)