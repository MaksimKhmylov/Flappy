import pygame as pg
import random

pg.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 480, 640
BIRD_WIDTH, BIRD_HEIGHT = 50, 50
PIPE_WIDTH, PIPE_GAP = 80, 250
SPEED = 5
UP = "up"
DOWN = "down"
ticks = 1


screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("~~Flappy Bird~~")
icon = pg.image.load("images/icon.png")
pg.display.set_icon(icon)

class Bird(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("images/bird.png")
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        self.gravity = 1
        self.lift = -15
        self.velocity = 0
        self.can_jump = True
        self.sound_num = 1

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity
        if self.rect.top < 0 and self.can_jump:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > SCREEN_HEIGHT and self.can_jump:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0
        if self.rect.bottom > SCREEN_HEIGHT + self.rect.height and not self.can_jump:
            quit("Умер")

    def jump(self):
        if self.can_jump:
            self.velocity = self.lift
            pg.mixer_music.load(f"sounds/jump{self.sound_num}.wav")
            pg.mixer_music.play()
            self.sound_num += 1
            if self.sound_num == 6:
                self.sound_num = 1

    def die(self):
        if self.can_jump:
            self.can_jump = False
            self.image = pg.image.load("images/bird_die.png")
            pg.mixer_music.load(f"sounds/explosion{self.sound_num}.wav")
            pg.mixer_music.play()

class Pipe(pg.sprite.Sprite):
    def __init__(self, direction, upper_pipe):
        super().__init__()
        self.image = pg.image.load("images/pipeDown.png")
        self.rect = self.image.get_rect()
        self.speed = 10
        self.rect.x = SCREEN_WIDTH + 20
        if direction == UP:
            self.image = pg.image.load("images/pipeUp.png")
            self.rect.y = random.randint(-250, 0)
        else:
            self.image = pg.image.load("images/pipeDown.png")
            self.rect.y = upper_pipe + SCREEN_HEIGHT -100


    def update(self):
        self.rect.x -= self.speed

bird = Bird()
all_sprites = pg.sprite.Group()
pipes = pg.sprite.Group()
all_sprites.add(bird)


def main(ticks):
    can_press = False
    while True:
        if ticks % 30 == 0:
            pipeup = Pipe(UP, 0)
            pipes.add(pipeup)
            pipedown = Pipe(DOWN, pipeup.rect.y)
            pipes.add(pipedown)
        events = pg.event.get()
        pg.transform.scale(bird.image, (BIRD_WIDTH, BIRD_HEIGHT))
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
            if pipe.rect.x <= -100:
                pipe.kill()
        screen.blit(bird.image, bird.rect)
        pg.display.update()
        pg.time.delay(30)
        if pg.key.get_pressed()[pg.K_SPACE] and can_press:
            bird.jump()
            can_press = False
        if not pg.key.get_pressed()[pg.K_SPACE]:
            can_press = True
        ticks += 1


if __name__ == '__main__':
    main(ticks)