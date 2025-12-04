import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 640, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash Screen")

# Colors and font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 250)
GREEN = (50, 250, 50)

font_big = pygame.font.SysFont(None, 80)
font_small = pygame.font.SysFont(None, 40)

def draw_play_screen(win):
    win.fill(WHITE)
    # Title
    title_surf = font_big.render("GEOMETRY DASH", True, BLUE)
    win.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, HEIGHT // 2 - 120))
    # Green "ground"
    pygame.draw.rect(win, GREEN, (0, HEIGHT - 100, WIDTH, 100))
    # Play prompt
    prompt = font_small.render("Press SPACE to Play!", True, BLACK)
    win.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.update()

def main():
    in_play_screen = True
    while in_play_screen:
        draw_play_screen(WIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_play_screen = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    in_play_screen = False  # In your full game, this would start the game!
        pygame.time.Clock().tick(30)

if __name__ == "__main__":
    main()