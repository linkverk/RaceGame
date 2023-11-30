import pygame
import math
from utilities import scale_image, blit_rotate_center

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 4.1)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)

TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = scale_image(pygame.image.load("imgs/finish.png"),0.5)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (260, 310)

RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.25)
GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.25)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

FPS = 120

pygame.font.init()


class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (280, 280)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

class Player2Car(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (300, 280)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

class Scoreboard:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.score = 0

    def update_score(self, time_elapsed):
        self.score = time_elapsed
        save_score(self.score)

    def draw(self, win):
        score_text = self.font.render(f"Score: {self.score} seconds", True, (255, 255, 255))
        win.blit(score_text, (WIDTH - 200, 10))


def show_scoreboard():
    scoreboard_window = pygame.display.set_mode((300, 200))
    pygame.display.set_caption("Scoreboard")

    font = pygame.font.Font(None, 36)

    with open("scores.txt", "r") as file:
        scores = [float(line.strip()) for line in file]

    scores.sort()

    while True:
        scoreboard_window.fill((255, 255, 255))

        scores_text = [font.render(f"{score} seconds", True, (0, 0, 0)) for score in scores]

        for i, score_text in enumerate(scores_text):
            scoreboard_window.blit(score_text, (50, 50 + i * 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

def save_score(score):
    with open("scores.txt", "a") as file:
        file.write(f"{score}\n")


def draw_timer(win, time_elapsed):
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Time: {time_elapsed} seconds", True, (255, 255, 255))
    win.blit(timer_text, (10, 10))


def draw(win, images, player_cars, scoreboard):
    draw_surface = pygame.Surface(WIN.get_size())
    draw_surface.fill((0, 0, 0))

    for img, pos in images:
        draw_surface.blit(img, pos)

    for player_car in player_cars:
        player_car.draw(draw_surface)

    scoreboard.draw(draw_surface)

    WIN.blit(draw_surface, (0, 0))


def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

def show_win_screen():
    win_screen = pygame.Surface(WIN.get_size())
    win_screen.set_alpha(200)
    win_screen = win_screen.convert()
    win_screen.fill((0, 0, 0))

    font = pygame.font.Font(None, 36)
    win_text = font.render("You Win!", True, (0, 255, 0))
    return_text = font.render("Return to Game", True, (255, 255, 255))
    menu_text = font.render("Go to Menu", True, (255, 255, 255))

    win_rect = win_text.get_rect(center=(win_screen.get_width() // 2, 50))
    return_rect = return_text.get_rect(center=(win_screen.get_width() // 2, 120))
    menu_rect = menu_text.get_rect(center=(win_screen.get_width() // 2, 160))

    win_screen.blit(win_text, win_rect)
    win_screen.blit(return_text, return_rect)
    win_screen.blit(menu_text, menu_rect)
    WIN.blit(win_screen, (0, 0))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if return_rect.collidepoint(mouse_pos):
                    return "return"
                elif menu_rect.collidepoint(mouse_pos):
                    return "menu"
            pygame.display.update()


run = True
clock = pygame.time.Clock()

images = [(GRASS, (0, 0)), (TRACK, (41, 11.8)),
          (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
player_car1 = PlayerCar(2, 4)
player_car2 = Player2Car(2, 4)

start_time = pygame.time.get_ticks() // 1000
scoreboard = Scoreboard()

while run:
    clock.tick(FPS)

    current_time = pygame.time.get_ticks() // 1000
    time_elapsed = current_time - start_time

    scoreboard.update_score(time_elapsed)

    draw(WIN, images, [player_car1, player_car2], scoreboard)
    draw_timer(WIN, time_elapsed)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    move_player(player_car1)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_car2.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_car2.rotate(right=True)
    if keys[pygame.K_UP]:
        player_car2.move_forward()
    if keys[pygame.K_DOWN]:
        player_car2.move_backward()

    if player_car1.collide(TRACK_BORDER_MASK) is not None:
        player_car1.bounce()

    if player_car2.collide(TRACK_BORDER_MASK) is not None:
        player_car2.bounce()

    finish_poi_collide1 = player_car1.collide(FINISH_MASK, *FINISH_POSITION)
    finish_poi_collide2 = player_car2.collide(FINISH_MASK, *FINISH_POSITION)

    if finish_poi_collide1 is not None or finish_poi_collide2 is not None:
        result = show_win_screen()
        if result == "return":
            start_time = pygame.time.get_ticks() // 1000
            player_car1.reset()
            player_car2.reset()
        elif result == "menu":
            run = False
            break
        pygame.quit()
pygame.quit()
