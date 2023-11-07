import pygame

from tool import Tool
from keylistener import KeyListener
from screen import Screen

class Entity(pygame.sprite.Sprite):
    def __init__(self, keylistener: KeyListener, screen: Screen, x: int, y: int):
        super().__init__()
        self.screen: Screen = screen
        self.keylistener: KeyListener = keylistener
        self.spritesheet: pygame.image = pygame.image.load("./assets/sprite/hero_01_red_m_walk.png")
        self.image: pygame.image = Tool.split_image(self.spritesheet, 0, 0, 12, 20)
        self.position: pygame.math.Vector2 = pygame.math.Vector2(x+402, y+216)
        self.rect: pygame.Rect = self.image.get_rect()
        self.all_images = self.get_all_images()
        self.index_image: int = 0
        self.image_part: int = 0
        self.reset_animation: bool = False
        self.hitbox: pygame.Rect = pygame.Rect(0, 0, 16, 16)

        self.step: int = 0
        self.animation_walk: bool = False
        self.direction: str = "down"

        self.animtion_step_time: float = 0.0
        self.action_animation: int = 16

    def update(self):
        self.animation_sprite()
        self.move()
        self.rect.center = self.position
        self.hitbox.midbottom = self.rect.midbottom
        self.image = self.all_images[self.direction][self.index_image]

    def check_move(self):
        if self.keylistener.key_pressed(pygame.K_q):
            self.move_left()
        elif self.keylistener.key_pressed(pygame.K_d):
            self.move_right()
        elif self.keylistener.key_pressed(pygame.K_z):
            self.move_up()
        elif self.keylistener.key_pressed(pygame.K_s):
            self.move_down()

    def move_left(self) -> None:
        self.animation_walk = True
        self.direction = "left"

    def move_right(self) -> None:
        self.animation_walk = True
        self.direction = "right"

    def move_up(self) -> None:
        self.animation_walk = True
        self.direction = "up"

    def move_down(self) -> None:
        self.animation_walk = True
        self.direction = "down"

    def animation_sprite(self):
        if int(self.step // 8) + self.image_part >= 4:
            self.image_part = 0
            self.reset_animation = True
        self.index_image = int(self.step // 8) + self.image_part

    def get_all_images(self):
        all_images = {
            "down": [],
            "left": [],
            "right": [],
            "up": []
        }

        width: int = self.spritesheet.get_width() // 4
        height: int = self.spritesheet.get_height() // 4

        for i in range(4):
            for j, key in enumerate(all_images.keys()):
                all_images[key].append(Tool.split_image(self.spritesheet, i * width, j * height, 24, 32))
        return all_images
    
    def align_hitbox(self) -> None:
        self.rect.center = self.position
        self.hitbox.midbottom = self.rect.midbottom
        while self.hitbox.x % 16 != 0:
            self.rect.x -= 1
            self.hitbox.midbottom = self.rect.midbottom
        while self.hitbox.y % 16 != 0:
            self.rect.y -= 1
            self.hitbox.midbottom = self.rect.midbottom
        self.position = pygame.math.Vector2(self.rect.center)
        print(self.hitbox)
    
    def move(self) -> None:
        if self.animation_walk:
            self.animtion_step_time += self.screen.get_delta_time()
            if self.step < 16 and self.animtion_step_time >= self.action_animation:
                self.step += 1
                if self.direction == "left":
                    self.position.x -= 1
                elif self.direction == "right":
                    self.position.x += 1
                elif self.direction == "up":
                    self.position.y -= 1
                elif self.direction == "down":
                    self.position.y += 1
                self.animtion_step_time = 0
            elif self.step >= 16:
                self.step = 0
                self.animation_walk = False
                if self.reset_animation:
                    self.reset_animation = False
                else:
                    if self.image_part == 0:
                        self.image_part = 2
                    else:
                        self.image_part = 0

    def get_position(self):
        print(self.position)