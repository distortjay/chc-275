import pygame
import sys

# --- Setup ---
pygame.init()
W, H = 700, 350
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Geometry Dash - Deadlocked: Multi-Mode Demo")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20, True)

# --- Colors ---
BG = (30, 180, 230)
GROUND = (25, 25, 30)
CUBE = (240, 150, 20)
SHIP = (125, 240, 160)
UFO = (245, 240, 50)
PORTAL = (220, 120, 250)
SPIKE = (70, 255, 255)
SAW = (255,80,80)
TEXT = (0,0,0)

# --- Level Data Syntax ---
# 0: empty
# 1: spike
# 2: ship portal
# 3: ufo portal
# 4: saw (wider)
# Format: [ (type, y_offset) ]
TILE = 32
LEVEL = []
LEVEL += [(0,0)]*8
LEVEL += [(1, 0), (0,0), (1,0), (1,0), (0,0), (2,0)]        # Ship Portal
LEVEL += [(0,0), (1,0), (1,0), (1,0), (0,0)] * 2
LEVEL += [(1, 0), (1,0), (1,0), (0,0), (3,0)]               # UFO Portal
LEVEL += [(1,0), (1,0), (0,0)] * 2
LEVEL += [(0,0), (1,0), (0,0), (1,0), (4, 8), (0,0), (1,0), (0,0)]
LEVEL += [(2,0)]  # Ship again
LEVEL += [(0,0), (1,0)] * 4
LEVEL += [(0,0)]*10

LEVEL_LENGTH = len(LEVEL)

# --- Mode Definitions ---
MODE_CUBE = "cube"
MODE_SHIP = "ship"
MODE_UFO = "ufo"
MODES = [MODE_CUBE, MODE_SHIP, MODE_UFO]

# --- Player ---
player = pygame.Rect(80, H-90-TILE, TILE, TILE)
mode = MODE_CUBE
vel_y = 0
on_ground = False
alive = True
scroll = 0
run_speed = 6

# --- Functions for Portals/Obstacles ---
def draw_ground(scroll):
    y = H-80
    pygame.draw.rect(screen, GROUND, (0, y, W, 80))

