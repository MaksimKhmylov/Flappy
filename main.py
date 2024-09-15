import pygame as pg
import pygame_menu as menu

import random

import utils


SCREEN_WIDTH, SCREEN_HEIGHT = 480, 640
BIRD_WIDTH, BIRD_HEIGHT = 50, 50
PIPE_WIDTH, PIPE_GAP = 80, 100
SPEED = 10
UP = "up"
DOWN = "down"

pg.init()
pg.font.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
point_text = pg.font.SysFont(
    'Comic Sans MS', 30)
pg.display.set_caption("~-~Flappy Birdy~-~")
icon = pg.image.load("images/icon.png")
pg.display.set_icon(icon)


class Bird(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("images/bird.png")
        self.sprite_copy = self.image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 4,
                                                SCREEN_HEIGHT // 2)
                                        )
        self.gravity = 1
        self.lift = -15  # jump height
        self.velocity = 0
        self.can_jump = True
        self.sound_num = 1

    def update(self, game):
        self.image = pg.transform.rotate(self.sprite_copy, -self.velocity)
        self.velocity += self.gravity
        self.rect.y += self.velocity
        if self.rect.top < 0 and self.can_jump:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > SCREEN_HEIGHT and self.can_jump:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0
        if (self.rect.bottom > SCREEN_HEIGHT + self.rect.height
                and not self.can_jump):
            self.kill()
            game.show_end_screen()


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
        self.speed = SPEED
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

    def update(self, bird, game):
        self.rect.x -= self.speed
        self.logic(bird, game)

    def logic(self, bird, game):
        if self.rect.colliderect(bird.rect):
            bird.die()
            died = True
            bird.sprite_copy = bird.image
        if self.rect.x <= -100:
            self.kill()
        if self.rect.x == bird.rect.x - 60:
            if not game.died:
                game.points += 0.5


class Game:
    def __init__(self):
        self.points = 0
        self.died = False
        self.can_press = False
    def _render(self,pipes: pg.sprite.Group, bird: Bird, points_on_screen):
        screen.fill('white')
        for pipe in pipes:
            screen.blit(pipe.image, pipe.rect)
        screen.blit(points_on_screen, dest=(SCREEN_WIDTH // 2 - 30, 0))
        screen.blit(bird.image, bird.rect)
        pg.display.update()


    def get_user_input(self,bird: Bird):
        if pg.key.get_pressed()[
            pg.K_SPACE
        ] and self.can_press:
            bird.jump()
            self.can_press = False
        if not pg.key.get_pressed()[pg.K_SPACE]:
            self.can_press = True
        events = pg.event.get()
        for e in events:
            if e.type == pg.QUIT:
                quit("Вышел из игры")


    def main(self,ticks=1):
        self.points = 0
        bird = Bird()
        all_sprites = pg.sprite.Group()
        pipes = pg.sprite.Group()
        all_sprites.add(bird)
        bird.rect.x = 80
        self.died = False
        while True:
            bird.rect.x = SPEED*3
            points_on_screen = point_text.render(
                f"{round(self.points)}",
                False,
                (0, 0, 0))
            self._render(pipes, bird, points_on_screen)
            if ticks % 30 == 0:
                pipeup = Pipe(UP, 0)
                pipes.add(pipeup)
                pipedown = Pipe(DOWN,
                                pipeup)
                pipes.add(pipedown)

            all_sprites.update(game=self)
            pipes.update(bird, game)
            self.get_user_input(bird)
            ticks += 1
            pg.time.delay(30)

    def show_end_screen(self,):
        end_menu = menu.Menu('Игра окончена', 300, 400,
    theme=menu.themes.THEME_BLUE)
        end_menu.add.label(f'Всего очков: {round(self.points)}', font_size=30)
        end_menu.add.button('Заново', self.main)
        end_menu.add.button('Выйти', menu.events.EXIT)
        end_menu.mainloop(screen)

    def show_start_screen(self):
        start_screen = menu.Menu('Flappy Birdy', 300, 400, theme=menu.themes.THEME_BLUE)
        start_screen.add.button('Начать', self.main)
        start_screen.add.button('Выйти', menu.events.EXIT)
        start_screen.add.button('Лидеры', self.leader_board)
        start_screen.mainloop(screen)

    def leader_board(self):
        leader_screen = menu.Menu("Лидеры:", 300, 400, theme=menu.themes.THEME_BLUE)
        leader_screen.add.label(f'1 место - {utils.get_top_players()[0]}')
        leader_screen.add.label(f'2 место - {utils.get_top_players()[1]}')
        leader_screen.add.label(f'3 место - {utils.get_top_players()[2]}')
        leader_screen.add.button('Меню', self.show_start_screen)
        leader_screen.mainloop(screen)

game = Game()
if __name__ == '__main__':
    game.show_start_screen()
