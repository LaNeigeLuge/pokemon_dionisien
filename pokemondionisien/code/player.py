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
        self.change_map: Switch = None

    def update(self) -> None:
        self.check_move()
        super().update()

    def check_move(self) -> None:
        if self.animation_walk is False:
            next_hitbox = self.hitbox.copy()
            if self.keylistener.key_pressed(pygame.K_q):
                next_hitbox = self.check_hitbox("left", next_hitbox)
                self.check_collisions_switch(next_hitbox)
                self.move_left()
            elif self.keylistener.key_pressed(pygame.K_d):
                next_hitbox = self.check_hitbox("right", next_hitbox)
                self.check_collisions_switch(next_hitbox)
                self.move_right()
            elif self.keylistener.key_pressed(pygame.K_z):
                next_hitbox = self.check_hitbox("up", next_hitbox)
                self.check_collisions_switch(next_hitbox)
                self.move_up()
            elif self.keylistener.key_pressed(pygame.K_s):
                next_hitbox = self.check_hitbox("down", next_hitbox)
                self.check_collisions_switch(next_hitbox)
                self.move_down()
            elif self.keylistener.key_pressed(pygame.K_m):
                self.get_position()
    
    def check_hitbox(self, direction: str, next_hitbox):
        if direction == "left":
            next_hitbox.x -= 16
        elif direction == "right":
            next_hitbox.x += 16
        elif direction == "up":
            next_hitbox.y -= 16
        elif direction == "down":
            next_hitbox.y += 16
        return next_hitbox
    
    def check_collisions_switch(self, next_hitbox: pygame.Rect):
        if self.switch:
            for switch in self.switch:
                if switch.check_collision(next_hitbox):
                    print("collision")
                    print("switch_player", switch.name)
                    self.change_map = switch
                return None


    def add_switch(self, switch: Switch):
        self.switch = switch