def draw_level(scroll):
    base_y = H-80
    for i, (thing, yoff) in enumerate(LEVEL):
        x = i*TILE - scroll
        y = base_y - yoff
        # skip far-out tiles for perf
        if x+TILE < 0 or x > W:
            continue
        if thing == 1:
            # Spike
            pts = [(x,y), (x+TILE//2,y-TILE), (x+TILE,y)]
            pygame.draw.polygon(screen, SPIKE, pts)
        elif thing == 2:
            # Ship Portal
            pygame.draw.ellipse(screen, PORTAL, (x+2,y-TILE//2,TILE-4,TILE))
            pygame.draw.rect(screen, SHIP, (x+10,y-TILE//3+7,12,15))
        elif thing == 3:
            # UFO Portal
            pygame.draw.ellipse(screen, PORTAL, (x+2,y-TILE//2,TILE-4,TILE))
            pygame.draw.ellipse(screen, UFO, (x+6,y-TILE//3+8,16,11))
        elif thing == 4:
            # Saw
            pygame.draw.circle(screen, SAW, (x+TILE//2,y-8), TILE//2)
            for a in range(8):
                ang = a*3.14/4
                tip = (x+TILE//2+int(20*pygame.math.Vector2(1,0).rotate_rad(ang).x),
                       y-8+int(20*pygame.math.Vector2(1,0).rotate_rad(ang).y))
                pygame.draw.line(screen, (220,220,220), (x+TILE//2,y-8), tip, 2)

def draw_player(mode, y, alive):
    color = CUBE if mode==MODE_CUBE else SHIP if mode==MODE_SHIP else UFO
    x = 80
    if mode == MODE_CUBE:  # cube
        pygame.draw.rect(screen, color, (x, y, TILE, TILE), border_radius=6)
    elif mode == MODE_SHIP: # ship triangle
        pts = [(x,y+TILE), (x+TILE//2, y), (x+TILE, y+TILE)]
        pygame.draw.polygon(screen, color, pts)
    elif mode == MODE_UFO: # UFO oval
        pygame.draw.ellipse(screen, color, (x, y, TILE, TILE//1.2))
    # death effect:
    if not alive:
        pygame.draw.line(screen, (0,0,0), (x, y), (x+TILE, y+TILE), 4)
        pygame.draw.line(screen, (0,0,0), (x+TILE, y), (x, y+TILE), 4)

def check_collision(mode, y_):
    cube_box = pygame.Rect(80, y_, TILE, TILE)
    base_y = H-80
    for idx, (thing, yoff) in enumerate(LEVEL):
        spike_x = idx*TILE - scroll
        y = base_y - yoff
        spike_rect = pygame.Rect(spike_x, y-TILE+2, TILE, TILE)
        if thing == 1 or thing == 4:
            # Ship mode is more forgiving (small triangle), UFO/cube full box
            if mode == MODE_SHIP:
                trix = 80 + TILE//2
                triy = y_
                if spike_rect.collidepoint(trix, triy):
                    return True
            else:
                if cube_box.colliderect(spike_rect):
                    return True
    return False

def check_portal(mode, y_):
    cube_box = pygame.Rect(80, y_, TILE, TILE)
    base_y = H-80
    for idx, (thing, yoff) in enumerate(LEVEL):
        x = idx*TILE - scroll
        y = base_y - yoff
        portal_rect = pygame.Rect(x, y-TILE//2, TILE, TILE)
        # Only respond if we're overlapping + in center of portal
        if thing==2 and cube_box.colliderect(portal_rect) and mode!=MODE_SHIP:
            return MODE_SHIP
        if thing==3 and cube_box.colliderect(portal_rect) and mode!=MODE_UFO:
            return MODE_UFO
        if thing==2 and cube_box.colliderect(portal_rect) and mode==MODE_SHIP:  # flip back to cube
            return MODE_CUBE
        if thing==3 and cube_box.colliderect(portal_rect) and mode==MODE_UFO:   # flip back to cube
            return MODE_CUBE
    return mode

def reset():
    global player, vel_y, on_ground, alive, scroll, mode
    player.y = H-90-TILE
    vel_y = 0
    on_ground = False
    alive = True
    scroll = 0
    mode = MODE_CUBE

# --- HUD ---
def hud(distance, mode, alive):
    s = f"{distance}m   MODE: {mode.upper()}"
    text = font.render(s, True, TEXT)
    screen.blit(text, (7, 7))
    if not alive:
        text2 = font.render("DEAD! Press [R] to Restart", True, (230,30,30))
        screen.blit(text2, (W//2 - text2.get_width()//2, 70))
    elif distance > LEVEL_LENGTH*TILE//10 - 10:
        text3 = font.render("YOU WIN! Press [R] to play again!", True, (10,210,10))
        screen.blit(text3, (W//2 - text3.get_width()//2, 70))

# --- Game loop ---
distance = 0
while True:
    clock.tick(60)
    screen.fill(BG)
    draw_ground(scroll)
    draw_level(scroll)

    # --- Jump/Fly/Bounce Logic ---
    keys = pygame.key.get_pressed()
    if alive and not (distance > LEVEL_LENGTH*TILE//10 - 10):
        # GRAVITY MODES
        if mode == MODE_CUBE:
            vel_y += 0.9
            if player.y+TILE >= H-80:
                player.y = H-80-TILE
                vel_y = 0
                on_ground = True
            else:
                on_ground = False
            if keys[pygame.K_SPACE] and on_ground:
                vel_y = -14
            player.y += int(vel_y)
        elif mode == MODE_SHIP:
            if keys[pygame.K_SPACE]:
                vel_y -= 0.55  # Go up if held
            vel_y += 0.42     # Fall
            player.y += int(vel_y)
            if player.y + TILE > H-80:
                player.y = H-80-TILE
                vel_y = 0
            if player.y < 10:
                player.y = 10
                vel_y = 0
        elif mode == MODE_UFO:
            vel_y += 0.85
            if player.y + TILE >= H-80:
                player.y = H-80-TILE
                vel_y = 0
                on_ground = True
            else:
                on_ground = False
            # Tap bounce up
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and on_ground:
                    vel_y = -13
            player.y += int(vel_y)
        else:
            player.y += int(vel_y)

        # Level scroll
        scroll += run_speed
        if scroll//TILE > LEVEL_LENGTH-4:
            alive = False  # Win!

        # Collision
        if check_collision(mode, player.y):
            alive = False

        # Portal transitions
        m2 = check_portal(mode, player.y)
        if m2 != mode:
            mode = m2

        # Distance
        distance = min(scroll//10, LEVEL_LENGTH*TILE//10)
    else:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r:
                reset()
                distance = 0

    # Controls the UFO bounce and quit
    if mode != MODE_UFO:
        for event in pygame.event.get():
            if event.type==pygame.QUIT: 
                pygame.quit(); sys.exit()
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r and not alive:
                reset()
                distance = 0

    draw_player(mode, player.y, alive)
    hud(distance, mode, alive)
    pygame.display.flip()