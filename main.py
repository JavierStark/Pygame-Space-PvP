import pygame as pg
import os

pg.font.init()
pg.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("SpacePVP")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pg.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pg.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pg.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pg.USEREVENT + 1
RED_HIT = pg.USEREVENT + 2

HEALTH_FONT = pg.font.SysFont("comicsans", 40)
WINNER_FONT = pg.font.SysFont("comicsans", 100)

YELLOW_SPACESHIP_IMAGE = pg.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = \
    pg.transform.rotate(pg.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pg.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = \
    pg.transform.rotate(pg.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pg.transform.scale(pg.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pg.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))

    for bullet in red_bullets:
        pg.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pg.draw.rect(WIN, YELLOW, bullet)

    pg.display.update()


def check_input(red, yellow):
    keys_pressed = pg.key.get_pressed()

    if keys_pressed[pg.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    elif keys_pressed[pg.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    elif keys_pressed[pg.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    elif keys_pressed[pg.K_s] and yellow.y + VEL + yellow.height < HEIGHT:
        yellow.y += VEL

    if keys_pressed[pg.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    elif keys_pressed[pg.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    elif keys_pressed[pg.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    elif keys_pressed[pg.K_DOWN] and red.y + VEL + red.height < HEIGHT:
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pg.event.post(pg.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pg.event.post(pg.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pg.display.update()
    pg.time.delay(5000)

def main():
    red = pg.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pg.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pg.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pg.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pg.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins"
        if yellow_health <= 0:
            winner_text = "Red Wins"

        if winner_text != "":
            draw_winner(winner_text)
            break

        check_input(red, yellow)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()

