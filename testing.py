import sys
import random
import math
import pygame

# testing.py
# Simple "Flabby Bird" (Flappy Bird-like) game using pygame.
# Single-file, no external assets. Press SPACE or click to flap. R to restart. Esc to quit.




# --- Configuration ---
WIDTH, HEIGHT = 400, 600
FPS = 60

BIRD_RADIUS = 16
BIRD_X = WIDTH // 4
GRAVITY = 0.45
FLAP_VELOCITY = -8.5
MAX_DROP_SPEED = 12
ROTATE_FACTOR = -6  # degrees per velocity unit

PIPE_WIDTH = 70
PIPE_GAP = 160
PIPE_SPEED = 3
PIPE_SPAWN_INTERVAL = 1500  # milliseconds

GROUND_HEIGHT = 80
BG_COLOR = (135, 206, 235)  # sky

# Colors
BIRD_COLOR = (255, 220, 0)
PIPE_COLOR = (34, 139, 34)
GROUND_COLOR = (159, 121, 64)
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0, 100)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flabby Bird")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("Arial", 48, bold=True)
font_small = pygame.font.SysFont("Arial", 20)

# Events
SPAWNPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNPIPE, PIPE_SPAWN_INTERVAL)


def clamp(v, a, b):
    return max(a, min(b, v))


class Bird:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = BIRD_X
        self.y = HEIGHT // 2
        self.vy = 0.0
        self.alive = True
        self.score_counted = set()

    def flap(self):
        self.vy = FLAP_VELOCITY

    def update(self):
        self.vy += GRAVITY
        self.vy = clamp(self.vy, -999, MAX_DROP_SPEED)
        self.y += self.vy

    def get_rect(self):
        return pygame.Rect(int(self.x - BIRD_RADIUS), int(self.y - BIRD_RADIUS), BIRD_RADIUS * 2, BIRD_RADIUS * 2)

    def draw(self, surf):
        # simple tilt proportional to velocity
        angle = clamp(self.vy * ROTATE_FACTOR, -45, 45)
        # draw shadow
        shadow_surf = pygame.Surface((BIRD_RADIUS * 2 + 6, BIRD_RADIUS * 2 + 6), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 100), shadow_surf.get_rect())
        surf.blit(shadow_surf, (self.x - BIRD_RADIUS + 3, self.y - BIRD_RADIUS + 8))
        # draw bird body
        pygame.draw.circle(surf, BIRD_COLOR, (int(self.x), int(self.y)), BIRD_RADIUS)
        # eye
        eye_x = int(self.x + BIRD_RADIUS * 0.4)
        eye_y = int(self.y - BIRD_RADIUS * 0.25)
        pygame.draw.circle(surf, (255, 255, 255), (eye_x, eye_y), 5)
        pygame.draw.circle(surf, (40, 40, 40), (eye_x + 2, eye_y), 2)
        # beak
        beak = [
            (int(self.x + BIRD_RADIUS * 0.9), int(self.y)),
            (int(self.x + BIRD_RADIUS * 1.5), int(self.y - 6)),
            (int(self.x + BIRD_RADIUS * 1.5), int(self.y + 6)),
        ]
        pygame.draw.polygon(surf, (255, 140, 0), beak)


class Pipe:
    def __init__(self, x):
        self.x = x
        # gap center Y
        margin = 40 + GROUND_HEIGHT
        self.gap_y = random.randint(margin + PIPE_GAP // 2, HEIGHT - margin - PIPE_GAP // 2)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def offscreen(self):
        return self.x + PIPE_WIDTH < -10

    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_y - PIPE_GAP // 2)
        bottom_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP // 2, PIPE_WIDTH, HEIGHT - (self.gap_y + PIPE_GAP // 2) - GROUND_HEIGHT)
        return top_rect, bottom_rect

    def draw(self, surf):
        top_rect, bottom_rect = self.get_rects()
        pygame.draw.rect(surf, PIPE_COLOR, top_rect)
        pygame.draw.rect(surf, PIPE_COLOR, bottom_rect)
        # simple pipe cap
        cap_h = 12
        pygame.draw.rect(surf, (20, 100, 20), (top_rect.x - 2, top_rect.height - cap_h, PIPE_WIDTH + 4, cap_h))
        pygame.draw.rect(surf, (20, 100, 20), (bottom_rect.x - 2, bottom_rect.y, PIPE_WIDTH + 4, cap_h))


def check_collision(bird, pipes):
    rect = bird.get_rect()
    # ground or ceiling
    if rect.top <= 0 or rect.bottom >= HEIGHT - GROUND_HEIGHT:
        return True
    # pipes
    for pipe in pipes:
        top_rect, bottom_rect = pipe.get_rects()
        if rect.colliderect(top_rect) or rect.colliderect(bottom_rect):
            return True
    return False


def draw_background(surf):
    surf.fill(BG_COLOR)
    # some clouds - simple circles
    for i in range(5):
        cx = 60 + i * 80
        cy = 60 + (i % 2) * 20
        pygame.draw.ellipse(surf, (255, 255, 255), (cx, cy, 80, 40))
    # ground
    pygame.draw.rect(surf, GROUND_COLOR, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))


def main():
    bird = Bird()
    pipes = []
    score = 0
    running = True
    game_over = False

    # spawn initial pipes
    for i in range(3):
        pipes.append(Pipe(WIDTH + i * (PIPE_WIDTH + 160)))

    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                if event.key == pygame.K_SPACE:
                    if game_over:
                        # restart
                        bird.reset()
                        pipes = [Pipe(WIDTH + i * (PIPE_WIDTH + 160)) for i in range(3)]
                        score = 0
                        game_over = False
                    else:
                        bird.flap()
                if event.key == pygame.K_r:
                    bird.reset()
                    pipes = [Pipe(WIDTH + i * (PIPE_WIDTH + 160)) for i in range(3)]
                    score = 0
                    game_over = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if game_over:
                        bird.reset()
                        pipes = [Pipe(WIDTH + i * (PIPE_WIDTH + 160)) for i in range(3)]
                        score = 0
                        game_over = False
                    else:
                        bird.flap()
            elif event.type == SPAWNPIPE:
                pipes.append(Pipe(WIDTH + 20))

        # update
        if not game_over:
            bird.update()
            for pipe in pipes:
                pipe.update()
                # scoring: when bird passes pipe
                if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                    pipe.passed = True
                    score += 1
            # remove offscreen
            pipes = [p for p in pipes if not p.offscreen()]

            if check_collision(bird, pipes):
                game_over = True

        # draw
        draw_background(screen)
        for pipe in pipes:
            pipe.draw(screen)
        bird.draw(screen)

        # score
        score_surf = font_big.render(str(score), True, TEXT_COLOR)
        screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 30))

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (0, 0))
            go_surf = font_big.render("GAME OVER", True, (255, 80, 80))
            screen.blit(go_surf, (WIDTH // 2 - go_surf.get_width() // 2, HEIGHT // 2 - 40))
            hint = font_small.render("Press SPACE or CLICK to restart. R to reset. Esc to quit.", True, TEXT_COLOR)
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 20))
            sub = font_small.render(f"Score: {score}", True, TEXT_COLOR)
            screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 - 80))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()