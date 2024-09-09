import time

import pygame as pg
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 480, 640
BIRD_WIDTH, BIRD_HEIGHT = 50, 50
PIPE_WIDTH, PIPE_GAP = 80, 100
SPEED = 5
UP = "up"
DOWN = "down"
ticks = 1

pg.init()
pg.font.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
point_text = pg.font.SysFont(
    'Comic Sans MS', 30)
pg.display.set_caption("~~Flappy Bird~~")
icon = pg.image.load("images/icon.png")
pg.display.set_icon(icon)


class Bird(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("images/bird.png")
        self.sprite_copy = self.image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        self.gravity = 1
        self.lift = -15  # jump height
        self.velocity = 0
        self.can_jump = True
        self.sound_num = 1

    def update(self):
        self.image = pg.transform.rotate(self.sprite_copy, -self.velocity)
        self.velocity += self.gravity
        self.rect.y += self.velocity
        if self.rect.top < 0 and self.can_jump:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > SCREEN_HEIGHT and self.can_jump:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0
        if self.rect.bottom > SCREEN_HEIGHT + self.rect.height and not self.can_jump:
            main(1)

    def jump(self):
        if self.can_jump:
            self.velocity = self.lift
            pg.mixer_music.load(f"sounds/jump{self.sound_num}.wav")
            pg.mixer_music.play()
            self.sound_num = random.randint(1, 5)

    def die(self):
        if self.can_jump:
            self.can_jump = False
            self.image = pg.image.load("images/bird_die.png")
            pg.mixer_music.load(f"sounds/explosion{self.sound_num}.wav")
            pg.mixer_music.play()


class Pipe(pg.sprite.Sprite):
    def __init__(self, direction, upper_pipe):
        super().__init__()
        self.speed = 10
        if direction == UP:
            self.image = pg.image.load("images/pipeDown.png")
            self.rect = self.image.get_rect()
            self.rect.x = SCREEN_WIDTH + 20
            self.rect.y = random.randint(-250, 0)
        else:
            self.image = pg.image.load("images/pipeUp.png")
            self.rect = self.image.get_rect()
            self.rect.x = SCREEN_WIDTH + 20
            self.rect.y = upper_pipe.rect.y + SCREEN_HEIGHT - PIPE_GAP

    def update(self):
        self.rect.x -= self.speed





def main(ticks):
    points = 0
    bird = Bird()
    all_sprites = pg.sprite.Group()
    pipes = pg.sprite.Group()
    all_sprites.add(bird)
    can_press = False
    died = False
    while True:
        bird.rect.x = 80
        points = int(points)
        points_on_screen = point_text.render(
            f"{points}",
            False,
            (0, 0, 0))
        if ticks % 30 == 0:
            pipeup = Pipe(UP, 0)
            pipes.add(pipeup)
            pipedown = Pipe(DOWN,
                            pipeup)
            pipes.add(pipedown)
        events = pg.event.get()
        for e in events:
            if e.type == pg.QUIT:
                quit("Вышел из игры")

        screen.fill('white')
        all_sprites.update()
        pipes.update()
        for pipe in pipes:
            screen.blit(pipe.image, pipe.rect)
            if pipe.rect.colliderect(bird.rect):
                bird.die()
                died = True
                bird.sprite_copy = bird.image
            if pipe.rect.x <= -100:
                pipe.kill()
            if pipe.rect.x == bird.rect.x - 60:
                if not died:
                    points += 0.5
            if died:
                pipe.rect.x += 10

        screen.blit(points_on_screen, dest=(SCREEN_WIDTH//2 - 30, 0))
        screen.blit(bird.image, bird.rect)
        pg.display.update()
        if pg.key.get_pressed()[
            pg.K_SPACE] and can_press:
            bird.jump()
            can_press = False
        if not pg.key.get_pressed()[pg.K_SPACE]:
            can_press = True
        ticks += 1
        pg.time.delay(30)


if __name__ == '__main__':
    while True:
        main(ticks)
