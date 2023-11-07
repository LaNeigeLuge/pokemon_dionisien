import pygame

from entity import Entity
from keylistener import KeyListener
from screen import Screen
from pokemon import Pokemon
from switch import Switch

class Player(Entity):
    def __init__(self, keylistener: KeyListener, screen: Screen, x: int, y: int):
        super().__init__(keylistener, screen, x, y)
        self.pokedollars: int = 0
        self.pokemons = [Pokemon.createPokemon("Pikachu", 10)]
        self.switch: list[Switch] = []

    def update(self) -> None:
        self.check_move()
        super().update()

    def check_move(self) -> None:
        if self.animation_walk is False:
            if self.keylistener.key_pressed(pygame.K_q):
                self.check_hitbox("left")
                self.move_left()
            elif self.keylistener.key_pressed(pygame.K_d):
                self.check_hitbox("right")
                self.move_right()
            elif self.keylistener.key_pressed(pygame.K_z):
                self.check_hitbox("up")
                self.move_up()
            elif self.keylistener.key_pressed(pygame.K_s):
                self.check_hitbox("down")
                self.move_down()
            elif self.keylistener.key_pressed(pygame.K_m):
                self.get_position()
    
    def check_hitbox(self, direction: str):
        temp_hitbox = self.hitbox.copy()
        if direction == "left":
            temp_hitbox.x -= 16
        elif direction == "right":
            temp_hitbox.x += 16
        elif direction == "up":
            temp_hitbox.y -= 16
        elif direction == "down":
            temp_hitbox.y += 16
        return temp_hitbox
    
    def check_collisions_switch(self):
        for switch in self.switch:
            if switch.check_collision(temps_hitbox):
                return True


    def add_switch(self, switch: Switch):
        self.switch = switch