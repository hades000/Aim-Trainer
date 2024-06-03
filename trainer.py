import math
import random
import time
import pygame

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

# Timing and event constants
TARGET_INCREMENT = 300
TARGET_EVENT = pygame.USEREVENT

# Game settings
TARGET_PADDING = 30
LIVES = 3
TOPBAR_HEIGHT = 50
MAX_TARGETS = 10  # Limit the number of targets

# Load background image
BACKGROUND_IMAGE = pygame.image.load('D:\\Py projects\\aim trainer project\\Aim trainer app\\wallpaperflare.com_wallpaper.jpg')
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

# Font settings
LABEL_FONT = pygame.font.SysFont("Times New Roman", 24, True)  # Enable bold font

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = (255, 215, 0)  # RGB for yellow
    SECOND_COLOR = (0, 128, 0)  # RGB for green

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), int(self.size))
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), int(self.size * 0.8))
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), int(self.size * 0.6))
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), int(self.size * 0.4))

    def collide(self, x, y):
        dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        return dis <= self.size

def draw(win, targets, elapsed_time, target_pressed, missed):
    # Draw background
    win.blit(BACKGROUND_IMAGE, (0, 0))
    
    for target in targets:
        target.draw(win)
    draw_top_bar(win, elapsed_time, target_pressed, missed)
    pygame.display.flip()  # Use flip instead of update for double buffering

def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    return f"{minutes:02d}:{seconds:02d}.{milli:02d}"

def draw_top_bar(win, elapsed_time, target_pressed, missed):
    pygame.draw.rect(win, (169, 169, 169), (0, 0, WIDTH, TOPBAR_HEIGHT))  # Use RGB for grey
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", True, (0, 0, 0))  # Anti-aliasing
    speed = round(target_pressed / elapsed_time, 1) if elapsed_time > 0 else 0
    speed_label = LABEL_FONT.render(f"Speed: {speed} clicks/sec", True, (0, 0, 0))
    hits_label = LABEL_FONT.render(f"Hits: {target_pressed}", True, (0, 0, 0))
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - missed}", True, (0, 0, 0))
    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))

def end_screen(win, elapsed_time, target_pressed, clicks):
    win.fill("white")
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", True, (0, 0, 0))
    speed = round(target_pressed / elapsed_time, 1) if elapsed_time > 0 else 0
    speed_label = LABEL_FONT.render(f"Speed: {speed} clicks/sec", True, (0, 0, 0))
    hits_label = LABEL_FONT.render(f"Hits: {target_pressed}", True, (0, 0, 0))
    accuracy = round(target_pressed / clicks * 100, 1) if clicks > 0 else 0
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", True, (0, 0, 0))
    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 120))
    win.blit(hits_label, (get_middle(hits_label), 140))
    win.blit(accuracy_label, (get_middle(accuracy_label), 160))
    pygame.display.flip()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()
    target_pressed = 0
    clicks = 0
    missed = 0
    start_time = time.time()
    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)
    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == TARGET_EVENT and len(targets) < MAX_TARGETS:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOPBAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1
        for target in targets:
            target.update()
            if target.size <= 0:
                targets.remove(target)
                missed += 1
            if click and target.collide(*mouse_pos):
                targets.remove(target)
                target_pressed += 1
            if missed >= LIVES:
                end_screen(WIN, elapsed_time, target_pressed, clicks)
                run = False
                break
        draw(WIN, targets, elapsed_time, target_pressed, missed)
    pygame.quit()

if __name__ == "__main__":
    main()
