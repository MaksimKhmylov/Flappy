import pygame as pg
import random

pg.init()  # У тебя ниже блок кода, перенеси эту строку в поз, например 14

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

class Bird(pg.sprite.Sprite):  # Перед определением класса делай две пустые строки
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("images/bird.png")
        self.rect = self.image.get_rect() # Эту строку можно удалить, ниже ты определяешь rect с параметрами
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        self.gravity = 1
        self.lift = -15 # Добавляй комментарии к переменным, а то не всегда понятно что они делают и за что отвечают
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
            self.sound_num += 1  # попробуй здесь использовать тернарный оператор, код будет короче и более читабельным
            if self.sound_num == 6:
                self.sound_num = 1

    def die(self):
        if self.can_jump:
            self.can_jump = False
            self.image = pg.image.load("images/bird_die.png")
            pg.mixer_music.load(f"sounds/explosion{self.sound_num}.wav")
            pg.mixer_music.play()

class Pipe(pg.sprite.Sprite):  # не забывай про две пустые строки перед классом
    def __init__(self, direction, upper_pipe):
        super().__init__()
        self.image = pg.image.load("images/pipeDown.png")  # Эта строка лишняя, т.к. image определяешь в стр 68 или 71
        self.rect = self.image.get_rect()  # Это тоже можно вынести в блок if/else стр 67
        self.speed = 10
        self.rect.x = SCREEN_WIDTH + 20
        if direction == UP:
            self.image = pg.image.load("images/pipeUp.png")
            self.rect.y = random.randint(-250, 0)
        else:
            self.image = pg.image.load("images/pipeDown.png")
            self.rect.y = upper_pipe + SCREEN_HEIGHT -100  # 100 это как я понял высота ворот из труб, давай вынесем это в константу


    def update(self):  # перед функцией внутри класса одна пустая строка, а не 2
        self.rect.x -= self.speed

bird = Bird()  # нет ли смысла весь блок 78 - 81 строку перенести в функцию main или сделать класс Game и в него добавить этот код и код из main
all_sprites = pg.sprite.Group()
pipes = pg.sprite.Group()
all_sprites.add(bird)


def main(ticks):
    can_press = False
    while True:
        if ticks % 30 == 0:
            pipeup = Pipe(UP, 0)
            pipes.add(pipeup)
            pipedown = Pipe(DOWN, pipeup.rect.y)  # предлагаю сделать более читаемый код, вторым аргументом передавать всю вернюю трубу, а в функции забирать y
            pipes.add(pipedown)
        events = pg.event.get()
        pg.transform.scale(bird.image, (BIRD_WIDTH, BIRD_HEIGHT))  # а нельзя это перенести в класс птицы, в init?
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
        if pg.key.get_pressed()[pg.K_SPACE] and can_press:  # Объясни что делает can_press? вроде как без нее должно работать?
            bird.jump()
            can_press = False
        if not pg.key.get_pressed()[pg.K_SPACE]:
            can_press = True
        ticks += 1


if __name__ == '__main__':
    main(ticks)  # не забывай добавлять одну пустую строку в конец кода, правило хорошего тона

# Перед тем как закинуть на githab, положи файл gitignore. Файл добавил, он ограничивает, чтобы мусор не летел в рипозиторий
